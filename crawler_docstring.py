import os

def add_docstrings_to_file(input_file, output_file):
    """Adds docstrings to the input Python file and saves it as output_file."""
    with open(input_file, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    with open(output_file, "w", encoding="utf-8") as outfile:
        for line in lines:
            # Add docstrings where needed
            if "def is_file_empty" in line:
                outfile.write(line)
                outfile.write('    """\n    Check if a file is empty by reading its content and removing whitespace.\n    Returns True if the file is empty or contains only comments.\n    """\n')
            elif "def get_node_source_code" in line:
                outfile.write(line)
                outfile.write('    """\n    Get the full source code of an AST node by reading the file\'s lines.\n    This function helps to extract the code for specific nodes such as functions or classes.\n    """\n')
            elif "def get_decorators" in line:
                outfile.write(line)
                outfile.write('    """\n    Extract decorators from a function or class definition node in the AST.\n    Returns a list of the decorators applied to the node.\n    """\n')
            elif "def parse_python_file" in line:
                outfile.write(line)
                outfile.write('    """\n    Parse a Python file using AST (Abstract Syntax Tree).\n    Extracts imports, functions, classes, variables/constants, and their docstrings or decorators.\n    Returns imports, functions, classes, variables, and file-level docstring.\n    """\n')
            elif "def process_directory" in line:
                outfile.write(line)
                outfile.write('    """\n    Process the entire directory tree starting from `root_dir`.\n    For each Python file found, extract information and save as markdown in the output directory.\n    """\n')
            elif "if __name__" in line:
                outfile.write(line)
                outfile.write('    """\n    Main entry point of the script.\n    Sets the correct root directory for the app and starts processing the files.\n    """\n')
            else:
                outfile.write(line)

    print(f"Docstrings added and saved to {output_file}")

def convert_to_markdown(input_file, markdown_file):
    """Converts the Python file with docstrings to markdown format and saves it."""
    with open(input_file, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    with open(markdown_file, "w", encoding="utf-8") as mdfile:
        mdfile.write(f"# Documentation for {input_file}\n\n")
        mdfile.write("```python\n")
        for line in lines:
            mdfile.write(line)
        mdfile.write("```\n")

    print(f"Converted {input_file} to markdown and saved to {markdown_file}")

# File paths
input_file = "crawler.py"  # Change this to the correct path of your original script
output_file = "crawler_documented.py"
markdown_file = "crawler_docstrings.md"

# Add docstrings
add_docstrings_to_file(input_file, output_file)

# Convert to markdown
convert_to_markdown(output_file, markdown_file)
