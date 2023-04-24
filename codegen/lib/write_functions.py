import os
from .util import R_ENABLED, util_code


def process_condition(cond, lang):
    # TODO: This is a hacky way to do this, but it works for now
    if lang == "py":
        return cond
    elif lang == "R":
        return (
            cond.replace(" and ", " && ").replace(" or ", " || ").replace("not ", "!")
        )


def functions_to_lang(filename, functions, import_statements, lang):
    code = {
        "func_def": {
            "py": lambda name, args: f"def {name}({', '.join(args)}):\n",
            "R": lambda name, args: f"{name} <- function({', '.join(args)})" + " {\n",
        },
        "docstring": {
            "py": lambda description: f'    """{description}"""',
            "R": lambda description: f"    #'{description}",
        },
        "return": {
            "py": lambda expr: f"    return {expr}\n",
            "R": lambda expr: f"    return({expr})\n" + "}\n",
        },
        "if": {
            "py": lambda cond, body: f"    if {cond}:\n        return {body}\n",
            "R": lambda cond, body: f"    if ({cond}) {{\n        return({body})\n    }}\n",
        },
        "elif": {
            "py": lambda cond, body: f"    elif {cond}:\n        return {body}\n",
            "R": lambda cond, body: f"    else if ({cond}) {{\n        return({body})\n    }}\n",
        },
        "else": {
            "py": lambda body: f"    else:\n        return {body}\n",
            "R": lambda body: f"    else {{\n        return({body})\n    }}\n" + "}\n",
        },
        "map": {
            "py": lambda lambda_args_str, func, lambda_map_arg_str, map_args_str: f"    return list(map(lambda {lambda_args_str}: {func}({lambda_map_arg_str}), {map_args_str}))\n\n",
            "R": lambda lambda_args_str, func, lambda_map_arg_str, map_args_str: f"    return(lapply({map_args_str}, function({lambda_args_str}) {func}({lambda_map_arg_str})))\n"
            + "}\n",
        },
    }
    file_str = util_code["top_line_comment"][lang]
    for import_statement in import_statements:
        file_str += f"{import_statement[lang]}\n"

    for func in functions:
        args = func["args"] if "args" in func else []
        func_def_str = code["func_def"][lang](func["name"], args)
        if "description" in func:
            func_def_str += code["docstring"][lang](func["description"]) + "\n"
        if "body" in func:
            func_def_str += code["return"][lang](func["body"])
        elif "type" in func:
            if func["type"] == "switch":
                cond1 = process_condition(func["cases"][0]["condition"], lang)
                body1 = func["cases"][0]["body"]
                func_def_str += code["if"][lang](cond1, body1)
                # Iterate after the first case to the second-to-last case
                for case in func["cases"][1:-1]:
                    cond = process_condition(case["condition"], lang)
                    body = case["body"]
                    func_def_str += code["elif"][lang](cond, body)
                # Add the last case
                bodyn = func["cases"][-1]["body"]
                func_def_str += code["else"][lang](bodyn)

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
            func_def_str += code["map"][lang](
                lambda_args_str,
                func["map_function"],
                lambda_map_arg_str,
                map_args_str,
            )

        file_str += func_def_str

    with open(
        os.path.join(util_code["output_dir"][lang], "lib", f"{filename}.{lang}"), "w"
    ) as codefile:
        codefile.write(file_str)


def functions_to_code(filename, functions, import_statements):
    functions_to_lang(filename, functions, import_statements, "py")
    if R_ENABLED:
        functions_to_lang(filename, functions, import_statements, "R")
