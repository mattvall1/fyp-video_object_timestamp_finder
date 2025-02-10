# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: File to demonstrate all models
import torch
from PIL import Image
import open_clip
import os
import time
from prettytable import PrettyTable

# ---- General functions ----
def print_results(model_name, results):
    print(f"--------------- {model_name} ---------------")

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


def save_results(model_name, results):
    pass

def print_save_results(model_name, results):
    print_results(model_name, results)
    save_results(model_name, results)

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

# ---- Run all models ----
print_save_results("OpenCLIP", run_open_clip())
