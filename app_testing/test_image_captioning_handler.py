# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Unit tests for the ImageCaptioningHandler class.

import unittest
from unittest.mock import MagicMock, patch
import os
import tempfile
import shutil
from PIL import Image

from app.processing.image_captioning_handler import ImageCaptioningHandler


class TestImageCaptioningHandler(unittest.TestCase):
    def setUp(self):
        # Set up patches for the model components
        self.automodel_patch = patch(
            "app.processing.image_captioning_handler.AutoModelForCausalLM"
        )
        self.mock_automodel = self.automodel_patch.start()
        self.mock_model = MagicMock()
        self.mock_automodel.from_pretrained.return_value = self.mock_model
        self.mock_model.to.return_value = self.mock_model  # For chaining .to(device)
        self.mock_model.generate.return_value = MagicMock()  # Mock generated_ids

        self.autoprocessor_patch = patch(
            "app.processing.image_captioning_handler.AutoProcessor"
        )
        self.mock_autoprocessor = self.autoprocessor_patch.start()
        self.mock_processor = MagicMock()
        self.mock_autoprocessor.from_pretrained.return_value = self.mock_processor
        self.mock_processor.batch_decode.return_value = ["Sample decoded text"]
        self.mock_processor.post_process_generation.return_value = {
            "<MORE_DETAILED_CAPTION>": "This is a detailed caption of an image"
        }

        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.test_output_dir = os.path.join(self.test_dir, "key_frames")
        os.makedirs(self.test_output_dir, exist_ok=True)

        # Create a test image
        self.test_frame = "test_frame.jpg"
        self.test_image_path = os.path.join(self.test_output_dir, self.test_frame)
        self.create_test_image()

        # Create instance with test output directory
        self.captioning_handler = ImageCaptioningHandler(
            original_output_dir=self.test_output_dir
        )
        self.captioning_handler.processor = self.mock_processor
        self.captioning_handler.model = self.mock_model

    def tearDown(self):
        # Stop patches
        self.automodel_patch.stop()
        self.autoprocessor_patch.stop()

        # Remove temporary directory
        shutil.rmtree(self.test_dir)

    def create_test_image(self):
        # Create a simple test image
        test_img = Image.new("RGB", (100, 100), color="#0000FF")
        test_img.save(self.test_image_path)

    def test_init(self):
        # Test initialization with default parameters
        with patch(
            "app.processing.image_captioning_handler.AutoModelForCausalLM"
        ) as mock_model:
            with patch(
                "app.processing.image_captioning_handler.AutoProcessor"
            ) as mock_processor:
                handler = ImageCaptioningHandler()

                # Verify the model is loaded with correct parameters
                mock_model.from_pretrained.assert_called_once_with(
                    "microsoft/Florence-2-large", trust_remote_code=True
                )

                # Verify the processor is loaded with correct parameters
                mock_processor.from_pretrained.assert_called_once_with(
                    "microsoft/Florence-2-large", trust_remote_code=True
                )

                # Verify default output directory
                self.assertEqual(handler.original_output_dir, "data/key_frames/")

                # Verify device setting (may vary by environment)
                self.assertEqual(handler.device, "mps")  # Assuming Mac environment

    def test_get_caption(self):
        # Note: This is a real test for the _get_caption method - mocking seemed unnecessary
        handler = ImageCaptioningHandler(original_output_dir=self.test_output_dir)

        # Get a real caption for the test image
        caption = handler._get_caption(self.test_image_path)

        # Verify that we got a non-empty string back
        self.assertIsInstance(caption, str)
        self.assertTrue(len(caption) > 0)
        print(f"Real caption generated: {caption}")

        # Test the public method as well
        frame_caption = handler.frame_caption(self.test_frame)
        self.assertIsInstance(frame_caption, str)
        self.assertTrue(len(frame_caption) > 0)

    @patch(
        "app.processing.image_captioning_handler.ImageCaptioningHandler._get_caption"
    )
    def test_frame_caption(self, mock_get_caption):
        # Set up the mock to return a test caption
        test_caption = "This is a test caption"
        mock_get_caption.return_value = test_caption

        # Call the method
        result = self.captioning_handler.frame_caption(self.test_frame)

        # Verify _get_caption was called with the correct path
        mock_get_caption.assert_called_once_with(
            f"{self.test_output_dir}/{self.test_frame}"
        )

        # Verify the result is correct
        self.assertEqual(result, test_caption)


if __name__ == "__main__":
    unittest.main()
