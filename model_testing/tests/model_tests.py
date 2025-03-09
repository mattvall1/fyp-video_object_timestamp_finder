# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Script to run tests on models
import csv
import PIL
from io import BytesIO
import torch
import requests
from PIL import Image
from model_testing.tests.dataset_retrival.text_caps import TextCaps
from model_testing.tests.metrics.BLEU_score import BLEUScoring

# Model imports
import open_clip


# Results to CSV
def save_results(model, reference, candidate, metric, score):
    with open("results/auto_results.csv", "a", newline="\n") as rf:
        writer = csv.writer(rf)
        if rf.tell() == 0:
            writer.writerow(
                [
                    "Model",
                    "Reference(s)",
                    "Candidate",
                    "Metric",
                    "Score",
                ]
            )
        writer.writerow([model, reference, candidate, metric, score])


def save_failed_url(url):
    with open("results/failed_urls.csv", "a") as rf:
        rf.write(url + "\n")


if __name__ == "__main__":
    # Setup test
    text_caps = TextCaps()
    device = "mps"
    limit = 0  # Set to 0 to run all images

    # Get all needed details from conceptual captions
    reference_captions = text_caps.get_reference_captions()
    image_urls = text_caps.get_reference_image_urls()

    # ---------- OpenCLIP ----------
    # Load the model
    model, _, transform = open_clip.create_model_and_transforms(
        "coca_ViT-L-14", pretrained="mscoco_finetuned_laion2b_s13b_b90k", device=device
    )

    # Get scores OpenCLIP
    completion_percentage = 0
    total_images = len(reference_captions)
    for i in range(total_images):
        image_url = image_urls[i]
        print(f"Image URL: {image_url}")

        # Download the image, if it doesn't exist, skip this iteration.
        try:
            raw_image = requests.get(image_url, stream=True, timeout=5).raw
            image_data = raw_image.read()
            image = Image.open(BytesIO(image_data))
        except (
            requests.exceptions.RequestException,
            PIL.UnidentifiedImageError,
            requests.exceptions.Timeout,
        ):
            print("Image not found, ignoring")
            save_failed_url(image_url)
            continue

        # ---------- Run OpenCLIP ----------
        transformed_image = transform(image).unsqueeze(0).to(torch.float32).to(device)

        with torch.no_grad():
            generation = model.generate(transformed_image)

        candidate_caption = (
            open_clip.decode(generation[0])
            .split("<end_of_text>")[0]
            .replace("<start_of_text>", "")
        )

        # Print captions
        print(f"Reference: {reference_captions[i]}")
        print(f"Candidate: {candidate_caption}")

        # ----- Get BLEU score -----
        bleu = BLEUScoring(reference_captions[i], candidate_caption)
        print(f"Sentence BLEU score: {bleu.get_sentence_bleu_score()}\n")

        # Save results
        save_results(
            "OpenCLIP",
            reference_captions[i],
            candidate_caption,
            "BLEU",
            bleu.get_sentence_bleu_score(),
        )

        if limit != 0 and i == limit:
            break
