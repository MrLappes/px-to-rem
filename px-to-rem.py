import os
import re
import argparse
from tqdm import tqdm

def convert_units(file_path, base_size=16, revert=False):
    """
    Converts all px units to rem or all rem units to px in a given file, depending on the revert flag.
    """
    replacements = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        if revert:
            # Regex to find all rem values (including negative values) that are followed by a semicolon, a closing parenthesis, or a space
            pattern = r'(-?\d+\.?\d*)rem(?=[\s;)]|$)'
            def repl(match):
                nonlocal replacements
                replacements += 1
                return f'{int(float(match.group(1)) * base_size)}px'
        else:
            # Regex to find all px values (including negative values) that are followed by a semicolon, a closing parenthesis, or a space
            pattern = r'(-?\d+)px(?=[\s;)]|$)'
            def repl(match):
                nonlocal replacements
                replacements += 1
                return f'{int(match.group(1)) / base_size}rem'

        content_new = re.sub(pattern, repl, content)

        # Write the changes back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content_new)
    except PermissionError:
        print(f"Skipping {file_path} due to insufficient permissions.")
    return replacements


def find_files(directory, subfolder, extension, ignore_folders, ignore_files):
    """
    Finds all files with a given extension in a directory.
    If subfolder is True, search is recursive.
    Ignores files and folders specified in ignore_files and ignore_folders.
    """
    pattern = f'.*\\.{extension}'
    if subfolder:
        for root, dirs, files in os.walk(directory):
            if any(ignore_folder in root for ignore_folder in ignore_folders):
                continue
            for file in files:
                if re.match(pattern, file) and file not in ignore_files:
                    yield os.path.join(root, file)
    else:
        for file in os.listdir(directory):
            if re.match(pattern, file) and file not in ignore_files:
                yield os.path.join(directory, file)

def main(directory, base_size, subfolder, css, revert, ignore_folders, ignore_files):
    file_extension = 'css' if css else 'scss'
    files = list(find_files(directory, subfolder, file_extension, ignore_folders, ignore_files))
    total_replacements = 0
    for file_path in tqdm(files, desc="Converting files"):
        total_replacements += convert_units(file_path, base_size, revert)
    if revert:
        print(f"Changed {total_replacements} occurrences. Your code has been px-ified!")
    else:
        print(f"Changed {total_replacements} occurrences. Your code has been rem-ified!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert PX to REM in CSS or SCSS files.')
    parser.add_argument('directory', type=str, help='Directory containing CSS or SCSS files to convert.')
    parser.add_argument('--base', type=int, default=16, help='Base pixel size for REM conversion. Default is 16.')
    parser.add_argument('--subfolder', action='store_true', help='Set this flag to search in subfolders.')
    parser.add_argument('--css', action='store_true', help='Set this flag to convert CSS files instead of SCSS files.')
    parser.add_argument('--revert', action='store_true', help='Set this flag to convert REM values back to PX.')
    parser.add_argument('--ignore-folder', nargs='*', default=[], help='List of folder paths to ignore.')
    parser.add_argument('--ignore-file', nargs='*', default=[], help='List of file names to ignore.')
    args = parser.parse_args()

    main(args.directory, args.base, args.subfolder, args.css, args.revert, args.ignore_folder, args.ignore_file)
