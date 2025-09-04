import os

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get all files in the current directory and remove number.
for filename in os.listdir(current_dir):
    # Only process files (not directories)
    file_path = os.path.join(current_dir, filename)
    if os.path.isfile(file_path):
        # Split filename and extension
        name, ext = os.path.splitext(filename)
        # Remove leading numbers and optional separators (space, dash, underscore)
        new_name = name.lstrip("0123456789").lstrip(".")
        # Only rename if the name has changed
        if new_name != name and new_name:
            new_filename = new_name + ext
            new_file_path = os.path.join(current_dir, new_filename)
            # Avoid overwriting existing files
            if not os.path.exists(new_file_path):
                os.rename(file_path, new_file_path)
