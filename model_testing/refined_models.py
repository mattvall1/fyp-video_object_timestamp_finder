# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: File to demonstrate all models
import torch
from PIL import Image
import open_clip
import os
import time
from prettytable import PrettyTable

# ---- Setup ----
device = "mps"
image_paths = []
runs = 0

# Get all image paths
dir_paths = os.listdir("../testing_images")
for dir_path in dir_paths:
    if dir_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
        image_paths.append("../testing_images/"+dir_path)


# ---- General functions ----
def print_results(model_name, run, results):
    print(f"\n--------------- {model_name} | Run {run} ---------------")

    # Create a table of results
    results_table = PrettyTable(["Image", "Caption", "Time Taken"])
    for i in range(len(results[0])):
        results_table.add_row([image_paths[i], results[0][i], results[2][i]])

    # Print the table
    print(results_table)

    # Create an overview of the results
    overview_table = PrettyTable(["Average time per image", "Total Time Taken"])
    overview_table.add_row([sum(results[2]) / len(results[2]), results[1]])

    # Print the overview
    print(overview_table)


def save_results(results):
    print("Saving results...")
    with open(f"results.csv", "a+") as csv:
        for result in results:
            csv.write(f"{time.time()},{result[0]},{result[1]}\n")

def run_test(model_name):
    all_results = []
    match model_name:
        case "OpenCLIP":
            for i in range(runs):
                results = run_open_clip()
                print_results(model_name, i, results)
                all_results.append([model_name, results])
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
        device=device
    )

    # Load the image
    for image_path in image_paths:
        indv_start_time = time.time()
        # Skip if not an image
        if image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            image = Image.open(image_path)
        else:
            continue
        image = transform(image).unsqueeze(0).to(torch.float32).to(device)

        # Get the features
        with torch.no_grad():
            generation = model.generate(image)

        # Add features to return_values
        return_values.append(open_clip.decode(generation[0]).split("<end_of_text>")[0].replace("<start_of_text>", ""))
        indv_end_time = time.time()
        indv_timings.append(indv_end_time - indv_start_time)

    # End the timer
    total_end_time = time.time()

    return [return_values, total_end_time - total_start_time, indv_timings]

# ---- Run all models ----
run_test("OpenCLIP")
print("All models have been run and the results have been saved.")
