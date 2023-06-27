import os
import typer
from typing import List

from h2a.util import root_dir
from h2a.cli_lib import prep, write_output
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

    original_filenames = [
        "default-autothermal-reforming-natural-gas-with-cc.json"
        "default-smr-natural-gas-with-cc.json"
        "default-pem-electrolysis.json"
        "default-smr-natural-gas-no-cc.json"
        "default-solid-oxide-electrolysis.json"
    ]
    filename_lookup = {
        "default-autothermal-reforming-natural-gas-with-cc.json": "ATR with CCS",
        "default-smr-natural-gas-with-cc.json": "SMR with CCS",
        "default-pem-electrolysis.json": "PEM Electrolysis",
        "default-smr-natural-gas-no-cc.json": "SMR without CCS",
        "default-solid-oxide-electrolysis.json": "Solid Oxide Electrolysis"
    }

    breakdown_original_keys = [
        "dollars_per_kg_h2_capital_related_costs",
        "dollars_per_kg_h2_decommissioning_costs",
        "dollars_per_kg_h2_fixed_cost",
        "dollars_per_kg_h2_total_feedstock_cost",
        "dollars_per_kg_h2_other_raw_material_cost",
        "dollars_per_kg_h2_variable_cost",
    ]
    key_lookup = {
        "dollars_per_kg_h2_capital_related_costs": "Capital Costs",
        "dollars_per_kg_h2_decommissioning_costs": "Decommissioning Costs",
        "dollars_per_kg_h2_fixed_cost": "Fixed Costs",
        "dollars_per_kg_h2_total_feedstock_cost": "Total Feedstock Cost",
        "dollars_per_kg_h2_other_raw_material_cost": "Other Raw Material Costs",
        "dollars_per_kg_h2_variable_cost": "Variable Costs",
    }

    cost_breakdown = {
        "Capital Costs": [],
        "Decommissioning Costs": [],
        "Fixed Costs": [],
        "Total Feedstock Cost": [],
        "Other Raw Material Costs": [],
        "Variable Costs": [],
    }
    categories = []
    for input in input_files:
        results = run_model(input)
        write_output(results, input)

        # Chart info
        categories.append(filename_lookup[input])
        for key in breakdown_original_keys:
            if key in results:
                cost_breakdown[key_lookup[key]].append(results[key])
            else:
                print(f"Warning: {key} not found in {input}")

    cost_breakdown_array = []
    for key in cost_breakdown:
        cost_breakdown_array.append(
            {
                "name": key,
                "data": cost_breakdown[key],
            }
        )
    
    print(cost_breakdown_array)
    print(categories)

if __name__ == "__main__":
    typer.run(main)
