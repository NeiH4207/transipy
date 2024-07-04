import os
import sys
import pytest
from unittest.mock import patch

# Add the parent directory to the Python path to import the main script
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transipy import main  # Replace with your actual main script name

@pytest.fixture
def sample_csv_path():
    return os.path.join('samples', 'sample.csv')

@patch('argparse.ArgumentParser.parse_args')
def test_main_with_sample_csv(mock_args, sample_csv_path):
    # Mock the command line arguments
    mock_args.return_value = type('Args', (), {
        'file_path': sample_csv_path,
        'sep': ',',
        'source': 'en',
        'target': 'vi',
        'chunk_size': 1,
        'output_file': None,
        'dictionary': None,
        'column': None,
        'skip': None,
        'sheet': None
    })()

    # Call the main function
    main()

    # Assert that the output file was created
    assert os.path.exists('examples/sample_en_vi.csv')

    # You can add more assertions here to check the content of the output file