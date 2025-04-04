import os
import shutil
import tempfile
import unittest
from unittest.mock import patch, mock_open, call

# Import the Tools class from the app module
from app.global_tools import Tools


class TestGlobalTools(unittest.TestCase):
    def setUp(self):
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

        # Create test directories (to test clear_frame_directories)
        os.makedirs(os.path.join(self.test_dir, "data/key_frames"))
        os.makedirs(os.path.join(self.test_dir, "data/original_frames"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "data/frame_histograms"), exist_ok=True)

    def tearDown(self):
        # Clean up temporary directory
        shutil.rmtree(self.test_dir)

    @patch("os.remove")
    @patch("os.path.isfile", return_value=True)
    @patch("os.listdir")
    def test_clear_frame_directories(self, mock_listdir, mock_isfile, mock_remove):
        # Mock return values for os.listdir
        mock_listdir.side_effect = [
            ["0000.jpg", "0001.jpg", "0002.jpg", "0003.jpg"],  # key_frames
            [
                "0000.jpg",
                "0001.jpg",
                "0002.jpg",
                "0003.jpg",
                "0004.jpg",
                "0005.jpg",
                "0006.jpg",
            ],  # original_frames
            ["0000_0001_hist.jpg", "0001_0002_hist.jpg"],  # frame_histograms
        ]

        # Call clear_frame_directories
        count = Tools.clear_frame_directories()

        # Check if the correct number of files were deleted
        self.assertEqual(count, 13)

        # Check if os.listdir was called for each directory
        self.assertEqual(mock_listdir.call_count, 3)

        # Check if os.remove was called for each file
        self.assertEqual(mock_remove.call_count, 13)

    @patch("os.makedirs")
    @patch("builtins.print")
    def test_create_directories(self, mock_print, mock_makedirs):
        # Expected directories to be created (TODO: Update with actual expected directories, when we get to full testing phase)
        expected_dirs = [
            "data",
            "data/key_frames",
            "data/frame_histograms",
            "data/original_frames",
            "logs",
        ]

        # Call create_directories
        Tools.create_directories()

        # Check if os.makedirs was called for each directory
        self.assertEqual(mock_makedirs.call_count, len(expected_dirs))

        # Check if each directory was created with exist_ok=True
        mock_makedirs.assert_has_calls(
            [call(dir_name, exist_ok=True) for dir_name in expected_dirs],
            any_order=True,
        )

        # Check if a print message was made for each directory
        self.assertEqual(mock_print.call_count, len(expected_dirs))

        # Check the print messages
        mock_print.assert_has_calls(
            [call(f"Created directory: {dir_name}") for dir_name in expected_dirs],
            any_order=True,
        )

    @patch("os.remove")
    @patch("os.path.isfile")
    @patch("os.listdir")
    def test_clear_frame_directories_with_non_files(self, mock_listdir, mock_isfile, mock_remove):
        # Mock return values
        mock_listdir.side_effect = [
            ["file1.jpg", "file2.jpg", "not_a_file"],  # key_frames
            ["file3.jpg", "file4.jpg"],  # original_frames
            [],  # frame_histograms (empty)
        ]
        
        # Mock isfile to return False for "not_a_file"
        mock_isfile.side_effect = lambda path: "not_a_file" not in path
        
        # Call clear_frame_directories
        count = Tools.clear_frame_directories()
        
        # Check if the correct number of files were deleted (4, not 5)
        self.assertEqual(count, 4)
        
        # Verify os.remove was called only for actual files
        self.assertEqual(mock_remove.call_count, 4)
    
    @patch("os.remove")
    @patch("os.path.isfile", return_value=True)
    @patch("os.listdir")
    def test_clear_frame_directories_with_permission_error(self, mock_listdir, mock_isfile, mock_remove):
        # Mock return values
        mock_listdir.return_value = ["file1.jpg", "file2.jpg"]
        
        # Mock os.remove to raise PermissionError for the second file
        mock_remove.side_effect = [None, PermissionError("Permission denied")]
        
        # Call and expect exception
        with self.assertRaises(PermissionError):
            Tools.clear_frame_directories()
        
        # Verify os.remove was called twice before exception
        self.assertEqual(mock_remove.call_count, 2)
    
    @patch("os.makedirs")
    @patch("builtins.print")
    def test_create_directories_with_permission_error(self, mock_print, mock_makedirs):
        # Mock os.makedirs to raise PermissionError
        mock_makedirs.side_effect = PermissionError("Permission denied")
        
        # Call and expect exception
        with self.assertRaises(PermissionError):
            Tools.create_directories()


if __name__ == "__main__":
    unittest.main()
