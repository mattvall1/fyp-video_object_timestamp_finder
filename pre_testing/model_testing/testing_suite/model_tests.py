# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Script to run tests on models
import csv
import time
import PIL
from io import BytesIO
import nltk
import torch
import requests
from PIL import Image
from pre_testing.model_testing.testing_suite.dataset_retrival.text_caps import TextCaps
from pre_testing.model_testing.testing_suite.metrics.BLEU_score import BLEUScoring
from pre_testing.model_testing.testing_suite.metrics.METEOR_score import METEORScoring
from pre_testing.model_testing.testing_suite.metrics.ROUGE_score import ROUGEScoring

# Model imports
import open_clip
from transformers import (
    AutoProcessor,
    AutoModelForImageTextToText, AutoModelForCausalLM,
)


# Setup results file
def setup_results_file():
    with open("results/auto_results.csv", "a", newline="\n") as rf:
        writer = csv.writer(rf)
        if rf.tell() == 0:
            writer.writerow(
                [
                    "Timestamp",
                    "Model",
                    "Reference(s)",
                    "Candidate",
                    "Metric",
                    "Score",
                ]
            )
            print("Written header")

    # Open the file in append mode and return the writer object
    rf = open("results/auto_results.csv", "a", newline="\n")
    print("Results file opened")
    return csv.writer(rf), rf


# Save results to CSV
def save_results(csv_writer, model, reference, candidate, metric, score):
    csv_writer.writerow([int(time.time()), model, reference, candidate, metric, score])


# Log failed URLs
def save_failed_url(url):
    with open("results/failed_urls.csv", "a") as rf:
        rf.write(url + "\n")

# Add this function to save other errors
def save_error(error_message, image_url, model_name=None):
    with open("results/other_errors.csv", "a", newline="\n") as error_file:
        writer = csv.writer(error_file)
        if error_file.tell() == 0:
            writer.writerow(["Timestamp", "Model", "Image URL", "Error Message"])
        writer.writerow([int(time.time()), model_name or "N/A", image_url, error_message])

# Calculate scores
def calculate_scores_save(model_name, reference_captions, candidate_caption):
    # BLEU
    bleu = BLEUScoring(reference_captions, candidate_caption)
    bleu_score = bleu.get_sentence_bleu_score()
    print(f"{model_name} BLEU score: {bleu_score}")
    save_results(
        csv_writer,
        model_name,
        reference_captions,
        candidate_caption,
        "BLEU",
        bleu_score,
    )

    # METEOR
    meteor = METEORScoring(reference_captions, candidate_caption)
    meteor_score = meteor.get_meteor_score()
    print(f"{model_name} METEOR score: {meteor_score}")
    save_results(
        csv_writer,
        model_name,
        reference_captions,
        candidate_caption,
        "METEOR",
        meteor_score,
    )

    # ROUGE
    rouge = ROUGEScoring(reference_captions, candidate_caption)
    rouge_scores = rouge.get_rouge_score()
    print(f"{model_name} ROUGE-1 score: {rouge_scores}")
    print(f"{model_name} ROUGE-2 score: {rouge_scores[1][1]}")
    print(f"{model_name} ROUGE-L score: {rouge_scores[2][1]}")

    save_results(
        csv_writer,
        model_name,
        reference_captions,
        candidate_caption,
        "ROUGE-1",
        rouge_scores[0][1],
    )
    save_results(
        csv_writer,
        model_name,
        reference_captions,
        candidate_caption,
        "ROUGE-2",
        rouge_scores[1][1],
    )
    save_results(
        csv_writer,
        model_name,
        reference_captions,
        candidate_caption,
        "ROUGE-L",
        rouge_scores[2][1],
    )

    return bleu_score, meteor_score, rouge_scores


if __name__ == "__main__":
    # Setup test
    text_caps = TextCaps()
    device = "cuda"
    limit = 0  # Set to 0 to run all images
    nltk.data.path.append("E:\\yr3fyp_object_detection\\nltk_data")

    # Set up results file and get writer
    csv_writer, results_file = setup_results_file()

    # Get all needed details from conceptual captions
    reference_captions = text_caps.get_reference_captions()
    image_urls = text_caps.get_reference_image_urls()

    print("Load models...")
    # ---------- OpenCLIP ----------
    # Load the model
    openclip_model, _, openclip_transform = open_clip.create_model_and_transforms(
        "coca_ViT-L-14", pretrained="mscoco_finetuned_laion2b_s13b_b90k", device=device
    )

    # ---------- BLIP ----------
    # Load the model
    blip_processor = AutoProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )
    blip_model = AutoModelForImageTextToText.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    ).to(device)

    # ---------- Florence2 ----------
    florence_processor = AutoProcessor.from_pretrained(
        "microsoft/Florence-2-large", trust_remote_code=True
    )
    florence_model = AutoModelForCausalLM.from_pretrained(
        "microsoft/Florence-2-large", trust_remote_code=True
    ).to(device)

    print("Models loaded, starting test...")
    # Get model scores
    completion_percentage = 0
    total_images = len(reference_captions)
    total_failed = 0

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
            completion_percentage += 1
            total_failed += 1
            continue

        # Print reference captions
        print(f"Reference(s): {reference_captions[i]}")

        # ---------- Run OpenCLIP ----------
        try:
            transformed_image = (
                openclip_transform(image).unsqueeze(0).to(torch.float32).to(device)
            )

            with torch.no_grad():
                generation = openclip_model.generate(transformed_image)

            openclip_candidate_caption = (
                open_clip.decode(generation[0])
                .split("<end_of_text>")[0]
                .replace("<start_of_text>", "")
            )

            # Print candidate caption
            print(f"OpenCLIP Candidate: {openclip_candidate_caption}")

            # Calculate scores and save results
            calculate_scores_save(
                "OpenCLIP", reference_captions[i], openclip_candidate_caption
            )
        except Exception as e:
            error_msg = f"OpenCLIP processing error: {str(e)}"
            print(error_msg)
            save_error(error_msg, image_url, "OpenCLIP")

        # ---------- Run BLIP ----------
        try:
            inputs = blip_processor(images=image, text=[""], return_tensors="pt").to(device)

            with torch.no_grad():
                outputs = blip_model.generate(**inputs, max_new_tokens=50)
                blip_candidate_caption = blip_processor.decode(
                    outputs[0], skip_special_tokens=True
                )

            # Print candidate caption
            print(f"BLIP Candidate: {blip_candidate_caption}")

            # Calculate scores and save results
            calculate_scores_save("BLIP", reference_captions[i], blip_candidate_caption)
        except Exception as e:
            error_msg = f"BLIP processing error: {str(e)}"
            print(error_msg)
            save_error(error_msg, image_url, "BLIP")

        # ---------- Run Florence2 ----------
        try:
            inputs = florence_processor(images=image, text=["<MORE_DETAILED_CAPTION>"], return_tensors="pt").to(
                device
            )
            with torch.no_grad():
                outputs = florence_model.generate(**inputs, max_new_tokens=50)
                florence_candidate_caption = florence_processor.decode(
                    outputs[0], skip_special_tokens=True
                )
            # Print candidate caption
            print(f"Florence2 Candidate: {florence_candidate_caption}")

            # Calculate scores and save results
            calculate_scores_save(
                "Florence2", reference_captions[i], florence_candidate_caption
            )
        except Exception as e:
            error_msg = f"Florence2 processing error: {str(e)}"
            print(error_msg)
            save_error(error_msg, image_url, "Florence2")

        # Print progress
        completion_percentage += 1
        print(
            f"Progress: {completion_percentage}/{total_images} ({(completion_percentage / total_images) * 100:.2f}%)\n"
        )
        # Apply limit if needed
        if limit != 0 and i == limit:
            break

    # Print completion message
    print("--------------------- Testing complete | cleaning up ---------------------")
    # Close the results file
    results_file.close()
    print("Results file closed")

    # Create a summary file
    total_attempted = total_images if limit == 0 else limit
    with open("results/summary.csv", "w", newline="\n") as summary_file:
        summary_writer = csv.writer(summary_file)
        summary_writer.writerow(
            [
                "Total failed/non-existent images",
                "Total attempted images",
                "Percentage images failed",
            ]
        )
        summary_writer.writerow(
            [
                total_failed,
                total_attempted,
                f"{(total_failed / total_attempted) * 100:.2f}%",
            ]
        )
        print("Summary file created")
