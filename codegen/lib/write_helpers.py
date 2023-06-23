import os
from .util import R_ENABLED, HELPERS_FILENAME, util_code


helper_code = {
    "irr": {
        "py": "from .helper_irr import IRR\n\ndef irr(cfList):\n    return IRR(cfList)\n\n",
        "R": "irr <- function(cfList) {\n    return(tidyquant::IRR(cfList))\n}\n\n",
    },
    "npv": {
        "py": "def npv(r, cfList):\n    sum_pv = 0\n    for i, pmt in enumerate(cfList, start=1):\n        sum_pv += pmt / ((1 + r) ** i)\n    return sum_pv\n\n",
        "R": "npv <- function(r, cfList) {\n    sum_pv <- 0\n    for (i in seq_along(cfList)) {\n        sum_pv <- sum_pv + cfList[[i]] / ((1 + r) ^ i)\n    }\n    return(sum_pv)\n}\n\n",
    },
    "round_num": {
        "py": "def round_num(num, ndigits):\n    if ndigits >= 0:\n        factor = 10 ** ndigits\n        return int(num * factor + 0.5) / factor\n    else:\n        factor = 10 ** abs(ndigits)\n        return int(num / factor + 0.5) * factor\n\n",
        "R": "round_num <- function(num, ndigits) {\n    if (ndigits >= 0) {\n        factor <- 10 ^ ndigits\n        return(as.integer(num * factor + 0.5) / factor)\n    } else {\n        factor <- 10 ^ abs(ndigits)\n        return(as.integer(num / factor + 0.5) * factor)\n    }\n}\n\n",
    },
    "to_str": {
        "py": "def to_str(num):\n    return str(num)\n\n",
        "R": "to_str <- function(num) {\n    return(as.character(num))\n}\n\n",
    },
    "to_num": {
        "py": "def to_num(str):\n    return float(str)\n\n",
        "R": "to_num <- function(str) {\n    return(as.numeric(str))\n}\n\n",
    },
    "get": {
        "py": "def get(obj, key, default_val=0):\n    return obj.get(key, default_val) if isinstance(obj, dict) else (obj[key] if key in obj or (isinstance(key, int) and len(obj) > key) else default_val)\n\n",
        "R": "get <- function(obj, key, default_val = 0) {\n    if (is.null(obj[[key]])) {\n        return(default_val)\n    } else {\n        return(obj[[key]])\n    }\n}\n\n",
    },
    "get_cell": {
        "py": "def get_cell(df, row, col):\n    return get(get(df, col), row) \n\n",
        "R": "get_cell <- function(df, row, col) df[as.character(row), col]\n\n",
    },
    "concat": {
        "py": "def concat(a, b):\n    return a + b\n\n",
        "R": 'concat <- function(a, b) paste(a, b, sep = "")\n\n',
    },
    "split": {
        "py": "def split(a, b):\n    return a.split(b)\n\n",
        "R": "split <- function(a, b) strsplit(a, b)[[1]]\n\n",
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
    # "divide": {
    #     "py": "def divide(a, b):\n    return a / b if b != 0 else 0\n\n",
    #     "R": "divide <- function(a, b) if (b != 0) a / b else 0\n\n",
    # },
    "sum_list": {
        "py": "def sum_list(a):\n    return sum(a)\n\n",
        "R": "sum_list <- function(a) sum(unlist(a))\n\n",
    },
    "sum_args": {
        "py": "def sum_args(*args):\n    return sum(args)\n\n",
        "R": "sum_args <- function(...) sum(...)\n\n",
    },
    "num_range": {
        "py": "def num_range(start, end):\n    return range(start, end)\n\n",
        "R": "num_range <- function(start, end) seq(start, end - 1)\n\n",
    },
    "sum_columns": {
        "py": "def sum_columns(rows):\n    columns = zip(*rows)\n    return list(map(sum, columns))\n\n",
        "R": "sum_columns <- function(rows) {\n    columns <- t(rows)\n    df <- as.data.frame(do.call(rbind, columns))\n    numeric_df <- dplyr::mutate_all(df, function(x) as.numeric(as.character(x)))\n    return(colSums(numeric_df))\n}\n\n",
    },
    "seq_along": {"py": "def seq_along(a):\n    return range(len(a))\n\n", "R": ""},
    "append": {
        "py": "def append(a, b):\n    a.append(b)\n    return a\n\n",
        "R": "",
    },
    "evaluate": {
        "py": "evaluate = eval\n\n",
        "R": "evaluate <- function(expr) eval(parse(text = expr))\n\n",
    },
    "args_to_list": {
        "py": "def args_to_list(*args):\n    return list(args)\n\n",
        "R": "args_to_list <- function(...) c(...)\n\n",
    },
    # "reduce": {
    #     "py": "import functools\n\ndef reduce(function, iterable, initializer=None):\n    return functools.reduce(function, iterable, initializer)\n\n",
    #     "R": "reduce <- Reduce\n\n",
    # },
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

    # irr() is a helper function to calculate the internal rate of return of a list of cash flows
    file_str += code["irr"][lang]

    # npv() is a helper function to calculate the net present value of a list of cash flows
    file_str += code["npv"][lang]

    # round_num() is a helper function to round a number to a specified number of digits
    # Negative ndigits means rounding to the nearest power of ten (e.g. -2 rounds to the nearest hundred)
    file_str += code["round_num"][lang]

    # to_str() is a helper function to convert a number to a string
    file_str += code["to_str"][lang]

    # to_num() is a helper function to convert a string to a number
    file_str += code["to_num"][lang]

    # get() is a helper function to access a dictionary
    file_str += code["get"][lang]

    # get_cell() is a helper function to access a dataframe
    file_str += code["get_cell"][lang]

    # at() is a helper function to access a list using zero-based indexing
    # file_str += "def at(obj, index):\n    return obj[index]\n\n"
    # R: at <- function(x, i) x[[i + 1]]

    # concat() is a helper function to concatenate strings
    file_str += code["concat"][lang]

    # split() is a helper function to split a string
    file_str += code["split"][lang]

    # skip() is a helper function to get all but the first value of a list
    file_str += code["skip"][lang]

    # slice() is a helper function to get a slice of a list
    file_str += code["slice"][lang]

    # length() is a helper function to get the length of a list
    file_str += code["length"][lang]

    # divide() is a helper function to divide two numbers (returns 0 if the denominator is 0)
    # file_str += code["divide"][lang]

    # sum_args() is a helper function to sum a list of arguments
    file_str += code["sum_args"][lang]

    # sum_list() is a helper function to sum a list
    file_str += code["sum_list"][lang]

    # range() is a helper function to get a range of integers
    file_str += code["num_range"][lang]

    # sum_columns() is a helper function to sum the columns of a list of lists
    file_str += code["sum_columns"][lang]

    # seq_along() is a helper function to get a sequence of integers
    file_str += code["seq_along"][lang]

    # append() is a helper function to append a value to a list
    file_str += code["append"][lang]

    # eval() is a helper function to evaluate a string as code
    file_str += code["evaluate"][lang]

    # args_to_list() is a helper function to convert a list of arguments to a list
    file_str += code["args_to_list"][lang]

    # reduce() is a helper function to reduce a list to a single value
    # file_str += code["reduce"][lang]

    # R note: helper: range <- seq

    # file_str += code["TRUE"][lang]

    # H2A requires years of construction to be 1, 2, 3, or 4
    # These constants are used to compare against operation_range years
    # The final year of construction is the first year of operation
    file_str += code["assign_index"][lang]("YEAR_1", 0)
    file_str += code["assign_index"][lang]("YEAR_2", 1)
    file_str += code["assign_index"][lang]("YEAR_3", 2)
    file_str += code["assign_index"][lang]("YEAR_4", 3)

    file_str += code["assign_index"][lang]("FIRST", 0)
    file_str += code["assign_index"][lang]("SECOND", 1)
    file_str += code["assign_index"][lang]("THIRD", 2)

    with open(
        os.path.join(util_code["output_dir"][lang], f"{HELPERS_FILENAME}.{lang}"), "w"
    ) as codefile:
        codefile.write(file_str)


def helpers_to_code():
    helpers_to_lang("py")
    if R_ENABLED:
        helpers_to_lang("R")
