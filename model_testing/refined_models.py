# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: File to demonstrate all models

# ---- Imports ----
# General imports
import torch
from PIL import Image
import os
import csv
import time
from prettytable import PrettyTable

# Import the models
import open_clip
import clip

# Import the datasets (as needed)
from torchvision.datasets import ImageNet

# ---- General functions ----
def print_results(model_name, run, results):
    print(f"\n--------------- {model_name} | Run {run} ---------------")

    # Create a table of results
    results_table = PrettyTable(["Image", "Caption", "Time Taken"])
    for i in range(len(results[0])):
        results_table.add_row([os.listdir("testing_images")[i], results[0][i], results[2][i]])

    # Print the table
    print(results_table)

    # Create an overview of the results
    overview_table = PrettyTable(["Average time per image", "Total Time Taken"])
    overview_table.add_row([sum(results[2]) / len(results[2]), results[1]])

    # Print the overview
    print(overview_table)


def save_results(results):
    print("Saving results...")
    # Create CSV data
    to_write = []
    for result in results:
        for i in range(len(result[2][0])):
            # Format: Timestamp, Model Name, Run Number, Image Name, Generated Caption, Time Taken
            to_write.append([int(time.time()), result[0], result[1], os.listdir("testing_images")[i], result[2][0][i], result[2][2][i]])

    # Save data to CSV
    with open(f"model_testing/results.csv", "a+", newline='') as file:
        writer = csv.writer(file)
        # Check if file is empty and add header
        if file.tell() == 0:
            writer.writerow(["Timestamp", "Model Name", "Run Number", "Image Name", "Generated Caption", "Time Taken"])
        writer.writerows(to_write)

def run_test(model_name):
    all_results = []
    match model_name:
        case "OpenCLIP":
            for i in range(3):
                results = run_open_clip()
                print_results(model_name, i, results)
                all_results.append([model_name, i, results])
        case "CLIP":
            for i in range(3):
                results = run_clip()
                print_results(model_name, i, results)
                all_results.append([model_name, i, results])
        case _:
            print("Model not found")

    # Save all results
    save_results(all_results)

# ---- Model definitions ----
def run_open_clip():
    # Create array to store all return values
    return_values = []
    indv_timings = []

    # Time the process
    total_start_time = time.time()

    # Load the model
    model, _, transform = open_clip.create_model_and_transforms(
        'coca_ViT-L-14', 
        pretrained='mscoco_finetuned_laion2b_s13b_b90k',
        device='cuda'
    )

    # Load the image
    for image_path in os.listdir("testing_images"):
        indv_start_time = time.time()
        image = Image.open(f"testing_images/{image_path}")
        image = transform(image).unsqueeze(0).to(torch.float32).to('cuda')

        # Get the features
        with torch.no_grad(), torch.amp.autocast('cuda'):
            generation = model.generate(image)

        # Add features to return_values
        return_values.append(open_clip.decode(generation[0]).split("<end_of_text>")[0].replace("<start_of_text>", ""))
        indv_end_time = time.time()
        indv_timings.append(indv_end_time - indv_start_time)

    # End the timer
    total_end_time = time.time()

    return [return_values, total_end_time - total_start_time, indv_timings]

def run_clip():
    # Create array to store all return values
    return_values = []
    indv_timings = []

    # Time the process
    total_start_time = time.time()

    # Load the model
    device = "cuda"
    model, preprocess = clip.load('RN50', device)

    # Download the dataset
    dataset = ImageNet(root=os.path.expanduser("E:\\datasets\\imagenet-2012"))

    # Run detection on all testing images
    for image_path in os.listdir("testing_images"):
        indv_start_time = time.time()
        # Prepare the inputs
        image = Image.open(f"testing_images\\{image_path}")
        image_input = preprocess(image).unsqueeze(0).to(device)
        text_inputs = torch.cat([clip.tokenize(f"a photo of a {c}") for c in dataset.classes]).to(device)

        # Calculate features
        with torch.no_grad():
            image_features = model.encode_image(image_input)
            text_features = model.encode_text(text_inputs)

        # Pick the top 5 most similar labels for the image
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
        values, indices = similarity[0].topk(5)

        # Add features to return_values
        return_values.append([f"{image_path} - Top predictions:"])
        for value, index in zip(values, indices):
            return_values[-1].append(f"{'|'.join(dataset.classes[index]):>16s}: {100 * value.item():.2f}%")
        indv_end_time = time.time()
        indv_timings.append(indv_end_time - indv_start_time)

    # End the timer
    total_end_time = time.time()

    return [return_values, total_end_time - total_start_time, indv_timings]

# ---- Run all models ----
run_test("OpenCLIP")
run_test("CLIP")
print("All models have been run and the results have been saved.")
