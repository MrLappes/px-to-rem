# PX to REM Converter

This Python script is designed to convert all pixel (px) units to relative (rem) units in CSS or SCSS files, and vice versa. It can be used to make your CSS more responsive and scalable.

## Features

- Convert all px units to rem units in a given file.
- Convert all rem units back to px units.
- Search for files in subfolders.
- Ignore specific files and folders.
- Specify the base pixel size for rem conversion.

## Usage

You can run the script from the command line with the following arguments:

- `directory`: The directory containing the CSS or SCSS files to convert.
- `--base`: The base pixel size for rem conversion. Default is 16.
- `--subfolder`: Set this flag to search in subfolders.
- `--css`: Set this flag to convert CSS files instead of SCSS files.
- `--revert`: Set this flag to convert rem values back to px.
- `--ignore-folder`: List of folder paths to ignore.
- `--ignore-file`: List of file names to ignore.

## Example usage:
```python
python px-to-rem.py ./my-css-directory --base 16 --subfolder --css --revert --ignore-folder ./ignore-this-folder --ignore-file ignore-this-file.css
```

This will convert all rem units back to px units in all CSS files in ./my-css-directory and its subfolders, except for the files in ./ignore-this-folder and the file named ignore-this-file.css.

## Requirements
This script requires Python 3 and the tqdm library for displaying progress. You can install tqdm with pip:

```python
pip install tqdm
```

## Disclaimer
Please make sure to backup your files before running this script, as it will overwrite the original files.