import argparse
from pipreqs_wrapper.converter import process_ipynb_files

def main():
    parser = argparse.ArgumentParser(description="Extract requirements from .ipynb files using pipreqs.")
    parser.add_argument("--path", required=True, help="Root directory to search for .ipynb files.")
    parser.add_argument("--keep", action="store_true", help="Keep the generated .py files.")
    args = parser.parse_args()

    process_ipynb_files(args.path, keep_py=args.keep)

if __name__ == "__main__":
    main()
