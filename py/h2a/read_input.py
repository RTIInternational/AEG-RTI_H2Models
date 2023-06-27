import os
import sys
import json
from .util import root_dir


# Function that reads data/input/default/default-smr-natural-gas-no-cc.json and returns a dictionary {[input_name:str]: input_value}
def read_inputs_json(json_file):
    default_inputs = {}
    filepath = os.path.join(root_dir, "data", "input", "default", json_file)

    # Throw error if file doesn't exist
    if not os.path.isfile(filepath):
        # Print all files in data/input/default
        print(f"\nError: File `{json_file}` not found.")
        print("\nInput files that do exist:\n")
        for filename in os.listdir(os.path.join(root_dir, "data", "input", "default")):
            if filename != "input.schema.json":
                print("  ", filename)
        print()
        sys.exit(1)

    with open(
        filepath, newline=""
    ) as jsonfile:
        data = json.load(jsonfile)
        for key, value in data.items():
            default_inputs[key] = value
    return default_inputs

# Used by check_formulas.py to get excel_locations
def read_formulas_json():
    with open(
        os.path.join(root_dir, "data", "formula", "formulas.json"), newline=""
    ) as jsonfile:
        try:
            loaded_json = json.load(jsonfile)
            return loaded_json["formulas"]
        except json.decoder.JSONDecodeError as e:
            print("invalid json: %s" % e)
            print(f"File: {jsonfile}")
            raise