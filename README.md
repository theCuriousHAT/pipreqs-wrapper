# pipreqs-wrapper

`pipreqs-wrapper` is a Python module that helps convert `.ipynb` (Jupyter notebook) files into `.py` (Python script) files and then extracts the required packages and their versions using `pipreqs`. Optionally, it can delete the generated `.py` files after extracting the requirements.

## Features
- Recursively converts `.ipynb` files to `.py` files.
- Runs `pipreqs` to extract package dependencies.
- Optionally deletes temporary `.py` files after extracting dependencies.

