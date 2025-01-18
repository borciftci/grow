import json
import os


def read(path):
    with open(path, 'r') as f:
        return f.read()


def read_json(path):
    # Get the absolute path of the JSON file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, path)
    return json.loads(read(full_path))


NOTE_MAP = read_json('frequency_map.json')
