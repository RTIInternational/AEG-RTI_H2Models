# Read JSON file containing function definitions and write a Python file containing the functions

import json
import os
import subprocess
import sys
from h2a.util import root_dir

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "h2a")

# Get project root directory
TOP_LINE_COMMENT = """#
# This file is programmatically generated by py_writer.py; do not edit
#
"""


def read_inputs_json():
    with open(
        os.path.join(root_dir, "data/input/default/default-smr-natural-gas-no-cc.json"),
        newline="",
    ) as jsonfile:
        return json.load(jsonfile)


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
            file_functions_json = json.load(jsonfile)["functions"]
            key = filename.split(".")[0]
            all_functions.append((key, file_functions_json))
    return all_functions


def read_formulas_json():
    with open(
        os.path.join(root_dir, "data/formula/formulas.json"), newline=""
    ) as jsonfile:
        return json.load(jsonfile)


def globals_to_python():
    global_formulas = read_globals_json()["globals"]
    file_str = TOP_LINE_COMMENT
    file_str += "from h2a.ref_tables import *\n"
    file_str += "from h2a.inputs import *\n"

    file_str += "\n"

    for formula in global_formulas:
        name = (
            formula["name"]
            if "name" in formula and formula["name"] != ""
            else formula["orig_name"]
        )
        formula_def_str = f"{name} = "
        formula_def_str += f"{formula['expression']}\n"
        file_str += formula_def_str
    with open(os.path.join(output_dir, "globals.py"), "w") as pyfile:
        pyfile.write(file_str)


def inputs_to_python():
    inputs = read_inputs_json()
    file_str = TOP_LINE_COMMENT
    file_str += "from h2a.read_input import user_input\n\n"

    for key in inputs:
        if key == "$schema":
            continue
        file_str += f"{key} = user_input['{key}']\n"
    with open(os.path.join(output_dir, "inputs.py"), "w") as pyfile:
        pyfile.write(file_str)


def helpers_to_python():
    file_str = TOP_LINE_COMMENT

    # get() is a helper function to access a dictionary
    file_str += "def get(obj, key):\n    return obj[key]\n\n"

    # concat() is a helper function to concatenate strings
    file_str += "def concat(a, b):\n    return a + b\n\n"

    # split() is a helper function to split a string
    file_str += "def split(a, b):\n    return a.split(b)\n\n"

    # seq_along() is a helper function to get a sequence of integers
    file_str += "def seq_along(a):\n    return range(len(a))\n\n"

    # R note: helper: range <- seq
    # R note: helper: len <- length

    file_str += "TRUE = True"

    with open(os.path.join(output_dir, "helpers.py"), "w") as pyfile:
        pyfile.write(file_str)


def functions_to_python():
    all_functions = read_functions_json()
    for filename, functions in all_functions:
        file_str = TOP_LINE_COMMENT
        file_str += "from h2a.ref_tables import *\n"
        file_str += "from h2a.helpers import *\n"
        file_str += "from h2a.globals import *\n\n"

        for func in functions:
            func_def_str = f"def {func['name']}("
            if "args" in func:
                func_def_str += ", ".join(func["args"])
            if "extra_args" in func:
                func_def_str += ", "
                func_def_str += ", ".join(func["extra_args"])
            func_def_str += "):\n"
            if "description" in func:
                func_def_str += f'    """{func["description"]}"""\n'
            if "body" in func:
                func_def_str += f"    return {func['body']}\n\n"
            elif "type" in func:
                if func["type"] == "switch":
                    cond1 = func["cases"][0]["condition"]
                    body1 = func["cases"][0]["body"]
                    func_def_str += f"    if {cond1}:\n"
                    func_def_str += f"        return {body1}\n"
                    for case in func["cases"][1:]:
                        cond = case["condition"]
                        body = case["body"]
                        func_def_str += f"    elif {cond}:\n"
                        func_def_str += f"        return {body}\n"
            elif "map_function" in func:
                # lambda_args_str is the list of arguments for the lambda function, using the list func["map_item_names"]
                lambda_args_str = (
                    func["lambda_args_str"]
                    if "lambda_args_str" in func
                    else ", ".join(func["map_item_names"])
                )
                map_args_str = (
                    func["map_args_str"]
                    if "map_args_str" in func
                    else ", ".join(func["map_iterables"])
                )
                # extra_arg_list is func["args"] without func["map_iterables"]
                extra_arg_list = [
                    arg for arg in func["args"] if arg not in func["map_iterables"]
                ]
                extra_args_str = (
                    f"{', '.join(extra_arg_list)}" if len(extra_arg_list) > 0 else None
                )
                # lambda_map_arg_str joins the lambda arguments with the extra arguments, if extra arguments exist
                lambda_map_arg_str = (
                    func["lambda_map_arg_str"]
                    if "lambda_map_arg_str" in func
                    else (
                        f"{lambda_args_str}, {extra_args_str}"
                        if extra_args_str is not None
                        else lambda_args_str
                    )
                )
                # R note: helper: map <- lapply or purrr::map
                func_def_str += f"    return list(map(lambda {lambda_args_str}: {func['map_function']}({lambda_map_arg_str}), {map_args_str}))\n\n"

            file_str += func_def_str

        with open(os.path.join(output_dir, "lib", f"{filename}.py"), "w") as pyfile:
            pyfile.write(file_str)

    return map(lambda x: x[0], all_functions)  # Return the list of function filenames


def formulas_to_python(function_files):
    formulas = read_formulas_json()["formulas"]
    file_str = TOP_LINE_COMMENT
    file_str += "from h2a.ref_tables import *\n"
    file_str += "from h2a.inputs import *\n"
    file_str += "from h2a.globals import *\n"
    for filename in function_files:
        file_str += f"from h2a.lib.{filename} import *\n"

    file_str += "\n"

    for formula in formulas:
        name = (
            formula["name"]
            if "name" in formula and formula["name"] != ""
            else formula["orig_name"]
        )
        formula_def_str = f"{name} = "
        formula_def_str += f"{formula['expression']}\n"
        file_str += formula_def_str
    with open(os.path.join(root_dir, "py", "formulas.py"), "w") as pyfile:
        pyfile.write(file_str)


def main():
    function_files = functions_to_python()
    inputs_to_python()
    globals_to_python()
    helpers_to_python()
    formulas_to_python(function_files)

    # Use subprocess to run `python formulas.py`
    subprocess.run(["python", "formulas.py"], cwd=os.path.join(root_dir, "py"))
    print("✅ Run complete")

    # Use subprocess to run black on the generated Python files
    # subprocess.run(["black", "."], cwd=output_dir)

    # Use subprocess to run black on lib/
    subprocess.run(["black", "-q", "lib"], cwd=output_dir)


if __name__ == "__main__":
    main()
