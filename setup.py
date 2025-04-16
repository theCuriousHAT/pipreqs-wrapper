# setup.py

from setuptools import setup, find_packages

setup(
    name="pipreqs-wrapper",  # Your package name
    version="0.1.0",  # Your package version
    description="A Python module to convert .ipynb files to .py and extract requirements using pipreqs.",
    long_description=open("README.md").read(),  # Content from your README file
    long_description_content_type="text/markdown",
    author="Ajay Singh Rawat",
    author_email="ajaysinghrawat.95@gmail.com",
    url="https://github.com/yourusername/pipreqs-wrapper",  # Replace with your GitHub link
    packages=find_packages(),  # Automatically find your package
    install_requires=[  # List dependencies here
        "pipreqs",
        "nbconvert",
        "nbformat",
        'nbconvert[extra]',
    ],
    entry_points={
    'console_scripts': [
    'pipreqs-wrapper=pipreqs_wrapper.converter:main',  # Update this path based on your structure
        ],
    },
    classifiers=[  # Classifiers are optional but help others find your package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Python version compatibility
)
