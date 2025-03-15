# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Image Captioning Handler (Florence2)
from PIL import Image
import torch
from transformers import (
    AutoProcessor,
    AutoModelForCausalLM,
)


class ImageCaptioningHandler:
    def __init__(self, original_output_dir="key_frames/"):
        self.original_output_dir = original_output_dir
        self.device = "mps"  # Use "cuda" for GPU, "mps" for Mac, "cpu" for CPU
        self.model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Florence-2-large", trust_remote_code=True
        ).to(self.device)
        self.processor = AutoProcessor.from_pretrained(
            "microsoft/Florence-2-large", trust_remote_code=True
        )
        pass

    def get_captions(self, frame_location, frame):
        # Open and process the image
        image = Image.open(frame_location)
        inputs = self.processor(
            images=image, text=["<MORE_DETAILED_CAPTION>"], return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            generated_ids = self.model.generate(
                input_ids=inputs["input_ids"],
                pixel_values=inputs["pixel_values"],
                max_new_tokens=1024,
                do_sample=False,
                num_beams=3,
            )
            caption = self.processor.post_process_generation(
                self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0],
                task="<MORE_DETAILED_CAPTION>",
                image_size=(image.width, image.height),
            )["<MORE_DETAILED_CAPTION>"]

        # Return key words
        return [caption, "None"]

    def frame_caption(self, frame):
        frame_location = self.original_output_dir + "/" + frame

        # Detect objects in frame and get detected object strings
        caption_output = self.get_captions(frame_location, frame)

        # Return key words
        return [
            self.original_output_dir + "/" + frame,
            caption_output[0],
        ]  # Example return value
