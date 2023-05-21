
from h2a.read_input import read_inputs_json
from h2a.formulas import calculate

def run_model(input_data_file):
    user_input = read_inputs_json(input_data_file)
    return calculate(user_input)

if __name__ == "__main__":
    results = run_model("default-smr-natural-gas-no-cc.json")
    # results = run_model("default-smr-natural-gas-with-cc.json")
    print(results)
