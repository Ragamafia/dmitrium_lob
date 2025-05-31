import json
import os


def save_dict_to_json(data, filename='glasses.json'):
    filepath = os.path.join(os.getcwd(), filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"JSON saved {filepath}")
