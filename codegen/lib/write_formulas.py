import os
from lib.read_json_files import read_inputs_json
from lib.write_inputs import inputs_to_lang
from .util import R_ENABLED, PRINT_FORMULAS, util_code


def formulas_to_lang(filename, formulas, import_statements, lang):
    code = {
        "import_inputs": {
            "py": "from h2a.inputs import *\n",
            "R": "source(here('h2a', 'inputs.R'))\n",
        },
        "function_def": {
            "py": "def calculate(user_input):\n",
            "R": "calculate <- function(user_input) {\n",
        },
        "assign": {
            "py": lambda name, expr: f"  {name} = {expr}\n",
            "R": lambda name, expr: f"  {name} <- {expr}\n",
        },
        "print": {
            "py": lambda name: f"  print('{name}: ', {name})\n\n",
            "R": lambda name: f'  print(paste("{name}", {name}, sep = ": "))\n\n',
        },
        "return_dict": {
            "py": "  return locals()\n",
            "R": "  return(setNames(mget(ls()), ls()))\n}\n",
        },
    }
    file_str = util_code["top_line_comment"][lang]

    for import_statement in import_statements:
        file_str += f"{import_statement[lang]}\n"

    file_str += "\n"

    file_str += code["function_def"][lang]

    file_str += inputs_to_lang(read_inputs_json(), lang)

    file_str += "\n\n"

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
        if PRINT_FORMULAS and filename == "formulas":
            file_str += code["print"][lang](name)

    file_str += code["return_dict"][lang]

    output_dir = util_code["output_dir"][lang]
    with open(os.path.join(output_dir, f"{filename}.{lang}"), "w") as codefile:
        codefile.write(file_str)


def formulas_to_code(filename, formulas, import_statements):
    formulas_to_lang(filename, formulas, import_statements, "py")
    if R_ENABLED:
        formulas_to_lang(filename, formulas, import_statements, "R")
