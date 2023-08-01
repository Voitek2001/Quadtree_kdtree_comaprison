import json

def dump_as_json(obj, filepath):
    with open(filepath, 'w') as f:
        json.dump(obj, f)


def load_from_json(filepath):
    with open(filepath, 'r') as f:
        obj = json.load(f)
    return obj