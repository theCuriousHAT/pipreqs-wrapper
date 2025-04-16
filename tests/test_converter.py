import pytest
import os
from pipreqs_wrapper.converter import process_ipynb_files

# Test to check if the `process_ipynb_files` function is accessible and callable
def test_process_ipynb_files():
    # Set up a test directory where .ipynb files are located
    test_dir = os.path.join(os.path.dirname(__file__), 'test_notebooks')
    os.makedirs(test_dir, exist_ok=True)

    # Create a sample .ipynb file with code (to simulate a real notebook)
    test_notebook_path = os.path.join(test_dir, 'test_notebook.ipynb')
    notebook_content = """
    {
     "cells": [
      {
       "cell_type": "code",
       "execution_count": null,
       "id": "dbf00e9b",
       "metadata": {},
       "outputs": [],
       "source": [
        "import numpy as np\\n",
        "import pandas as pd\\n",
        "a = np.array([1, 2, 3])\\n",
        "b = pd.Series([1, 2, 3])\\n"
       ]
      }
     ],
     "metadata": {},
     "nbformat": 4,
     "nbformat_minor": 2
    }
    """
    with open(test_notebook_path, 'w') as f:
        f.write(notebook_content)

    # Call the function from your pipreqs_wrapper to process the notebook
    result = process_ipynb_files(test_dir)

    # Test if the function runs without errors
    assert result is not None, "The result should not be None"

    # Check if the .py file is created
    expected_py_file = os.path.join(test_dir, 'test_notebook.py')
    assert os.path.exists(expected_py_file), f"Expected .py file {expected_py_file} not created"

    # Optional: Check if the .py file contains the correct imports
    with open(expected_py_file, 'r') as f:
        python_code = f.read()
        assert 'import numpy as np' in python_code, "Expected import numpy as np"
        assert 'import pandas as pd' in python_code, "Expected import pandas as pd"

    # Clean up after the test
    os.remove(test_notebook_path)
    os.remove(expected_py_file)
    os.rmdir(test_dir)
