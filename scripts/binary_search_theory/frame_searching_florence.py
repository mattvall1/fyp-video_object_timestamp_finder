# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Get detailed captions from images using Florence-2 model
# Imports
import torch
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM


class FrameSearcher:
    def __init__(self):
        self.device = "mps"
        # Load the Florence-2 model
        self.processor = AutoProcessor.from_pretrained(
            "microsoft/Florence-2-large", trust_remote_code=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Florence-2-large", trust_remote_code=True
        ).to(self.device)

    # Load and return image object
    def get_image(self, image_path):
        return Image.open(image_path)

    # Get caption for an image
    def get_caption(self, image):
        # Create the prompt
        prompt = "<MORE_DETAILED_CAPTION>"

        inputs = self.processor(images=image, text=prompt, return_tensors="pt").to(
            self.device
        )

        with torch.no_grad():
            # Generate and get the detailed caption
            generated_ids = self.model.generate(
                input_ids=inputs["input_ids"],
                pixel_values=inputs["pixel_values"],
                max_new_tokens=4096,
                do_sample=False,
                num_beams=3,
            )

            results = self.processor.post_process_generation(
                self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0],
                task="<MORE_DETAILED_CAPTION>",
                image_size=(image.width, image.height),
            )
            detailed_caption = results["<MORE_DETAILED_CAPTION>"]

            return detailed_caption

    # Print caption
    def print_caption(self, caption):
        print(f"Caption: {caption}")

    # Find search term in the frame
    def find_in_frame(self, caption, search_term):
        if search_term.lower() in caption.lower():
            print(f"Found '{search_term}' in the frame.")
            return True
        else:
            print(f"'{search_term}' not found in the frame.")
            return False

    # Pipeline: load image, get caption, optionally show caption, and search
    def search_image(self, image_path, search_term, show_caption=True):
        image = self.get_image(image_path)
        caption = self.get_caption(image)
        if show_caption:
            self.print_caption(caption)
        return self.find_in_frame(caption, search_term)


# Main
if __name__ == "__main__":
    searcher = FrameSearcher()
    searcher.search_image("../../testing_images/trucks.jpg", "red truck")
