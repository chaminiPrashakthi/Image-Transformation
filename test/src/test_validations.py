import sys
import os
import unittest
from datetime import datetime
from unittest import mock
from unittest.mock import patch, MagicMock


from pathlib import Path
from src import constants, validations

sys.modules['src.validations'] = mock.Mock()

class TestValidation(unittest.TestCase):
    def setUp(self):
        print('Start Validation class UTs')
        
    def test_validate_data_object_success(self):
        data_object = {
            "timestamp": "2023-03-28T04:55:04.307000+00:00",
            "description": {
                "width" : 20,
                "height": 20
            },
            "image": ""
            }
        output = validations.validate_data_object(data_object, constants.RESIZE)
        self.assertEqual(output, (True, None))
        
    def test_validate_data_object_empty_image(self):
        data_object = {
            "timestamp": "2023-03-28T04:55:04.307000+00:00",
            "description": "Bottom"
            }
        output = validations.validate_data_object(data_object, constants.RESIZE)
        self.assertEqual(output, (False, 'Both Base64 Image value and description are required'))
        
    def test_validate_data_object_empty_description(self):
        data_object = {
            "timestamp": "2023-03-28T04:55:04.307000+00:00",
            "image": "test image"
            }
        output = validations.validate_data_object(data_object, constants.RESIZE)
        self.assertEqual(output, (False, 'Both Base64 Image value and description are required'))
    
    def test_validate_data_object_empty_height(self):
        data_object = {
            "timestamp": "2023-03-28T04:55:04.307000+00:00",
            "description": {
                "height": 20},
            "image": "test image"
            }
        output = validations.validate_data_object(data_object, constants.RESIZE)
        self.assertEqual(output, (False, 'if process type is Resizing, you must provide valid description with height and width.(ex: description: {width : 20, height: 20}) '))
        
    @patch('src.validations.is_valid_base64_image')
    def test_validate_data_object_valid_base64image(self, mock_base64_image):
        data_object = {
            "timestamp": "2023-03-28T04:55:04.307000+00:00",
            "description": "Bottom",
            "image": "test image"
            }
        mock_base64_image.return_value = True
        output = validations.validate_data_object(data_object, constants.FLIP)
        self.assertEqual(output, (True, None))
        
    @patch('src.validations.is_valid_base64_image')
    def test_validate_data_object_invalid_base64image(self, mock_base64_image):
        data_object = {
            "timestamp": "2023-03-28T04:55:04.307000+00:00",
            "description": "Bottom",
            "image": "test image"
            }
        mock_base64_image.return_value = False
        output = validations.validate_data_object(data_object, constants.FLIP)
        self.assertEqual(output, (False, 'The image file is not valid base64 image'))
        
    def test_validate_description_invalid_scenario_flip(self):
        output = validations.validate_description(constants.FLIP, "test")
        self.assertEqual(output, (False, 'Enter a valid Flipping type (ex: Top, Bottom, Left, Right)'))
        
    def test_validate_description_resize(self):
        description = {
                "width" : 20,
                "height": 20
            }
        output = validations.validate_description(constants.RESIZE, description)
        self.assertEqual(output, (True, None))
        
    def test_validate_description_invalid_scenario_resize(self):
        description = {
                "width" : "",
                "height": 20
            }
        output = validations.validate_description(constants.RESIZE, description)
        self.assertEqual(output, (False, 'Enter the resolution in (width, height) format (ex: (20,20))'))
      
       
    def test_is_valid_base64_image(self):
        mock_base64 = MagicMock()
        mock_io_bytes = MagicMock()
        mock_open = MagicMock()
        mock_base64.return_value = 'Mock Base 64'
        mock_io_bytes.return_value = 'Mock_IO'
        mock_open.get.side_effect = Exception
        output = validations.is_valid_base64_image("test image")
        self.assertEqual(output, False)
        