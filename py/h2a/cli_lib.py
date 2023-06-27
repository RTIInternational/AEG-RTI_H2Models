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
