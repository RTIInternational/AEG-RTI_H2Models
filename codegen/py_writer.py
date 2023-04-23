# Read JSON files containing function and variable definitions and output Python files

import ast
import itertools
import os
import subprocess
from lib.read_json_files import (
    read_functions_json,
    read_globals_json,
    read_inputs_json,
    read_formulas_json,
)
from lib.util import py_dir, py_h2a_dir
from lib.read_ref_table_exports import ref_tables_exports, REF_TABLES_FILENAME

# Get project root directory
TOP_LINE_COMMENT = """#
# This file is programmatically generated by py_writer.py; do not edit
#
"""

INPUTS_FILENAME = "inputs"  # Python file containing the user input variables
GLOBALS_FILENAME = "globals"  # Name of the Python file containing a few global variables that functions use
HELPERS_FILENAME = "helpers"  # Name of the Python file containing helper functions


def globals_to_python(global_formulas, import_statements):
    file_str = TOP_LINE_COMMENT
    for import_statement in import_statements:
        file_str += f"{import_statement}\n"

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
    with open(os.path.join(py_h2a_dir, f"{GLOBALS_FILENAME}.py"), "w") as pyfile:
        pyfile.write(file_str)


def inputs_to_python(inputs):
    """Creates a Python file containing the user inputs and returns a list of the names of the variables"""
    inputs_exports = []
    file_str = TOP_LINE_COMMENT
    file_str += "from h2a.read_input import user_input\n\n"

    for key in inputs:
        if key == "$schema":
            continue
        file_str += f"{key} = user_input['{key}']\n"
        inputs_exports.append(key)

    with open(os.path.join(py_h2a_dir, f"{INPUTS_FILENAME}.py"), "w") as pyfile:
        pyfile.write(file_str)
    return inputs_exports


HELPERS_EXPORTS = [
    "get",
    "concat",
    "split",
    "seq_along",
    "YEAR_1",
    "YEAR_2",
    "YEAR_3",
    "YEAR_4",
    "TRUE",
]


def helpers_to_python():
    file_str = TOP_LINE_COMMENT

    # get() is a helper function to access a dictionary
    file_str += "def get(obj, key):\n    return obj[key]\n\n"

    # at() is a helper function to access a list using zero-based indexing
    # file_str += "def at(obj, index):\n    return obj[index]\n\n"
    # R: at <- function(x, i) x[[i + 1]]

    # concat() is a helper function to concatenate strings
    file_str += "def concat(a, b):\n    return a + b\n\n"

    # split() is a helper function to split a string
    file_str += "def split(a, b):\n    return a.split(b)\n\n"

    # seq_along() is a helper function to get a sequence of integers
    file_str += "def seq_along(a):\n    return range(len(a))\n\n"

    # R note: helper: range <- seq
    # R note: helper: len <- length

    file_str += "TRUE = True\n"

    # H2A requires years of construction to be 1, 2, 3, or 4
    # These constants are used to compare against operation_range years
    # The final year of construction is the first year of operation
    file_str += "YEAR_1 = 0\n"
    file_str += "YEAR_2 = 1\n"
    file_str += "YEAR_3 = 2\n"
    file_str += "YEAR_4 = 3\n"

    with open(os.path.join(py_h2a_dir, f"{HELPERS_FILENAME}.py"), "w") as pyfile:
        pyfile.write(file_str)


def functions_to_python(filename, functions, import_statements):
    file_str = TOP_LINE_COMMENT
    for import_statement in import_statements:
        file_str += f"{import_statement}\n"

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

    with open(os.path.join(py_h2a_dir, "lib", f"{filename}.py"), "w") as pyfile:
        pyfile.write(file_str)


PRINT_FORMULAS = True


def formulas_to_python(formulas, import_statements):
    file_str = TOP_LINE_COMMENT
    file_str += "from h2a.inputs import *\n"
    for import_statement in import_statements:
        file_str += f"{import_statement}\n"

    file_str += "\n"

    for formula in formulas:
        # Skip if name starts with #
        if "name" in formula and formula["name"].startswith("#"):
            continue
        name = (
            formula["name"]
            if "name" in formula and formula["name"] != ""
            else formula["orig_name"]
        )
        formula_def_str = f"{name} = "
        formula_def_str += f"{formula['expression']}\n"
        file_str += formula_def_str
        if PRINT_FORMULAS:
            file_str += f"print('{name}: ', {name})\n\n"
    with open(os.path.join(py_dir, "formulas.py"), "w") as pyfile:
        pyfile.write(file_str)


def parse_formulas_to_nodes_and_edges(formulas):
    """Parses each formula in global_formulas to get the names of all the variables in the formula expression."""
    nodes = []
    edges = []
    for formula in formulas:
        node = (
            formula["name"]
            if "name" in formula and formula["name"] != ""
            else formula["orig_name"]
        )
        # node = {
        #     "id": formula["name"],
        #     "label": formula["name"],
        #     "type": "global",
        # }
        nodes.append(node)
        # Use ast to parse the formula expression
        tree = ast.parse(formula["expression"])
        # Get the names of all the variables in the formula expression
        var_names = [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]
        for var_name in var_names:
            edge = {"from": node, "to": var_name}
            # If edge not already in edges, add it
            if edge not in edges:
                edges.append(edge)
    return nodes, edges


def parse_functions_to_nodes_and_edges(all_functions):
    def parse_tree(tree, node, edges):
        # Get the unique names of all the variables in the function body
        var_names = list(
            set([node.id for node in ast.walk(tree) if isinstance(node, ast.Name)])
        )
        # Remove arguments from var_names
        if "args" in func:
            for arg in func["args"]:
                if arg in var_names:
                    var_names.remove(arg)
        # Remove map_item_names from var_names
        if "map_item_names" in func:
            for arg in func["map_item_names"]:
                if arg in var_names:
                    var_names.remove(arg)
        if len(var_names) > 0:
            for var_name in var_names:
                edge = {"from": node, "to": var_name}
                # If edge not already in edges, add it
                if edge not in edges:
                    edges.append(edge)

    new_all_functions = []
    for filename, functions in all_functions:
        nodes = []
        edges = []
        for func in functions:
            node = func["name"]
            # node = {
            #     "id": func["name"],
            #     "label": func["name"],
            #     "type": "function",
            #     "filename": filename,
            # }
            nodes.append(node)
            if "body" in func:
                # Use ast to parse the function body and get the names of all the variables in the function body that are not arguments
                tree = ast.parse(func["body"])
                parse_tree(tree, node, edges)
            if "type" in func and func["type"] == "switch":
                for case in func["cases"]:
                    body_tree = ast.parse(case["body"])
                    parse_tree(body_tree, node, edges)
                    condition_tree = ast.parse(case["condition"])
                    parse_tree(condition_tree, node, edges)
            if "map_function" in func:
                map_function_tree = ast.parse(func["map_function"])
                parse_tree(map_function_tree, node, edges)
                if "map_args_str" in func:
                    map_args_str_tree = ast.parse(func["map_args_str"])
                    parse_tree(map_args_str_tree, node, edges)
                if "lambda_map_arg_str" in func:
                    lambda_map_arg_str_tree = ast.parse(func["lambda_map_arg_str"])
                    parse_tree(lambda_map_arg_str_tree, node, edges)
        new_all_functions.append((filename, functions, nodes, edges))

    return new_all_functions


# For each global_edges[i]["to"], if it is in lib_exports, then add an import statement for it
def edges_to_imports(edges, lib_exports):
    """Returns a list of import statements given edges (file dependencies) and exports (vars/functions exported by each file)"""
    all_imports = []
    import_statements = []

    for edge in edges:
        for filename, exports in lib_exports:
            found = None
            for export in exports:
                if edge["to"] == export:
                    found = export
                    break
            if found and (filename, found) not in all_imports:
                all_imports.append((filename, found))
    # Sort all_imports by filename
    all_imports.sort(key=lambda x: x[0])
    # Iterate over all_imports and group them by filename
    for filename, imports in itertools.groupby(all_imports, key=lambda x: x[0]):
        import_statements.append(
            f"from h2a.{filename} import {', '.join([x[1] for x in imports])}"
        )

    return import_statements


def main():
    """
    1) Read JSON files
    2) Parse JSON files into nodes and edges to create dependency graphs
    3) Convert nodes and edges into import statements
    5) Parse JSON into Python code (expressions and functions)
    6) Write Python code to files
    """
    inputs = read_inputs_json()
    global_formulas = read_globals_json()["globals"]
    all_functions = read_functions_json()
    formulas = read_formulas_json()["formulas"]

    input_exports = inputs_to_python(inputs)

    global_exports, global_edges = parse_formulas_to_nodes_and_edges(global_formulas)
    # Globals dependency tree
    imports_for_globals = edges_to_imports(
        global_edges,
        [(REF_TABLES_FILENAME, ref_tables_exports), (INPUTS_FILENAME, input_exports)],
    )

    globals_to_python(global_formulas, imports_for_globals)

    new_all_functions = parse_functions_to_nodes_and_edges(all_functions)
    function_filenames = []
    # Functions dependency tree
    for filename, functions, function_nodes, function_edges in new_all_functions:
        imports_for_functions = edges_to_imports(
            function_edges,
            [
                (REF_TABLES_FILENAME, ref_tables_exports),
                (HELPERS_FILENAME, HELPERS_EXPORTS),
                (GLOBALS_FILENAME, global_exports),
            ],
        )
        functions_to_python(filename, functions, imports_for_functions)
        function_filenames.append(filename)

    helpers_to_python()

    # Formulas dependency tree
    _, formulas_edges = parse_formulas_to_nodes_and_edges(formulas)
    imports_for_formulas = edges_to_imports(
        formulas_edges,
        [
            (REF_TABLES_FILENAME, ref_tables_exports),
            (HELPERS_FILENAME, HELPERS_EXPORTS),
            (GLOBALS_FILENAME, global_exports),
        ]
        + [
            (f"lib.{filename}", exports)
            for filename, _, exports, _ in new_all_functions
        ],
    )
    formulas_to_python(formulas, imports_for_formulas)

    # Use subprocess to run `python formulas.py`
    subprocess.run(["python", "formulas.py"], cwd=os.path.join(py_dir))
    print("✅ Run complete")

    # Use subprocess to run black on the generated Python files
    # subprocess.run(["black", "."], cwd=output_dir)

    # Use subprocess to run black on lib/
    subprocess.run(["black", "-q", "lib"], cwd=py_h2a_dir)


if __name__ == "__main__":
    main()
