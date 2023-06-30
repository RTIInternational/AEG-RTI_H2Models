import json
import os


def prep(clean: bool):
    if clean:
        # Delete out/ directory if it exists
        if os.path.exists("out"):
            for filename in os.listdir("out"):
                filepath = os.path.join("out", filename)
                os.remove(filepath)
            os.rmdir("out")

    # Make out/ directory if it doesn't exist
    if not os.path.exists("out"):
        os.makedirs("out")


def write_output(results, input):

    # Delete user_input and non-serializable keys from results
    del results["user_input"]
    del results["analysis_range"]
    del results["analysis_index_range"]
    del results["recovery_range"]
    del results["recovery_index_range"]
    del results["remaining_depreciation_range"]

    # Write results to out/ as JSON with filename = input filename
    with open(os.path.join("out", input), "w") as outfile:
        json.dump(results, outfile)

def transform_for_graph1(input_files, results_list):
    # Quick and dirty script to transform the output of the H2A model into a format that can be used by the graphing library
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
    for i, input in enumerate(input_files):
        results = results_list[i]
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
    return cost_breakdown_array, categories