import os
import json
from .util import root_dir


def read_inputs_json():
    with open(
        os.path.join(root_dir, "data/input/default/default-smr-natural-gas-no-cc.json"),
        newline="",
    ) as jsonfile:
        return json.load(jsonfile)


def read_formulas_json():
    with open(
        os.path.join(root_dir, "data/formula/formulas.json"), newline=""
    ) as jsonfile:
        try:
            loaded_json = json.load(jsonfile)
            return loaded_json
        except json.decoder.JSONDecodeError as e:
            print("invalid json: %s" % e)
            print(f"File: {jsonfile}")
            raise


def read_globals_json():
    with open(
        os.path.join(root_dir, "data/formula/globals.json"), newline=""
    ) as jsonfile:
        return json.load(jsonfile)


# JSON file containing function definitions
def read_functions_json():
    # all_functions is a list of tuples (filename, [functions])
    all_functions = []
    for filename in os.listdir(os.path.join(root_dir, "data/formula/lib")):
        with open(
            os.path.join(root_dir, "data/formula/lib", filename), newline=""
        ) as jsonfile:
            try:
                loaded_json = json.load(jsonfile)
                file_functions_json = loaded_json["functions"]
                key = filename.split(".")[0]
                all_functions.append((key, file_functions_json))
            except json.decoder.JSONDecodeError as e:
                print("invalid json: %s" % e)
                print(f"File: {jsonfile}")
                raise
    return all_functions
