# **Project Documentation Extractor**

This repository contains a Python-based project for automatically extracting and documenting Python code files. It converts Python code to Markdown, integrates Markmap visualizations, and configures MkDocs for presenting documentation in a structured, user-friendly format.

_Features_

Automated Python Documentation: A Python script crawler.py converts all Python files into Markdown with rich documentation.
Markmap Integration: The script generates interactive Markmap mind maps for each file, embedded in the generated Markdown files.
MkDocs: The project is configured with MkDocs to easily navigate and present the extracted documentation.
Workflow Overview
Crawler Script:

The script crawler.py extracts information from each Python file (functions, classes, decorators, variables) and generates corresponding markdown files.
These markdown files are saved in an output_markdown folder.

## Markmap Integration:

The script also creates Markmap HTML files for each markdown file.
These Markmap HTML files are then embedded into the markdown files using html tags for interactive visualization.

## MkDocs Configuration:

The generated markdown files are added to MkDocs configuration.
MkDocs is used to generate a clean and structured documentation website.

Installation

Ensure you have Python 3.6+ installed. Install MkDocs and the necessary dependencies:

pip install mkdocs mkdocs-material markmap-lib

## Run the Crawler Script:

Execute crawler.py to generate the documentation in the output_markdown folder:

python crawler.py

## Generate Markmap Visualizations:

The Markmap visualizations for each file are automatically embedded in the markdown files through html tags.
Ensure the assets folder is populated with the corresponding .html files.

## Build the MkDocs Site:

** MkDocs Ssite here
https://andelprojects.co.uk/site_sref/

Once all markdown files are generated and the mkdocs.yml file is configured, you can serve the documentation site locally
using MkDocs:
mkdocs serve

If you want to deploy your documentation to GitHub Pages:

mkdocs gh-deploy

## Usage

The crawler.py script can be modified or extended to suit other Python projects.
The generated markdown files will be available in the output_markdown/ directory, and Markmap HTML files will be placed in assets folder

All files are accessible through MkDocs for easy navigation and browsing.

## Contributing

Feel free to submit issues, fork the repository, and make pull requests. Contributions to improve the documentation or the Python crawler script are always welcome!

## License

This project is licensed under the MIT License.
