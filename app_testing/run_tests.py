# © 2025 Matthew Vallance. All rights reserved.
# COMP1682 Final Year Project.
# Purpose: Run all tests in the app_testing directory.
import unittest
import sys
import os


def run_tests():
    """Discovers then run all tests in the app_testing directory"""
    # Get the current directory (app_testing)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Ensure the parent directory is in the Python path (to allow importing from app module)
    parent_dir = os.path.dirname(current_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    # Set up the test loader
    loader = unittest.TestLoader()

    # Discover all tests in the current directory (app_testing)
    test_suite = loader.discover(current_dir)

    # Create a test runner
    runner = unittest.TextTestRunner(verbosity=2)

    # Run the tests
    result = runner.run(test_suite)

    # Return True if all tests pass, False otherwise
    return result.wasSuccessful()


if __name__ == "__main__":
    # Run the tests and use the result as the exit code
    success = run_tests()
    sys.exit(0 if success else 1)
