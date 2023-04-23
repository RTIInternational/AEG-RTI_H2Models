import os
from .util import R_ENABLED, py_h2a_dir, r_h2a_dir, util_code


def formulas_to_lang(filename, formulas, import_statements, lang):
    code = {
        "import_inputs": {
            "py": "from h2a.inputs import *\n",
            "R": "source(here('h2a', 'inputs.R'))\n",
        },
        "assign": {
            "py": lambda name, expr: f"{name} = {expr}\n",
            "R": lambda name, expr: f"{name} <- {expr}\n",
        },
        "output_dir": {"py": py_h2a_dir, "R": r_h2a_dir},
    }
    file_str = util_code["top_line_comment"][lang]

    if filename == "formulas":
        file_str += code["import_inputs"][lang]

    for import_statement in import_statements:
        file_str += f"{import_statement[lang]}\n"

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
        file_str += code["assign"][lang](name, formula["expression"])
    with open(
        os.path.join(code["output_dir"][lang], f"{filename}.{lang}"), "w"
    ) as codefile:
        codefile.write(file_str)


def formulas_to_code(filename, formulas, import_statements):
    formulas_to_lang(filename, formulas, import_statements, "py")
    if R_ENABLED:
        formulas_to_lang(filename, formulas, import_statements, "R")
