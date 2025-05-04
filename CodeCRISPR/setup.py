from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="codecrispr",
    version="0.1.0",
    author="David Burgess",
    author_email="david.burgess@usask.ca",
    description="Precision code editing at the function level",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ssegrubdivad/CodeCRISPR",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "codecrispr=CodeCRISPR.codecrispr:main",
        ],
    },
)