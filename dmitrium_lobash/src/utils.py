import json
from pathlib import Path


current_dir = Path(__file__)
root = current_dir.parent.parent
database = root / 'glasses.json'

def save_data_to_json(data):
    with open(database, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"JSON saved {database}")
