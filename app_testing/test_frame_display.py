# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Unit tests for the FrameDisplayer class.

import unittest
from unittest.mock import MagicMock, patch
import os
import tempfile
import shutil
from PIL import Image

from app.processing.frame_display import FrameDisplayer


class TestFrameDisplayer(unittest.TestCase):
    def setUp(self):
        # Create mock preview element (QGraphicsView)
        self.mock_preview_element = MagicMock()
        self.mock_preview_element.setScene = MagicMock()
        self.mock_preview_element.fitInView = MagicMock()

        # Patch Qt components
        self.qimage_patch = patch("app.processing.frame_display.QImage")
        self.mock_qimage = self.qimage_patch.start()
        self.mock_qimage_instance = MagicMock()
        self.mock_qimage.return_value = self.mock_qimage_instance

        self.qpixmap_patch = patch("app.processing.frame_display.QPixmap")
        self.mock_qpixmap = self.qpixmap_patch.start()
        self.mock_pixmap = MagicMock()
        self.mock_qpixmap.fromImage.return_value = self.mock_pixmap

        self.qgraphicsscene_patch = patch("app.processing.frame_display.QGraphicsScene")
        self.mock_qgraphicsscene = self.qgraphicsscene_patch.start()
        self.mock_scene = MagicMock()
        self.mock_qgraphicsscene.return_value = self.mock_scene
        self.mock_scene.itemsBoundingRect.return_value = MagicMock()

        self.qapplication_patch = patch("app.processing.frame_display.QApplication")
        self.mock_qapplication = self.qapplication_patch.start()

        # Create FrameDisplayer instance
        self.frame_displayer = FrameDisplayer(self.mock_preview_element)

        # Create directory for test files
        self.test_dir = tempfile.mkdtemp()
        self.test_image_path = os.path.join(self.test_dir, "test_frame.jpg")

        # Create a test image
        test_img = Image.new("RGB", (100, 100), color="#0000FF")
        test_img.save(self.test_image_path)

    def tearDown(self):
        # Stop all patches
        self.qimage_patch.stop()
        self.qpixmap_patch.stop()
        self.qgraphicsscene_patch.stop()
        self.qapplication_patch.stop()

        # Remove temp directory
        shutil.rmtree(self.test_dir)

    def test_init(self):
        # Test initialization
        self.assertEqual(
            self.frame_displayer.preview_element, self.mock_preview_element
        )
        self.assertEqual(self.frame_displayer.scene, self.mock_scene)

        # Verify QGraphicsScene was created
        self.mock_qgraphicsscene.assert_called_once()

    def test_display_frame(self):
        # Call the method to test
        self.frame_displayer.display_frame(self.test_image_path)

        # Verify QImage was created
        self.mock_qimage.assert_called_once_with(self.test_image_path)

        # Verify QPixmap was created
        self.mock_qpixmap.fromImage.assert_called_once_with(self.mock_qimage_instance)

        # Verify pixmap was added to scene
        self.mock_scene.addPixmap.assert_called_once_with(self.mock_pixmap)

        # Verify scene was set on preview element
        self.mock_preview_element.setScene.assert_called_once_with(self.mock_scene)

        # Verify QApplication.processEvents was called
        self.mock_qapplication.processEvents.assert_called_once()

    def test_clear_frame(self):
        # Call method to test
        self.frame_displayer.clear_frame()

        # Verify scene was cleared
        self.mock_scene.clear.assert_called_once()

        # Verify new scene was created - Once in __init__, once in clear_frame
        self.assertEqual(self.mock_qgraphicsscene.call_count, 2)
