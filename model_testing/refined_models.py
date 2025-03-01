# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Standalone script to demonstrate all models
import csv
import requests
import torch
from PIL import Image
import os
import time
from prettytable import PrettyTable

# ---- Model imports ----
import open_clip
from ultralytics import YOLO
from ultralytics import settings as yolo_settings
from transformers import pipeline, AutoProcessor, AutoModelForImageTextToText, AutoModelForCausalLM

# ---- Setup ----
device = "mps"
image_paths = []
runs = 2
models_to_run = ["OpenCLIP", "YOLO", "SalesForceBLIP", "Florence2"]

# YOLO settings (if using YOLO)
if "YOLO" in models_to_run:
    yolo_settings.update({"datasets_dir": "../../datasets", "runs_dir": "detection_output/yolo_runs", "weights_dir": "detection_output/yolo_runs"})

# Get all image paths
path = "../testing_images"
dir_paths = os.listdir(path)
for dir_path in dir_paths:
    if dir_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
        image_paths.append(path+"/"+dir_path)


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
    # Create CSV data
    to_write = []
    for result in results:
        for run in range(len(result[1][0])):
            # Format: Timestamp, Model Name, Run Number, Image Name, Generated Caption, Time Taken
            to_write.append([int(time.time()), result[0], run, image_paths[run], result[1][0][run], result[1][2][run]])
    # Save data to CSV
    with open(f"results.csv", "a+", newline='') as file:
        writer = csv.writer(file)
        # Check if file is empty and add header
        if file.tell() == 0:
            writer.writerow(["Timestamp", "Model Name", "Run Number", "Image Name", "Model output", "Time Taken"])
        writer.writerows(to_write)

def run_test(save_results=True):
    for model_name in models_to_run:
        run_results = []
        match model_name:
            case "OpenCLIP":
                for i in range(runs):
                    results = run_open_clip()
                    print_results(model_name, i, results)
                    run_results.append([model_name, results])
            case "YOLO":
                for i in range(runs):
                    results = run_yolo()
                    print_results(model_name, i, results)
                    run_results.append([model_name, results])
            case "SalesForceBLIP":
                for i in range(runs):
                    results = run_blip()
                    print_results(model_name, i, results)
                    run_results.append([model_name, results])
            case "Florence2":
                for i in range(runs):
                    results = run_florence2()
                    print_results(model_name, i, results)
                    run_results.append([model_name, results])
            case _:
                print("Model not found, continuing...")

        # Save run results
        if save_results:
            save_results(run_results)

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
        image = transform(Image.open(image_path)).unsqueeze(0).to(torch.float32).to(device)

        # Get the features
        with torch.no_grad():
            generation = model.generate(image)

        # Add features to return_values
        indv_end_time = time.time()
        return_values.append(open_clip.decode(generation[0]).split("<end_of_text>")[0].replace("<start_of_text>", ""))
        indv_timings.append(indv_end_time - indv_start_time)

    # End the timer
    total_end_time = time.time()

    return [return_values, total_end_time - total_start_time, indv_timings]

def run_yolo():
    # Create array to store all return values
    return_values = []
    indv_timings = []

    # Time the process
    total_start_time = time.time()

    # Load the image
    for image_path in image_paths:
        indv_start_time = time.time()

        # Load the model
        model = YOLO("yolo11n.pt")

        # Perform object detection on an image
        detection = model(image_path)

        # Get a list of names of detected objects
        detected_objects = []
        for cls in detection[0].boxes.cls:
            detected_objects.append(detection[0].names[cls.item()])

        # Print the detected objects
        indv_end_time = time.time()
        return_values.append(', '.join(detected_objects))
        indv_timings.append(indv_end_time - indv_start_time)

    # End the timer
    total_end_time = time.time()

    return [return_values, total_end_time - total_start_time, indv_timings]

def run_blip():
    # Create array to store all return values
    return_values = []
    indv_timings = []

    # Time the process
    total_start_time = time.time()

    # Load the model
    processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = AutoModelForImageTextToText.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

    # Process each image
    for image_path in image_paths:
        indv_start_time = time.time()

        image = Image.open(image_path)
        inputs = processor(images=image, text=[""], return_tensors="pt").to(device)

        with torch.no_grad():
            outputs = model.generate(**inputs, max_new_tokens=50)
            caption = processor.decode(outputs[0], skip_special_tokens=True)
            return_values.append(caption)

        indv_end_time = time.time()
        indv_timings.append(indv_end_time - indv_start_time)

    # End the timer
    total_end_time = time.time()

    return [return_values, total_end_time - total_start_time, indv_timings]

def run_florence2():
    # Create array to store all return values
    return_values = []
    indv_timings = []

    # Time the process
    total_start_time = time.time()

    # Load the model
    processor = AutoProcessor.from_pretrained("microsoft/Florence-2-large", trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained("microsoft/Florence-2-large", trust_remote_code=True).to(device)

    # Process each image
    for image_path in image_paths:
        indv_start_time = time.time()

        image = Image.open(image_path)
        inputs = processor(images=image, text=["<CAPTION>"], return_tensors="pt").to(device)

        with torch.no_grad():
            generated_ids = model.generate(
                input_ids=inputs["input_ids"],
                pixel_values=inputs["pixel_values"],
                max_new_tokens=1024,
                do_sample=False,
                num_beams=3
            )
            return_values.append(processor.post_process_generation(processor.batch_decode(generated_ids, skip_special_tokens=True)[0], task="<CAPTION>", image_size=(image.width, image.height))["<CAPTION>"])

        indv_end_time = time.time()
        indv_timings.append(indv_end_time - indv_start_time)

    # End the timer
    total_end_time = time.time()

    return [return_values, total_end_time - total_start_time, indv_timings]


# ---- Run all models ----
if __name__ == "__main__":
    run_test(False)
    print("All models have been run and the results have been saved.")
