import os
import ast
from lib.util import py_h2a_dir

REF_TABLES_FILENAME = "ref_tables"


def get_ast_from_file(filename):
    with open(filename, "r") as pyfile:
        return ast.parse(pyfile.read())


def get_ast_from_py_h2a_file(filename):
    return get_ast_from_file(os.path.join(py_h2a_dir, filename))


ref_tables_ast = get_ast_from_py_h2a_file(f"{REF_TABLES_FILENAME}.py")

# Get all the names of the top-level variables in ref_tables.py
ref_tables_exports = []

for node in ref_tables_ast.body:
    if isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                ref_tables_exports.append(target.id)
