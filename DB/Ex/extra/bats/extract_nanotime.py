import os
import re

# python ./extract_nanotime.py

folder = "../png_output"  # Change to your relative or absolute path

# Get only .png files in the folder
files = [f for f in os.listdir(folder) if f.endswith(".png")]

# Extract the trailing nanotime from the filename
def extract_nanotime(filename):
    match = re.search(r"_(\d+)\.png$", filename)
    return int(match.group(1)) if match else -1

# Filter out invalid files and sort by nanotime
files = [(f, extract_nanotime(f)) for f in files if extract_nanotime(f) != -1]
files.sort(key=lambda x: x[1])  # Sort by extracted nanotime

# Rename to frame0000.png, frame0001.png, ...
for idx, (original, _) in enumerate(files):
    new_name = f"frame{idx:04d}.png"
    src = os.path.join(folder, original)
    dst = os.path.join(folder, new_name)
    os.rename(src, dst)
    print(f"Renamed: {original} -> {new_name}")
