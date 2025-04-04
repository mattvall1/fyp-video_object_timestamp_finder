# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Unit tests for the CompletionHandler class.

import unittest
from unittest.mock import MagicMock, patch, mock_open
import os
import tempfile
import shutil
from PIL import Image
from app.processing.completion_handler import CompletionHandler


class TestCompletionHandler(unittest.TestCase):
    def setUp(self):
        # Create mock element handler
        self.mock_element_handler = MagicMock()
        self.mock_element_handler.selected_file_path = "/test/path/video_test.mp4"
        self.mock_element_handler.search_term = "test search term"

        # Create test matching frames data
        self.matching_frames = [
            {
                "filename": "data/key_frames/0001_1000.jpg",
                "caption": "A person walking on a street",
                "timestamp": 1.0,
            },
            {
                "filename": "data/key_frames/0003_3000.jpg",
                "caption": "A car driving down the road",
                "timestamp": 3.0,
            },
        ]

        # Create the CompletionHandler instance
        self.completion_handler = CompletionHandler(
            self.mock_element_handler, self.matching_frames
        )

        # Set up temporary directory for test files
        self.test_dir = tempfile.mkdtemp()

        # Create dummy image files
        self.create_test_images()

    def tearDown(self):
        # Remove temp directory
        shutil.rmtree(self.test_dir)

    def create_test_images(self):
        # Ensure key_frames directory exists
        os.makedirs(os.path.join(self.test_dir, "data/key_frames"), exist_ok=True)

        # Create dummy images
        for frame in self.matching_frames:
            # Create a small blank image
            img = Image.new("RGB", (100, 100), color="#ffffff")
            # Save it to the temporary path
            img_path = os.path.join(self.test_dir, frame["filename"])
            os.makedirs(os.path.dirname(img_path), exist_ok=True)
            img.save(img_path)

            # Update the path in matching_frames to use the test path
            frame["filename"] = img_path

    def test_init(self):
        self.assertEqual(
            self.completion_handler.element_handler, self.mock_element_handler
        )
        self.assertEqual(self.completion_handler.matching_frames, self.matching_frames)
        self.assertEqual(self.completion_handler.video_name, "video_test")

    @patch("app.processing.completion_handler.canvas.Canvas")
    def test_setup_pdf(self, mock_canvas):
        # Setup mock canvas
        mock_canvas_instance = MagicMock()
        mock_canvas.return_value = mock_canvas_instance

        # Call the method
        report_path = "/test/report/path"
        result = self.completion_handler._setup_pdf(report_path)

        # Verify the PDF was created correctly
        mock_canvas.assert_called_once_with(
            f"{report_path}/completion_report_video_test.pdf",
            pagesize=(595.2755905511812, 841.8897637795277),  # A4 size
        )
        mock_canvas_instance.setTitle.assert_called_once_with(
            "Completion Report for video_test"
        )
        mock_canvas_instance.setFont.assert_called_once_with("Helvetica", 12)
        self.assertEqual(result, mock_canvas_instance)

    @patch("app.processing.completion_handler.Image.open")
    @patch("app.processing.completion_handler.canvas.Canvas")
    def test_generate_pdf_content(self, mock_canvas, mock_image_open):
        # Setup mock canvas
        mock_canvas_instance = MagicMock()

        # Setup mock image
        mock_img = MagicMock()
        mock_img.size = (800, 600)  # Test image dimensions
        mock_image_open.return_value = mock_img

        # Call the method
        self.completion_handler._generate_pdf_content(mock_canvas_instance)

        # Verify that the PDF content methods were called (basic verification)
        self.assertTrue(mock_canvas_instance.drawCentredString.called)
        self.assertTrue(mock_canvas_instance.drawString.called)
        self.assertTrue(mock_canvas_instance.drawInlineImage.called)
        self.assertTrue(mock_canvas_instance.rect.called)
        self.assertTrue(mock_canvas_instance.line.called)

        # Verify image was opened for each matching frame
        self.assertEqual(mock_image_open.call_count, len(self.matching_frames))

    @patch("app.processing.completion_handler.canvas.Canvas")
    def test_save_pdf(self, mock_canvas):
        # Setup mock canvas
        mock_canvas_instance = MagicMock()

        # Call the method
        self.completion_handler._save_pdf(mock_canvas_instance)

        # Verify the PDF was saved
        mock_canvas_instance.save.assert_called_once()

    @patch("app.processing.completion_handler.Image.open")
    @patch("app.processing.completion_handler.canvas.Canvas")
    def test_generate_completion_report(self, mock_canvas, mock_image_open):
        # Setup mock canvas
        mock_canvas_instance = MagicMock()
        mock_canvas.return_value = mock_canvas_instance

        # Setup mock image
        mock_img = MagicMock()
        mock_img.size = (800, 600)  # Test image dimensions
        mock_image_open.return_value = mock_img

        # Call the main method
        report_path = "/test/report/path"
        self.completion_handler.generate_completion_report(report_path)

        # Verify setup_pdf was called with correct path
        mock_canvas.assert_called_once_with(
            f"{report_path}/completion_report_video_test.pdf",
            pagesize=(595.2755905511812, 841.8897637795277),  # A4 size
        )

        # Verify content was generated
        self.assertTrue(mock_canvas_instance.drawCentredString.called)

        # Verify PDF was saved
        mock_canvas_instance.save.assert_called_once()

    def test_init_with_empty_matching_frames(self):
        # Test initialization with empty matching frames list
        handler = CompletionHandler(self.mock_element_handler, [])
        
        # Verify the empty list was saved
        self.assertEqual(handler.matching_frames, [])
        self.assertEqual(handler.video_name, "video_test")
    
    def test_init_with_invalid_matching_frames(self):
        # Test initialization with invalid matching frames format
        invalid_frames = [{"invalid_key": "value"}]
        
        # Initialize without required fields should not raise error during init
        # but will cause issues during PDF generation
        handler = CompletionHandler(self.mock_element_handler, invalid_frames)
        self.assertEqual(handler.matching_frames, invalid_frames)
    
    @patch("app.processing.completion_handler.canvas.Canvas")
    def test_setup_pdf_with_invalid_path(self, mock_canvas):
        # Setup mock canvas that raises an exception when file can't be created
        mock_canvas.side_effect = IOError("Cannot create file")
        
        # Call the method and expect an exception
        with self.assertRaises(IOError):
            self.completion_handler._setup_pdf("/nonexistent/directory")
    
    @patch("app.processing.completion_handler.Image.open")
    @patch("app.processing.completion_handler.canvas.Canvas")
    def test_generate_pdf_content_with_missing_images(self, mock_canvas, mock_image_open):
        # Setup mock canvas
        mock_canvas_instance = MagicMock()
        
        # Setup mock image.open to raise FileNotFoundError
        mock_image_open.side_effect = FileNotFoundError("File not found")
        
        # Create handler with frames pointing to non-existent images
        bad_frames = [
            {
                "filename": "/nonexistent/path/frame.jpg",
                "caption": "Test caption",
                "timestamp": 1.0
            }
        ]
        handler = CompletionHandler(self.mock_element_handler, bad_frames)
        
        # Call the method and expect an exception
        with self.assertRaises(FileNotFoundError):
            handler._generate_pdf_content(mock_canvas_instance)
