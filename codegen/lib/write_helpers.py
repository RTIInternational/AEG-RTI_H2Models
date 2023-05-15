import os
from .util import R_ENABLED, HELPERS_FILENAME, util_code


helper_code = {
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
    "npv": {
        "py": "def npv(r, cfList):\n    sum_pv = 0\n    for i, pmt in enumerate(cfList, start=1):\n        sum_pv += pmt / ((1 + r) ** i)\n    return sum_pv\n\n",
        "R": "npv <- function(r, cfList) {\n    sum_pv <- 0\n    for (i in seq_along(cfList)) {\n        sum_pv <- sum_pv + cfList[[i]] / ((1 + r) ^ i)\n    }\n    return(sum_pv)\n}\n\n",
    },
    "skip": {
        "py": "def skip(a, b):\n    return a[b:]\n\n",
        "R": "skip <- function(a, b) a[(b + 1):length(a)]\n\n",
    },
    "slice": {
        "py": "def slice(a, start=0, end=None):\n    return a[start:end]\n\n",
        "R": "slice <- function(a, start=0, end=NULL) a[(start + 1):end]\n\n",
    },
    "length": {
        "py": "def length(a):\n    return len(a)\n\n",
        "R": "",
    },
    "sum_args": {
        "py": "def sum_args(*args):\n    return sum(args)\n\n",
        "R": "sum_args <- function(...) sum(...)\n\n",
    },
    "seq_along": {"py": "def seq_along(a):\n    return range(len(a))\n\n", "R": ""},
    "append": {
        "py": "def append(a, b):\n    a.append(b)\n    return a\n\n",
        "R": "",
    },
    "reduce": {
        "py": "import functools\n\ndef reduce(function, iterable, initializer=None):\n    return functools.reduce(function, iterable, initializer)\n\n",
        "R": "reduce <- Reduce\n\n",
    },
    # "TRUE": {
    #     "py": "TRUE = True\n",
    #     "R": "",
    # },
    "assign_index": {
        "py": lambda name, val: f"{name} = {val}\n",
        "R": lambda name, val: f"{name} <- {val + 1}\n",
    },
}
code = helper_code


def helpers_to_lang(lang):
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

    # npv() is a helper function to calculate the net present value of a list of cash flows
    file_str += code["npv"][lang]

    # skip() is a helper function to get all but the first value of a list
    file_str += code["skip"][lang]

    # slice() is a helper function to get a slice of a list
    file_str += code["slice"][lang]

    # length() is a helper function to get the length of a list
    file_str += code["length"][lang]

    # sum_args() is a helper function to sum a list of arguments
    file_str += code["sum_args"][lang]

    # seq_along() is a helper function to get a sequence of integers
    file_str += code["seq_along"][lang]

    # append() is a helper function to append a value to a list
    file_str += code["append"][lang]

    # reduce() is a helper function to reduce a list to a single value
    file_str += code["reduce"][lang]

    # R note: helper: range <- seq

    # file_str += code["TRUE"][lang]

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
