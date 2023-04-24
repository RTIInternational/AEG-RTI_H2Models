import os
from .util import R_ENABLED, HELPERS_FILENAME, util_code


def helpers_to_lang(lang):
    code = {
        "get": {
            "py": "def get(obj, key):\n    return obj[key]\n\n",
            "R": "get <- function(obj, key) obj[[key]]\n\n",
        },
        "concat": {
            "py": "def concat(a, b):\n    return a + b\n\n",
            "R": 'concat <- function(a, b) paste(a, b, sep = "")\n\n',
        },
        "split": {
            "py": "def split(a, b):\n    return a.split(b)\n\n",
            "R": "split <- function(a, b) strsplit(a, b)[[1]]\n\n",
        },
        "seq_along": {"py": "def seq_along(a):\n    return range(len(a))\n\n", "R": ""},
        "TRUE": {
            "py": "TRUE = True\n",
            "R": "",
        },
        "assign_index": {
            "py": lambda name, val: f"{name} = {val}\n",
            "R": lambda name, val: f"{name} <- {val + 1}\n",
        },
    }
    file_str = util_code["top_line_comment"][lang]

    # get() is a helper function to access a dictionary
    file_str += code["get"][lang]

    # at() is a helper function to access a list using zero-based indexing
    # file_str += "def at(obj, index):\n    return obj[index]\n\n"
    # R: at <- function(x, i) x[[i + 1]]

    # concat() is a helper function to concatenate strings
    file_str += code["concat"][lang]

    # split() is a helper function to split a string
    file_str += code["split"][lang]

    # seq_along() is a helper function to get a sequence of integers
    file_str += code["seq_along"][lang]

    # R note: helper: range <- seq
    # R note: helper: len <- length

    file_str += code["TRUE"][lang]

    # H2A requires years of construction to be 1, 2, 3, or 4
    # These constants are used to compare against operation_range years
    # The final year of construction is the first year of operation
    file_str += code["assign_index"][lang]("YEAR_1", 0)
    file_str += code["assign_index"][lang]("YEAR_2", 1)
    file_str += code["assign_index"][lang]("YEAR_3", 2)
    file_str += code["assign_index"][lang]("YEAR_4", 3)

    with open(
        os.path.join(util_code["output_dir"][lang], f"{HELPERS_FILENAME}.{lang}"), "w"
    ) as codefile:
        codefile.write(file_str)


def helpers_to_code():
    helpers_to_lang("py")
    if R_ENABLED:
        helpers_to_lang("R")
