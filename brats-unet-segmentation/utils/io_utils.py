import os
import json
from typing import Dict, Any

import torch


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def save_checkpoint(state: Dict[str, Any], filename: str):
    torch.save(state, filename)


def load_checkpoint(filename: str, map_location=None):
    return torch.load(filename, map_location=map_location)


def save_json(obj: Dict[str, Any], path: str):
    with open(path, "w") as f:
        json.dump(obj, f, indent=4)


def load_json(path: str) -> Dict[str, Any]:
    with open(path) as f:
        return json.load(f)
