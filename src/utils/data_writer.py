import csv
import json
from typing import List, Dict

def write_data(data: List[Dict], filename: str, format: str):
    if format.lower() == 'csv':
        write_to_csv(data, f"{filename}.csv")
    elif format.lower() == 'json':
        write_to_json(data, f"{filename}.json")
    else:
        raise ValueError(f"Unsupported format: {format}")

def write_to_csv(data: List[Dict], filename: str):
    if not data:
        raise ValueError("No data to write")

    # Get all unique keys from all dictionaries
    fieldnames = set()
    for item in data:
        fieldnames.update(item.keys())
    fieldnames = sorted(fieldnames)  # Sort field names for consistency

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            # Fill in missing fields with None
            row_data = {field: row.get(field, None) for field in fieldnames}
            writer.writerow(row_data)

def write_to_json(data: List[Dict], filename: str):
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2, ensure_ascii=False)