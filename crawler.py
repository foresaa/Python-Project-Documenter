import os
import ast

# Function to check if a file is empty (ignoring comments and whitespace)
def is_file_empty(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read().strip()
        return len(content) == 0 or all(line.startswith('#') for line in content.splitlines())

# Function to get the full source code of a node by reading the file's lines
def get_node_source_code(file_path, node):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    start_line = node.lineno - 1  # AST line numbers are 1-indexed
    end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
    return ''.join(lines[start_line:end_line])

# Function to extract decorators from functions or classes
def get_decorators(node):
    decorators = []
    if hasattr(node, 'decorator_list'):
        for decorator in node.decorator_list:
            decorators.append(ast.unparse(decorator) if hasattr(ast, 'unparse') else str(decorator))
    return decorators

# Function to parse a Python file and extract imports, functions, classes, decorators, and variables/constants
def parse_python_file(file_path, app_root):
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=file_path)
    
    imports = []
    functions = []
    classes = []
    variables = []
    file_docstring = None  # Capture file-level docstring if applicable
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                import_statement = f"import {alias.name}"
                if import_statement.startswith(f"import {app_root}"):
                    import_statement = f'<font color="red">{import_statement}</font>'
                imports.append(import_statement)
        elif isinstance(node, ast.ImportFrom):
            module = node.module if node.module else ''
            import_statement = f"from {module} import {', '.join(alias.name for alias in node.names)}"
            if import_statement.startswith(f"from {app_root}"):
                import_statement = f'<font color="red">{import_statement}</font>'
            imports.append(import_statement)
        elif isinstance(node, ast.FunctionDef):
            decorators = get_decorators(node)
            functions.append({
                'name': node.name,
                'start_line': node.lineno,
                'docstring': ast.get_docstring(node),
                'decorators': decorators,
                'code': get_node_source_code(file_path, node)
            })
        elif isinstance(node, ast.ClassDef):
            decorators = get_decorators(node)
            classes.append({
                'name': node.name,
                'start_line': node.lineno,
                'docstring': ast.get_docstring(node),
                'decorators': decorators,
                'code': get_node_source_code(file_path, node)
            })
        elif isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            # Capture module-level variables/constants
            var_name = node.targets[0].id
            var_value = ast.get_source_segment(open(file_path).read(), node)
            variables.append({
                'name': var_name,
                'value': var_value
            })
    
    return imports, functions, classes, variables, file_docstring

# Function to process the entire directory tree and create markdown files in output_markdown
def process_directory(root_dir):
    app_root = os.path.basename(root_dir)  # Get the root folder name (e.g., 'app')
    output_dir = "output_markdown"  # Specify the output directory for markdown files
    os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

    print(f"Processing root directory: {root_dir}")
    print(f"Markdown files will be saved in: {os.path.abspath(output_dir)}")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Ignore __pycache__ directories
        dirnames[:] = [d for d in dirnames if not d.endswith('__pycache__')]  
        
        # Normalize the path and replace backslashes with forward slashes
        dirpath_normalized = os.path.normpath(dirpath).replace("\\", "/")

        # Handle Python files in each directory (including the root)
        filenames = [f for f in filenames if f.endswith(".py") and not is_file_empty(os.path.join(dirpath, f)) and f != '__init__.py']
        filenames.sort()

        if filenames:
            # Create a markdown file for the directory (name based on directory path)
            output_file = os.path.join(output_dir, f"{os.path.basename(dirpath)}.md")
            print(f"Creating markdown file: {output_file}")

            documentation = f"# Directory: `{dirpath_normalized}`\n\n"
        
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                imports, functions, classes, variables, file_docstring = parse_python_file(file_path, app_root)
                
                documentation += f"## File: `{filename}`\n\n"
                if file_docstring:
                    documentation += f"**File Docstring:**\n```\n{file_docstring}\n```\n"
                
                if imports:
                    documentation += "### Imports:\n"
                    for imp in imports:
                        documentation += f"- {imp}\n"
                
                if functions:
                    documentation += "### Functions:\n"
                    for func in functions:
                        documentation += f"- **Function:** `{func['name']}` (line {func['start_line']})\n"
                        if func['decorators']:
                            documentation += f"  **Decorators:**\n  ```\n  {' '.join(func['decorators'])}\n  ```\n"
                        if func['docstring']:
                            documentation += f"  **Docstring:**\n  ```\n  {func['docstring']}\n  ```\n"
                        documentation += "  ```python\n"
                        documentation += f"  {func['code']}\n"
                        documentation += "  ```\n"
                
                if classes:
                    documentation += "### Classes:\n"
                    for cls in classes:
                        documentation += f"- **Class:** `{cls['name']}` (line {cls['start_line']})\n"
                        if cls['decorators']:
                            documentation += f"  **Decorators:**\n  ```\n  {' '.join(cls['decorators'])}\n  ```\n"
                        if cls['docstring']:
                            documentation += f"  **Docstring:**\n  ```\n  {cls['docstring']}\n  ```\n"
                        documentation += "  ```python\n"
                        documentation += f"  {cls['code']}\n"
                        documentation += "  ```\n"

                if variables:
                    documentation += "### Variables/Constants:\n"
                    for var in variables:
                        documentation += f"  ```python\n  {var['value']}\n  ```\n"
            
            # Write to markdown file in the output directory
            with open(output_file, "w", encoding="utf-8") as file:
                file.write(documentation)
        else:
            print(f"No Python files found in {dirpath}, skipping.")

# Main entry point
if __name__ == "__main__":
    # Set the correct root directory for app
    root_directory = "C:/MJ6_SREF/app"  # Update this path to the correct app folder
    process_directory(root_directory)
    print(f"Documentation for each directory created.")
