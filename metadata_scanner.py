import os
import hashlib
import json
from datetime import datetime
import mimetypes

def calculate_hash(file_path, algorithm='sha256'):
    """Calculate the hash of a file."""
    hash_func = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):  # Read the file in chunks
            hash_func.update(chunk)
    return hash_func.hexdigest()

def get_file_metadata(file_path):
    """Extract metadata of a single file."""
    stats = os.stat(file_path)
    metadata = {
        "file_name": os.path.basename(file_path),
        "file_path": file_path,
        "file_size": stats.st_size,
        "created_time": datetime.fromtimestamp(stats.st_ctime).isoformat(),
        "modified_time": datetime.fromtimestamp(stats.st_mtime).isoformat(),
        "file_type": mimetypes.guess_type(file_path)[0],
        "hash_sha256": calculate_hash(file_path),
    }
    return metadata

def scan_directory(directory):
    """Scan all files in a directory and collect their metadata."""
    metadata_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                metadata_list.append(get_file_metadata(file_path))
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    return metadata_list

def save_to_json(data, output_file):
    """Save the metadata list to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    print("Metadata Scanner")
    folder_path = input("Enter the folder path to scan: ").strip()
    output_file = input("Enter the output JSON file name (e.g., output.json): ").strip()

    if not os.path.isdir(folder_path):
        print("The specified folder path does not exist.")
    else:
        print("Scanning files...")
        metadata = scan_directory(folder_path)
        save_to_json(metadata, output_file)
        print(f"Metadata saved to {output_file}")