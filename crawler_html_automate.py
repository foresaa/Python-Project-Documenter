import os
import subprocess

# Folders
markdown_folder = 'output_markdown'  # Folder where markdown files are stored
html_output_folder = 'site_sref/assets'  # Folder where HTML markmap files will be saved

# Ensure the HTML output folder exists
os.makedirs(html_output_folder, exist_ok=True)

# HTML snippet to append to markdown files
html_snippet = """
<a href="/site_sref/assets/{filename}.html" target="_blank">Click here to open the markmap file in a new tab</a>

<iframe src="/site_sref/assets/{filename}.html" width="800" height="600"></iframe>
"""

# Loop through markdown files in the folder
for markdown_file in os.listdir(markdown_folder):
    if markdown_file.endswith(".md"):
        # Get the file name without extension
        file_name_without_extension = os.path.splitext(markdown_file)[0]

        # Path for the markdown file
        markdown_file_path = os.path.join(markdown_folder, markdown_file)

        # Path to save the converted HTML file
        html_file_path = os.path.join(html_output_folder, f"{file_name_without_extension}.html")

        # Convert markdown to Markmap HTML using markmap-cli
        subprocess.run([
            r"C:\Users\User\AppData\Roaming\npm\markmap.cmd", 
            "auto", 
            markdown_file_path, 
            "-o", 
            html_file_path
        ])

        print(f"Converted {markdown_file} to {html_file_path}")

        # Append the HTML snippet to the markdown file
        with open(markdown_file_path, 'a', encoding='utf-8') as md_file:
            md_file.write("\n\n")
            md_file.write(html_snippet.format(filename=file_name_without_extension))

        print(f"Updated {markdown_file} with embedded HTML.")

print("All markdown files have been processed and updated with Markmap HTML.")
