# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Unit tests for the KeyFrameHandler class.

import unittest
from unittest.mock import MagicMock, patch
import os
import tempfile
import shutil
import numpy as np
from PIL import Image
import cv2

from app.processing.key_frame_handler import KeyFrameHandler


class TestKeyFrameHandler(unittest.TestCase):
    def setUp(self):
        # Create mock frame displayer
        self.mock_frame_displayer = MagicMock()
        self.mock_frame_displayer.display_frame = MagicMock()
        self.mock_frame_displayer.clear_frame = MagicMock()

        # Create mock progress bar
        self.mock_progress_bar = MagicMock()
        self.mock_progress_bar.setValue = MagicMock()

        # Create directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.test_video_path = os.path.join(self.test_dir, "test_video.mp4")
        self.test_output_dir = os.path.join(self.test_dir, "data/key_frames")
        self.test_original_frames_dir = os.path.join(self.test_dir, "data/original_frames")
        self.test_histograms_dir = os.path.join(self.test_dir, "data/frame_histograms")
        
        # Create necessary directories
        os.makedirs(self.test_output_dir, exist_ok=True)
        os.makedirs(self.test_original_frames_dir, exist_ok=True)
        os.makedirs(self.test_histograms_dir, exist_ok=True)

        # Create a few test frame images in the original frames directory
        self.create_test_frames()

        # Set up patches
        self.path_is_file_patch = patch("app.processing.key_frame_handler.os.path.isfile", return_value=True)
        self.path_is_file_patch.start()

        # Create instance of KeyFrameHandler
        self.key_frame_handler = KeyFrameHandler(
            file_path=self.test_video_path,
            output_dir=self.test_output_dir,
            frame_displayer=self.mock_frame_displayer,
            progress_bar=self.mock_progress_bar
        )
        
        # Set all_frames to test dir path
        self.key_frame_handler.all_frames = self.test_original_frames_dir


    def tearDown(self):
        # Remove temporary directory and all contents
        shutil.rmtree(self.test_dir)

        # Stop patches
        self.path_is_file_patch.stop()

    def create_test_frames(self):
        # Create a few test frames in the original frames directory
        for i in range(3):
            frame_path = os.path.join(self.test_original_frames_dir, f"{i:04d}_{i*1000}.jpg")
            test_img = Image.new("RGB", (100, 100), color=(i * 50, i * 50, i * 50))
            test_img.save(frame_path)

    def test_init(self):
        # Test initialization
        self.assertEqual(self.key_frame_handler.file_path, self.test_video_path)
        self.assertEqual(self.key_frame_handler.output_dir, self.test_output_dir)
        self.assertEqual(self.key_frame_handler.frame_displayer, self.mock_frame_displayer)
        self.assertEqual(self.key_frame_handler.progress_bar, self.mock_progress_bar)
        self.assertEqual(self.key_frame_handler.total_frames, 0)
        self.assertEqual(self.key_frame_handler.all_frames, self.test_original_frames_dir)

    @patch("cv2.VideoCapture")
    @patch("cv2.imwrite")
    def test_split_video(self, mock_imwrite, mock_video_capture):
        # Mock video capture to return frames
        mock_video = MagicMock()
        mock_video_capture.return_value = mock_video
        
        # Mock video properties
        mock_video.isOpened.return_value = True
        mock_video.get.side_effect = lambda prop: {
            cv2.CAP_PROP_FRAME_COUNT: 3,
            cv2.CAP_PROP_POS_MSEC: 1000
        }.get(prop, 0)
        
        # Mock read to return 3 frames then fail
        frame_1 = np.zeros((100, 100, 3), dtype=np.uint8)
        frame_2 = np.ones((100, 100, 3), dtype=np.uint8) * 127
        frame_3 = np.ones((100, 100, 3), dtype=np.uint8) * 255
        mock_video.read.side_effect = [
            (True, frame_1), 
            (True, frame_2), 
            (True, frame_3),
            (False, None)
        ]
        
        # Call the method to test
        self.key_frame_handler._split_video()
        
        # Verify VideoCapture was called with the correct file path
        mock_video_capture.assert_called_once_with(self.test_video_path)
        
        # Verify imwrite was called for each frame
        self.assertEqual(mock_imwrite.call_count, 3)
        
        # Verify release was called
        mock_video.release.assert_called_once()
        
        # Verify progress bar was updated
        self.assertEqual(self.mock_progress_bar.setValue.call_count, 3)
        
    @patch("cv2.imread")
    @patch("cv2.cvtColor")
    @patch("cv2.calcHist")
    @patch("cv2.absdiff")
    @patch("cv2.sumElems")
    @patch("os.listdir")
    def test_calculate_frame_difference(self, mock_listdir, mock_sum_elems, 
                                       mock_absdiff, mock_calc_hist, 
                                       mock_cvt_color, mock_imread):
        # Mock directory listing
        mock_listdir.return_value = ["0000_0.jpg", "0001_1000.jpg", "0002_2000.jpg"]
        
        # Mock image reading
        mock_frame = MagicMock()
        mock_imread.return_value = mock_frame
        
        # Mock color conversion
        mock_gray_frame = MagicMock()
        mock_cvt_color.return_value = mock_gray_frame
        
        # Mock histogram calculation
        mock_hist = np.ones((256, 1), dtype=np.float32)
        mock_calc_hist.return_value = mock_hist
        
        # Mock difference calculation
        mock_diff = MagicMock()
        mock_absdiff.return_value = mock_diff
        
        # Mock sum elements
        mock_sum_elems.return_value = [100.0]
        
        # Patch the plot_histogram method to prevent actual plotting
        with patch.object(self.key_frame_handler, '_plot_histogram') as mock_plot:
            # Call the method to test
            frame_diffs = self.key_frame_handler._calculate_frame_difference()
            
            # Verify the frame differences list is correct length
            self.assertEqual(len(frame_diffs), 2)  # 3 frames means 2 pairs
            
            # Verify each frame diff contains correct data structure
            for frame_diff in frame_diffs:
                self.assertEqual(len(frame_diff), 4)  # [frame1, frame2, diff, sum_diff]
                self.assertEqual(frame_diff[3], 100.0)  # The mocked sum value
                
            # Verify the plot_histogram method was called for each pair
            self.assertEqual(mock_plot.call_count, 2)
            
            # Verify progress bar was updated
            self.assertEqual(self.mock_progress_bar.setValue.call_count, 2)
    
    def test_generate_histograms(self):
        # Create mock grayscale frames
        frame_1_gray = np.zeros((100, 100), dtype=np.uint8)
        frame_2_gray = np.ones((100, 100), dtype=np.uint8) * 255
        
        # Patch cv2.calcHist to return controlled values
        with patch('cv2.calcHist') as mock_calc_hist:
            # Setup mock return values
            hist_1 = np.zeros((256, 1), dtype=np.float32)
            hist_1[0] = 10000  # All zeros in frame_1_gray
            hist_2 = np.zeros((256, 1), dtype=np.float32)
            hist_2[255] = 10000  # All 255s in frame_2_gray
            mock_calc_hist.side_effect = [hist_1, hist_2]
            
            # Call the method
            result_hist_1, result_hist_2 = KeyFrameHandler._generate_histograms(
                frame_1_gray, frame_2_gray
            )
            
            # Verify histograms are correct
            self.assertEqual(result_hist_1[0], 10000)
            self.assertEqual(result_hist_2[255], 10000)
            
            # Verify calcHist was called twice
            self.assertEqual(mock_calc_hist.call_count, 2)
    
    def test_calculate_threshold(self):
        # Create sample frame differences
        frame_diffs = [
            ["frame1.jpg", "frame2.jpg", "diff", 100],
            ["frame2.jpg", "frame3.jpg", "diff", 200],
            ["frame3.jpg", "frame4.jpg", "diff", 300],
            ["frame4.jpg", "frame5.jpg", "diff", 400]
        ]
        
        # Expected values:
        # mean = (100+200+300+400)/4 = 250
        # sd = sqrt(((100-250)^2 + (200-250)^2 + (300-250)^2 + (400-250)^2)/4)
        # sd = sqrt(((-150)^2 + (-50)^2 + 50^2 + 150^2)/4)
        # sd = sqrt((22500 + 2500 + 2500 + 22500)/4)
        # sd = sqrt(50000/4) = sqrt(12500) = 111.8
        # threshold (with const=1) = 111.8 + (250 * 1) = 361.8
        
        # Calculate threshold with different constants
        threshold_1 = KeyFrameHandler._calculate_threshold(frame_diffs, 1)
        threshold_05 = KeyFrameHandler._calculate_threshold(frame_diffs, 0.5)
        
        # Verify calculated thresholds
        self.assertAlmostEqual(threshold_1, 361.8, places=1)
        self.assertAlmostEqual(threshold_05, 236.8, places=1)
    
    @patch("os.listdir")
    @patch("shutil.move")
    @patch("matplotlib.pyplot.savefig")
    def test_extract_keyframes(self, mock_savefig, mock_move, mock_listdir):
        # Mock the internal methods to isolate the test
        with patch.object(self.key_frame_handler, '_split_video') as mock_split_video:
            with patch.object(self.key_frame_handler, '_calculate_frame_difference') as mock_calc_diff:
                with patch.object(self.key_frame_handler, '_calculate_threshold') as mock_calc_threshold:
                    # Setup mock return values
                    mock_listdir.return_value = ["0000_0.jpg", "0001_1000.jpg", "0002_2000.jpg"]

                    # non-zero total frames
                    self.key_frame_handler.total_frames = 7

                    # Setup mock frame differences
                    mock_calc_diff.return_value = [
                        ["0000_0.jpg", "0001_1000.jpg", "diff1", 100],
                        ["0001_1000.jpg", "0002_2000.jpg", "diff2", 300]
                    ]
                    
                    # Setup mock threshold - set to 200 so only second frame diff exceeds it
                    mock_calc_threshold.return_value = 200
                    
                    # Call the extract_keyframes method
                    self.key_frame_handler.extract_keyframes()
                    
                    # Verify _split_video was called
                    mock_split_video.assert_called_once()
                    
                    # Verify _calculate_frame_difference was called
                    mock_calc_diff.assert_called_once()
                    
                    # Verify _calculate_threshold was called with const=0.7
                    mock_calc_threshold.assert_called_once()
                    self.assertEqual(mock_calc_threshold.call_args[0][1], 0.7)
                    
                    # Verify shutil.move was called once (for the frame that exceeds threshold)
                    mock_move.assert_called_once()
                    # First frame of the second pair which exceeds threshold
                    self.assertEqual(mock_move.call_args[0][0], 
                                    os.path.join(self.test_original_frames_dir, "0001_1000.jpg"))
    
    def test_init_with_invalid_parameters(self):
        # Test initialization with empty file path
        with self.assertRaises(ValueError):
            KeyFrameHandler(
                file_path="",
                output_dir=self.test_output_dir,
                frame_displayer=self.mock_frame_displayer,
                progress_bar=self.mock_progress_bar
            )
    
    @patch("cv2.VideoCapture")
    def test_split_video_with_invalid_video(self, mock_video_capture):
        # Mock video capture to fail opening
        mock_video = MagicMock()
        mock_video_capture.return_value = mock_video
        mock_video.isOpened.return_value = False
        
        # Call the method
        self.key_frame_handler._split_video()
        
        # Verify video was not processed
        mock_video.read.assert_not_called()
        mock_video.release.assert_not_called()
    
    @patch("cv2.VideoCapture")
    def test_split_video_with_read_failure(self, mock_video_capture):
        # Mock video capture to fail on first read
        mock_video = MagicMock()
        mock_video_capture.return_value = mock_video
        mock_video.isOpened.return_value = True
        mock_video.read.return_value = (False, None)
        
        # Call the method
        self.key_frame_handler._split_video()
        
        # Verify video was opened but released after read failure
        mock_video.read.assert_called_once()
        mock_video.release.assert_called_once()