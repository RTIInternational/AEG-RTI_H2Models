import os
import json
from .util import root_dir


# Function that reads data/input/default/default-smr-natural-gas-no-cc.json and returns a dictionary {[input_name:str]: input_value}
def read_inputs_json(json_file):
    default_inputs = {}
    with open(
        os.path.join(root_dir, "data", "input", "default", json_file), newline=""
    ) as jsonfile:
        data = json.load(jsonfile)
        for key, value in data.items():
            default_inputs[key] = value
    return default_inputs
