
def inputs_to_lang(inputs, lang):
    """Returns a Python/R string containing the assignments of the inputs off the dictionary"""

    code = {
        "assign": {
            "py": lambda key: f"  {key} = user_input['{key}']\n",
            "R": lambda key: f'  {key} <- user_input[["{key}"]]\n',
        },
    }

    file_str = ""

    for key in inputs:
        if key == "$schema":
            continue
        file_str += code["assign"][lang](key)

    return file_str
