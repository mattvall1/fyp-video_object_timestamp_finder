# Testing notes

This directory contains all automated tests for the application

## Test diirectory structure

- `test_global_tools.py` - Test for global tools
- `test_frame_display.py` - Tests for frame display functionality
- `test_file_handler.py` - Tests for file handling
- `test_image_captioning_handler.py` - Tests for image captioning
- `test_completion_handler.py` - Tests for completion report generation
- `run_tests.py` - Script to run all tests

## Running Tests

Open a terminal and navigate to the app_testing directory of the project. Then run:

To run all tests:

```bash
python run_tests.py
```

To run specific test files:

```bash
python test_file_handler.py
```

## Testing Approach

The test suite includes both positive and negative test cases:

- **Positive tests**: Verify that components work correctly with valid inputs
- **Negative tests**: Verify that components handle invalid inputs, edge cases, and error conditions appropriately

## Notes

