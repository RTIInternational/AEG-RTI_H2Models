import os

from .util import R_ENABLED, INPUTS_FILENAME, py_h2a_dir, r_h2a_dir, util_code


def inputs_to_lang(inputs, lang):
    """Creates a Python/R file containing the user inputs and returns a list of the names of the variables"""

    code = {
        "import": {
            "py": "from h2a.read_input import user_input\n\n",
            "R": 'import::from("read_input.R", user_input, .directory = here("h2a"))\n\n',
        },
        "assign": {
            "py": lambda key: f"{key} = user_input['{key}']\n",
            "R": lambda key: f'{key} <- user_input[["{key}"]]\n',
        },
        "output_dir": {"py": py_h2a_dir, "R": r_h2a_dir},
    }

    inputs_exports = []
    file_str = util_code["top_line_comment"][lang]
    file_str += code["import"][lang]

    for key in inputs:
        if key == "$schema":
            continue
        file_str += code["assign"][lang](key)
        inputs_exports.append(key)

    with open(
        os.path.join(code["output_dir"][lang], f"{INPUTS_FILENAME}.{lang}"), "w"
    ) as pyfile:
        pyfile.write(file_str)
    return inputs_exports


def inputs_to_code(inputs):
    input_exports = inputs_to_lang(inputs, "py")
    if R_ENABLED:
        inputs_to_lang(inputs, "R")
    return input_exports
