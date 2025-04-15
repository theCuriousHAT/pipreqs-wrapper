import os
import subprocess
import tempfile
from nbconvert import PythonExporter
import nbformat
import argparse


def convert_ipynb_to_py(ipynb_path):
    """Converts a .ipynb notebook to a .py file."""
    try:
        with open(ipynb_path, 'r', encoding='utf-8') as f:
            nb_node = nbformat.read(f, as_version=4)
        py_exporter = PythonExporter()
        (body, _) = py_exporter.from_notebook_node(nb_node)

        py_path = ipynb_path.replace('.ipynb', '.py')
        with open(py_path, 'w', encoding='utf-8') as f:
            f.write(body)

        return py_path
    except Exception as e:
        print(f"[Error] Failed to convert {ipynb_path}: {e}")
        return None


def run_pipreqs(target_dir):
    """Runs pipreqs to generate requirements.txt from .py files."""
    try:
        subprocess.run(['pipreqs', target_dir, '--force'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[Error] pipreqs failed: {e}")


def process_ipynb_files(root_dir, keep_py=False):
    """Main function to walk through folders, convert .ipynb to .py, run pipreqs, and clean up."""
    generated_py_files = []

    for foldername, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.ipynb') and '-checkpoint' not in filename:
                ipynb_path = os.path.join(foldername, filename)
                py_path = convert_ipynb_to_py(ipynb_path)
                if py_path:
                    generated_py_files.append(py_path)

    if generated_py_files:
        run_pipreqs(root_dir)

        if not keep_py:
            for py_file in generated_py_files:
                try:
                    os.remove(py_file)
                except Exception as e:
                    print(f"[Warning] Could not delete {py_file}: {e}")
            print("Temporary .py files deleted.")
        else:
            print("Temporary .py files kept.")
    else:
        print("No valid .ipynb files found to convert.")


def main():
    parser = argparse.ArgumentParser(description="Extract requirements from .ipynb files using pipreqs.")
    parser.add_argument("path", help="Root directory to search for .ipynb files.")
    parser.add_argument("--keep", action="store_true", help="Keep the generated .py files.")
    args = parser.parse_args()

    process_ipynb_files(args.path, keep_py=args.keep)


if __name__ == "__main__":
    main()
