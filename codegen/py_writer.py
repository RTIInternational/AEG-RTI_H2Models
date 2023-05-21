# Read JSON files containing function and variable definitions and output Python files

import ast
import itertools
import os
import subprocess
from lib.write_functions import functions_to_code
from lib.write_helpers import helpers_to_code, helper_code
from lib.write_formulas import formulas_to_code
from lib.read_json_files import (
    read_functions_json,
    read_formulas_json,
)
from lib.util import (
    py_dir,
    py_h2a_dir,
    HELPERS_FILENAME,
)
from lib.read_ref_table_exports import ref_tables_exports, REF_TABLES_FILENAME

FORMULAS_FILENAME = "formulas"

# function names of helper functions
HELPER_CODE_KEYS = list(helper_code.keys())

# Some extra helper constants not defined in helper_code
HELPER_CODE_EXTRA_KEYS = ["YEAR_1", "YEAR_2", "YEAR_3", "YEAR_4", "FIRST", "SECOND", "THIRD"]

# All helper functions and constants
HELPERS_EXPORTS = HELPER_CODE_KEYS + HELPER_CODE_EXTRA_KEYS

# Some helper functions are only used in Python, so we need to filter them out
R_HELPER_EXPORTS = (
    list(filter(lambda x: helper_code[x]["R"] != "", HELPER_CODE_KEYS))
    + HELPER_CODE_EXTRA_KEYS
)


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
            elif "reduce_function" in func:
                reduce_function_tree = ast.parse(func["reduce_function"])
                parse_tree(reduce_function_tree, node, edges)
                edges.append({"from": "", "to": "reduce"})
        new_all_functions.append((filename, functions, nodes, edges))

    return new_all_functions


def dir_path_to_import_str(dirs, filename, lang):
    """Helper function for edges_to_imports. Returns a string that can be used in an import statement in Python or R."""
    if lang == "py":
        # py_import_path is "h2a" joined with dirs if any exist, and filename, separated by periods
        py_import_path = "h2a"
        if dirs:
            py_import_path += "." + ".".join(dirs)
        py_import_path += "." + filename
        return py_import_path
    elif lang == "R":
        # R_import_path is "h2a" joined with dirs if any exist, separated by commas
        R_import_path = "h2a"
        if dirs:
            R_import_path += "," + ",".join(dirs)
        return R_import_path


def edges_to_imports(edges, lib_exports):
    """Returns a list of import statements given edges (file dependencies) and exports (vars/functions exported by each file)"""
    all_imports = []
    import_statements = []
    file_dirs = {
        x[0]: x[2] for x in lib_exports
    }  # {filename: dirs} where dirs is like ["lib"]

    for edge in edges:
        for filename, exports, _ in lib_exports:
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
        dirs = file_dirs[filename]
        imports_as_list = list(imports)
        import_list = [x[1] for x in imports_as_list]
        # Sort import_list alphabetically
        import_list.sort()
        py_import_list_str = ", ".join(import_list)

        # If the file is the helper file, only import the functions that are used
        if imports_as_list[0][0] == "helpers":
            r_import_list = list(filter(lambda x: x in R_HELPER_EXPORTS, import_list))
            r_import_list.sort()
            r_import_list_str = ", ".join(r_import_list)
        else:
            r_import_list_str = py_import_list_str

        import_statements.append(
            {
                "py": f"from {dir_path_to_import_str(dirs, filename, 'py')} import {py_import_list_str}",
                "R": f'import::from("{filename}.R", {r_import_list_str}, .directory = here({dir_path_to_import_str(dirs, "", "R")}))',
            }
        )

    return import_statements


def main():
    """
    1) Read JSON files
    2) Parse JSON files into nodes and edges to create dependency graphs
    3) Convert edges into import statements
    5) Translate formulas & functions to Python/R code
    6) Write code to files
    """
    all_functions = read_functions_json()
    formulas = read_formulas_json()["formulas"]

    new_all_functions = parse_functions_to_nodes_and_edges(all_functions)
    function_filenames = []
    # Functions dependency tree
    for filename, functions, function_nodes, function_edges in new_all_functions:
        imports_for_functions = edges_to_imports(
            function_edges,
            [
                (REF_TABLES_FILENAME, ref_tables_exports, []),
                (HELPERS_FILENAME, HELPERS_EXPORTS, []),
            ],
        )
        functions_to_code(filename, functions, imports_for_functions)
        function_filenames.append(filename)

    helpers_to_code()

    # Formulas dependency tree
    _, formulas_edges = parse_formulas_to_nodes_and_edges(formulas)
    imports_for_formulas = edges_to_imports(
        formulas_edges,
        [
            (REF_TABLES_FILENAME, ref_tables_exports, []),
            (HELPERS_FILENAME, HELPERS_EXPORTS, []),
        ]
        + [
            (filename, exports, ["lib"])
            for filename, _, exports, _ in new_all_functions
        ],
    )
    formulas_to_code(FORMULAS_FILENAME, formulas, imports_for_formulas)

    # Use subprocess to run `python run.py`
    subprocess.run(["python", "run.py"], cwd=os.path.join(py_dir))
    print("✅ Run complete")

    # Use subprocess to run black on the generated Python files
    # subprocess.run(["black", "."], cwd=output_dir)

    # Use subprocess to run black on lib/
    subprocess.run(["black", "-q", "lib"], cwd=py_h2a_dir)


if __name__ == "__main__":
    main()
