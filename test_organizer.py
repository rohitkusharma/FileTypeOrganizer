#!/usr/bin/env python3
"""
Unit tests for the FileOrganizer script.

This test suite validates the core functionality of the file organization system,
including file discovery, categorization, and configuration loading.
"""

import unittest
import tempfile
import os
import shutil
import json
from unittest.mock import patch, MagicMock
import sys

# Add the current directory to the path so we can import organizer
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import organizer


class TestFileOrganizer(unittest.TestCase):
    """Test cases for the file organizer functionality."""

    def setUp(self):
        """Set up test environment with temporary directories and files."""
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create test files with various extensions
        self.test_files = [
            'document.pdf',
            'image.jpg', 
            'video.mp4',
            'audio.mp3',
            'script.py',
            'archive.zip',
            'noextension',
            'unknown.xyz'
        ]
        
        for filename in self.test_files:
            with open(filename, 'w') as f:
                f.write('test content')

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_get_files_to_organize(self):
        """Test that get_files_to_organize returns correct list of files."""
        files = organizer.get_files_to_organize(self.test_dir)
        
        # Should return all files except the script itself
        self.assertIsInstance(files, list)
        self.assertTrue(len(files) > 0)
        
        # Check that it includes our test files
        for test_file in self.test_files:
            self.assertIn(test_file, files)

    def test_get_files_to_organize_nonexistent_dir(self):
        """Test get_files_to_organize with non-existent directory."""
        result = organizer.get_files_to_organize('/nonexistent/directory')
        self.assertIsNone(result)

    def test_load_categories_default(self):
        """Test loading default categories when no config file exists."""
        # Remove any existing categories.json
        if os.path.exists('categories.json'):
            os.remove('categories.json')
        
        categories = organizer.load_categories()
        
        self.assertIsInstance(categories, dict)
        self.assertIn('Images', categories)
        self.assertIn('Documents', categories)
        self.assertIn('Videos', categories)
        self.assertIn('.jpg', categories['Images'])
        self.assertIn('.pdf', categories['Documents'])

    def test_load_categories_from_file(self):
        """Test loading categories from existing config file."""
        test_categories = {
            "TestCategory": [".test", ".example"],
            "Images": [".jpg", ".png"]
        }
        
        with open('categories.json', 'w') as f:
            json.dump(test_categories, f)
        
        categories = organizer.load_categories()
        
        self.assertEqual(categories, test_categories)
        self.assertIn('TestCategory', categories)
        self.assertEqual(categories['TestCategory'], [".test", ".example"])

    def test_load_categories_invalid_json(self):
        """Test loading categories with invalid JSON file."""
        # Create invalid JSON file
        with open('categories.json', 'w') as f:
            f.write('invalid json content {')
        
        # Should return default categories on error
        categories = organizer.load_categories()
        
        self.assertIsInstance(categories, dict)
        self.assertIn('Images', categories)

    @patch('organizer.logging.getLogger')
    def test_list_available_files(self, mock_logger):
        """Test the list_available_files function."""
        # Capture print output
        with patch('builtins.print') as mock_print:
            organizer.list_available_files(self.test_dir)
        
        # Should have printed files
        mock_print.assert_called()
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        
        # Check that some of our test files were mentioned
        output_text = ' '.join(print_calls)
        self.assertTrue(any(filename in output_text for filename in self.test_files))

    @patch('organizer.logging.getLogger')
    @patch('organizer.setup_logging')
    def test_perform_organization_dry_run(self, mock_setup_logging, mock_logger):
        """Test perform_organization in dry run mode."""
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance
        
        categories = {
            'Images': ['.jpg'],
            'Documents': ['.pdf'],
            'Videos': ['.mp4'],
            'Audio': ['.mp3'],
            'Scripts': ['.py'],
            'Archives': ['.zip']
        }
        
        with patch('builtins.print') as mock_print:
            organizer.perform_organization(self.test_dir, is_dry_run=True, categories=categories)
        
        # Should have printed plans without actually moving files
        mock_print.assert_called()
        print_calls = [call[0][0] for call in mock_print.call_args_list]
        output_text = ' '.join(print_calls)
        
        self.assertIn('Plan:', output_text)
        
        # Files should still exist in original location
        for filename in ['document.pdf', 'image.jpg', 'video.mp4']:
            self.assertTrue(os.path.exists(os.path.join(self.test_dir, filename)))

    def test_file_extension_categorization(self):
        """Test that files are categorized correctly by extension."""
        categories = organizer.load_categories()
        
        # Test some known extensions
        test_cases = [
            ('.jpg', 'Images'),
            ('.pdf', 'Documents'),
            ('.mp4', 'Videos'),
            ('.mp3', 'Audio'),
            ('.py', 'Scripts'),
            ('.zip', 'Archives')
        ]
        
        for extension, expected_category in test_cases:
            found_category = None
            for category, extensions in categories.items():
                if extension in extensions:
                    found_category = category
                    break
            
            self.assertEqual(found_category, expected_category, 
                           f"Extension {extension} should be in {expected_category}")

    @patch('organizer.logging.getLogger')
    @patch('organizer.setup_logging')
    def test_get_target_dir_from_user_valid(self, mock_setup_logging, mock_logger):
        """Test get_target_dir_from_user with valid directory."""
        with patch('builtins.input', return_value=self.test_dir):
            result = organizer.get_target_dir_from_user()
        
        self.assertEqual(result, self.test_dir)

    @patch('organizer.logging.getLogger')
    @patch('organizer.setup_logging')
    def test_get_target_dir_from_user_invalid(self, mock_setup_logging, mock_logger):
        """Test get_target_dir_from_user with invalid directory."""
        with patch('builtins.input', return_value='/nonexistent/directory'):
            with patch('builtins.print'):
                result = organizer.get_target_dir_from_user()
        
        self.assertIsNone(result)


class TestConfigurationManagement(unittest.TestCase):
    """Test cases for configuration file management."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir)

    def test_config_file_creation(self):
        """Test that config file is created with default categories."""
        # Ensure no config file exists
        if os.path.exists('categories.json'):
            os.remove('categories.json')
        
        categories = organizer.load_categories()
        
        # Config file should now exist
        self.assertTrue(os.path.exists('categories.json'))
        
        # Verify it's valid JSON
        with open('categories.json', 'r') as f:
            loaded_config = json.load(f)
        
        self.assertEqual(loaded_config, categories)

    def test_custom_category_addition(self):
        """Test adding custom categories to config file."""
        custom_categories = {
            "CustomCategory": [".custom", ".special"],
            "Images": [".jpg", ".png"],
            "Documents": [".pdf", ".doc"]
        }
        
        with open('categories.json', 'w') as f:
            json.dump(custom_categories, f)
        
        loaded_categories = organizer.load_categories()
        
        self.assertIn('CustomCategory', loaded_categories)
        self.assertEqual(loaded_categories['CustomCategory'], [".custom", ".special"])


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)