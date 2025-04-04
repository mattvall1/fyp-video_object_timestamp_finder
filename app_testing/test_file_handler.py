# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Unit tests for the FileHandler class.

import unittest
from unittest.mock import MagicMock, patch, mock_open
import os
import tempfile
import csv
from io import StringIO

from app.processing.file_handler import FileHandler


class TestFileHandler(unittest.TestCase):
    def setUp(self):
        # Mock element handler
        self.mock_element_handler = MagicMock()
        self.mock_element_handler.preview_element = MagicMock()
        self.mock_element_handler.progress_bar = MagicMock()
        self.mock_element_handler.search_term_handler = MagicMock()
        self.mock_element_handler.search_term_handler.compare_caption_to_search_term.return_value = [
            "test"
        ]

        # Mock file path
        self.test_file_path = "/test/path/test_video.mp4"

        # Create test directory
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.test_dir, "data/key_frames")
        os.makedirs(self.output_dir, exist_ok=True)

        # Set up patches
        # Note: this prevents segfault
        self.frame_displayer_patch = patch(
            "app.processing.frame_display.FrameDisplayer", autospec=True
        )
        self.mock_frame_displayer_class = self.frame_displayer_patch.start()
        self.mock_frame_displayer = MagicMock()
        self.mock_frame_displayer_class.return_value = self.mock_frame_displayer

        self.tools_patch = patch("app.processing.file_handler.Tools")
        self.mock_tools = self.tools_patch.start()

        self.setup_caption_patch = patch(
            "app.processing.file_handler.FileHandler._setup_caption_file"
        )
        self.mock_setup_caption = self.setup_caption_patch.start()
        self.mock_csv_writer = MagicMock()
        self.mock_file = MagicMock()
        self.mock_setup_caption.return_value = (self.mock_csv_writer, self.mock_file)

        # Create FileHandler instance
        with patch(
            "app.processing.file_handler.FrameDisplayer",
            self.mock_frame_displayer_class,
        ):
            self.file_handler = FileHandler(
                self.test_file_path, self.mock_element_handler
            )
            self.file_handler.frame_displayer = self.mock_frame_displayer
            self.file_handler.output_dir = self.output_dir

    def tearDown(self):
        # Stop all patches
        self.setup_caption_patch.stop()
        self.tools_patch.stop()
        self.frame_displayer_patch.stop()

        # Clean up temp directory if necessary
        if os.path.exists(self.test_dir):
            import shutil

            shutil.rmtree(self.test_dir)

    def test_init(self):
        self.assertEqual(self.file_handler.file_path, self.test_file_path)
        self.assertEqual(self.file_handler.element_handler, self.mock_element_handler)
        self.assertEqual(self.file_handler.matching_frames, [])
        self.mock_tools.clear_frame_directories.assert_called_once()
        self.mock_setup_caption.assert_called_once_with("test_video")

    def test_setup_caption_file(self):
        # Stop patch to test the actual method
        self.setup_caption_patch.stop()

        # Use context manager to handle open mock
        with patch("builtins.open", mock_open()) as mock_file:
            csv_writer, file_handle = FileHandler._setup_caption_file("test_video")

            # Verify file was opened
            mock_file.assert_called_once_with(
                "data/test_video_captions.csv", "w", newline="\n", encoding="utf-8"
            )

            # Verify writer was created
            self.assertTrue(isinstance(csv_writer, csv.writer(StringIO()).__class__))

            # Verify file handle was returned
            self.assertEqual(file_handle, mock_file())

        # Restart patch for other tests
        self.mock_setup_caption = self.setup_caption_patch.start()
        self.mock_setup_caption.return_value = (self.mock_csv_writer, self.mock_file)

    @patch("app.processing.file_handler.KeyFrameHandler")
    @patch("app.processing.file_handler.FileHandler._process_keyframes")
    def test_retrieve_keyframes(
        self, mock_process_keyframes, mock_key_frame_handler_class
    ):
        # Create mock for KeyFrameHandler instance
        mock_key_frame_handler = MagicMock()
        mock_key_frame_handler_class.return_value = mock_key_frame_handler

        # Call method to test
        self.file_handler.retrieve_keyframes()

        # Verify KeyFrameHandler was instantiated correctly
        mock_key_frame_handler_class.assert_called_once_with(
            file_path=self.test_file_path,
            output_dir=self.output_dir,
            frame_displayer=self.mock_frame_displayer,
            progress_bar=self.mock_element_handler.progress_bar,
        )

        # Verify the extract_keyframes method was called
        mock_key_frame_handler.extract_keyframes.assert_called_once()

        # Verify _process_keyframes was called
        mock_process_keyframes.assert_called_once()

    # This is a pretty slow test - no need to be alarmed
    @patch("os.listdir")
    @patch("app.processing.file_handler.ImageCaptioningHandler")
    @patch("app.processing.file_handler.CompletionHandler")
    def test_process_keyframes(
        self,
        mock_completion_handler_class,
        mock_image_captioning_handler_class,
        mock_listdir,
    ):
        # Mock frame listing
        mock_listdir.return_value = ["frame_0001_1000.jpg", "frame_0002_2000.jpg"]

        # Mock image captioning handler
        mock_image_captioning_handler = MagicMock()
        mock_image_captioning_handler.frame_caption.return_value = "Test caption"
        mock_image_captioning_handler_class.return_value = mock_image_captioning_handler

        # Mock completion handler
        mock_completion_handler = MagicMock()
        mock_completion_handler_class.return_value = mock_completion_handler

        # Mock generate_report_modal to return a report path
        self.mock_element_handler.generate_report_modal.return_value = (
            "/test/report/path"
        )

        # Call the method to test
        self.file_handler._process_keyframes()

        # Verify the image captioning handler was instantiated correctly
        mock_image_captioning_handler_class.assert_called_once_with(
            original_output_dir=self.output_dir
        )

        # Verify frames were processed
        self.assertEqual(mock_image_captioning_handler.frame_caption.call_count, 2)

        # Verify frame display
        self.assertEqual(self.mock_frame_displayer.display_frame.call_count, 2)

        # Verify caption saving
        self.assertEqual(self.mock_csv_writer.writerow.call_count, 2)

        # Verify matching frames were added (2 matches)
        self.assertEqual(len(self.file_handler.matching_frames), 2)

        # Verify completion handler created and generate_report called
        mock_completion_handler_class.assert_called_once_with(
            self.mock_element_handler, self.file_handler.matching_frames
        )
        mock_completion_handler.generate_completion_report.assert_called_once_with(
            "/test/report/path"
        )

        # Verify file closed
        self.mock_file.close.assert_called_once()

    def test_save_caption(self):
        # Call the method to test
        frame = "test_frame.jpg"
        caption = "This is a test caption"
        self.file_handler.save_caption(frame, caption)

        # Verify csv writer was called correctly
        self.mock_csv_writer.writerow.assert_called_once_with([frame, caption])
