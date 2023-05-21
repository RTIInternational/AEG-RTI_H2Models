import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

from openpyxl import load_workbook
from run import run_model
from h2a.util import compare_lists, compare_value
from h2a.read_input import read_formulas_json

formulas = read_formulas_json()
results = run_model("default-smr-natural-gas-no-cc.json")
wb = load_workbook(filename = 'current-central-steam-methane-reforming-without-co2-sequestration-version-aug22.xlsm', data_only=True)

# For each formula with an excel_loc with a comma, split the string to get the sheet and cell/range
# Then check that the value in the cell/range matches the value in the results dictionary
for formula in formulas:
    if "excel_loc" in formula and "," in formula["excel_loc"]:
        name = (
            formula["name"]
            if "name" in formula and formula["name"] != ""
            else formula["orig_name"]
        )
        sheet, cell = formula["excel_loc"].split(",")
        cell = cell.strip()
        # If the cell is a range, check that the values in the range match the values in the results dictionary
        if ":" in cell:
            cells = wb[sheet][cell]
            values = list(map(lambda x: x[0].value, cells))
            if compare_lists(name, values, results[name]):
                print("✅", name)
        # If the cell is not a range, check that the value in the cell matches the value in the results dictionary
        else:
            value = wb[sheet][cell].value
            if compare_value(name, value, results[name]):
                print("✅", name)
