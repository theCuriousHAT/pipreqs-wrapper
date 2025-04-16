import os
import subprocess
import logging
from nbconvert import PythonExporter
import nbformat
import argparse


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def convert_ipynb_to_py(ipynb_path):
    """Converts a .ipynb notebook to a .py file."""
    try:
        with open(ipynb_path, 'r', encoding='utf-8') as f:
            nb_node = nbformat.read(f, as_version=4)

        py_exporter = PythonExporter()
        body, _ = py_exporter.from_notebook_node(nb_node)

        py_path = ipynb_path.replace('.ipynb', '.py')
        with open(py_path, 'w', encoding='utf-8') as f:
            f.write(body)

        logging.info(f"Converted: {ipynb_path} -> {py_path}")
        return py_path
    except Exception as e:
        logging.error(f"Failed to convert {ipynb_path}: {e}")
        return None


def run_pipreqs(target_dir):
    """Runs pipreqs to generate requirements.txt from .py files."""
    try:
        subprocess.run(['pipreqs', target_dir, '--force'], check=True)
        logging.info(f"pipreqs successfully generated requirements.txt in {target_dir}")
    except subprocess.CalledProcessError as e:
        logging.error(f"pipreqs failed: {e}")


def process_ipynb_files(root_dir, keep_py=False):
    """
    Walks through folders, converts .ipynb to .py, runs pipreqs, and cleans up.

    Args:
        root_dir (str): Directory to scan for .ipynb files.
        keep_py (bool): Whether to retain the generated .py files.

    Returns:
        bool: True if pipreqs ran successfully, False otherwise.
    """
    generated_py_files = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.ipynb') and '-checkpoint' not in filename:
                ipynb_path = os.path.join(dirpath, filename)
                py_path = convert_ipynb_to_py(ipynb_path)
                if py_path:
                    generated_py_files.append(py_path)

    if not generated_py_files:
        logging.warning("No valid .ipynb files found to convert.")
        return False

    run_pipreqs(root_dir)

    if not keep_py:
        for py_file in generated_py_files:
            try:
                os.remove(py_file)
                logging.info(f"Deleted temporary file: {py_file}")
            except Exception as e:
                logging.warning(f"Could not delete {py_file}: {e}")
    else:
        logging.info("Temporary .py files retained.")

    return True


def main():
    parser = argparse.ArgumentParser(description="Extract requirements from .ipynb files using pipreqs.")
    parser.add_argument("path", help="Root directory to search for .ipynb files.")
    parser.add_argument("--keep", action="store_true", help="Keep the generated .py files.")
    args = parser.parse_args()

    success = process_ipynb_files(args.path, keep_py=args.keep)
    if success:
        logging.info("Requirements extraction completed successfully.")
    else:
        logging.info("No requirements were extracted.")


if __name__ == "__main__":
    main()
