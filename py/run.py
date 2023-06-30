import os
import typer
from typing import List

from h2a.util import root_dir
from h2a.cli_lib import prep, write_output, transform_for_graph1
from h2a.read_input import read_inputs_json
from h2a.formulas import calculate

def run_model(input_data_file):
    user_input = read_inputs_json(input_data_file)
    return calculate(user_input)

def main(input_files: List[str], clean: bool = False):
    prep(clean)

    if len(input_files) == 1 and input_files[0] == "all":
        input_files = []
        for filename in os.listdir(os.path.join(root_dir, "data", "input", "default")):
            if filename != "input.schema.json":
                input_files.append(filename)

    results_list = []
    for input in input_files:
        results = run_model(input)
        write_output(results, input)

        results_list.append(results)

    series, categories = transform_for_graph1(input_files, results_list)
    # Replace var SERIES_DATA=[] in index.html
    with open(os.path.join(root_dir, "index-data.js"), "w") as f:
        f.write(f"window.SERIES_DATA={series};\n")
        f.write(f"window.CATEGORIES={categories};\n")


if __name__ == "__main__":
    typer.run(main)
