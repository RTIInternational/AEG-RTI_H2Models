import sys
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

from openpyxl import load_workbook
from run import run_model
from h2a.util import compare_lists, compare_value
from h2a.read_input import read_formulas_json


def check_formulas(input_filename, excel_filename):
    formulas = read_formulas_json()

    results = run_model(input_filename)
    wb = load_workbook(filename=excel_filename, data_only=True)

    is_pem = "-pem-" in input_filename

    # For each formula with an excel_loc with a comma, split the string to get the sheet and cell/range
    # Then check that the value in the cell/range matches the value in the results dictionary
    for formula in formulas:
        if "excel_loc" in formula and "," in formula["excel_loc"]:
            name = (
                formula["name"]
                if "name" in formula and formula["name"] != ""
                else formula["orig_name"]
            )
            excel_loc = (
                formula["pem_excel_loc"]
                if is_pem and "pem_excel_loc" in formula
                else formula["excel_loc"]
            )
            parts = excel_loc.split(",")
            if len(parts) == 2:
                sheet, cell = parts
                cell = cell.strip()
                # If excel_filename is "current-central-steam-methane-reforming-with-co2-sequestration-version-aug-22.xlsm"
                # and the sheet is "Input_Sheet_Template" and the cell row is greater than 90, subtract 1 from the row
                if (
                    (
                        excel_filename
                        == "current-central-steam-methane-reforming-with-co2-sequestration-version-aug-22.xlsm"
                        or excel_filename
                        == "current-central-authothermal-reforming-of-natural-gas-with-co2-sequestration-version-aug22.xlsm"
                    )
                    and sheet == "Input_Sheet_Template"
                    and int(cell[1:]) > 90
                ):
                    cell = cell[0] + str(int(cell[1:]) - 1)

                # if is_pem and cell row is greater than 85, subtract 2 from the row
                if is_pem and sheet == "Input_Sheet_Template" and int(cell[1:]) > 85:
                    cell = cell[0] + str(int(cell[1:]) - 2)

                if (
                    (excel_filename
                    == "current-central-steam-methane-reforming-without-co2-sequestration-version-aug22.xlsm"
                    or is_pem)
                    and sheet == "Carbon Sequestration"
                ):
                    continue  # No use in checking unused formulas

                # If the cell is a range, check that the values in the range match the values in the results dictionary
                if ":" in cell:
                    cells = wb[sheet][cell]
                    # Split the range into two cells
                    cell1, cell2 = cell.split(":")
                    # Get first character of cell1 and cell2
                    cell1_char = cell1[0]
                    cell2_char = cell2[0]
                    # If the first character of cell1 and cell2 are different, set cells = cells[0]
                    if cell1_char != cell2_char:
                        cells = cells[0]
                        excel_vals = list(map(lambda x: x.value, cells))
                    else:
                        excel_vals = list(map(lambda x: x[0].value, cells))
                    py_vals = results[name]

                    # If lengths don't match, make excel_vals the same length as py_vals
                    if len(excel_vals) != len(py_vals):
                        if len(excel_vals) > len(py_vals):
                            excel_vals = excel_vals[: len(py_vals)]

                    # Change None values to 0 in excel_vals
                    for i in range(len(excel_vals)):
                        if excel_vals[i] is None:
                            excel_vals[i] = 0

                    #   if len(excel_vals) != len(py_vals):
                    #       print("🔸", name, "lengths don't match")
                    #       print("Excel:", excel_vals)
                    #       print("Python:", py_vals)
                    #   elif compare_lists(name, excel_vals, py_vals):
                    if compare_lists(name, excel_vals, py_vals):
                        print("✅", name)
                # If the cell is not a range, check that the value in the cell matches the value in the results dictionary
                else:
                    value = wb[sheet][cell].value
                    if compare_value(name, value, results[name]):
                        print("✅", name)
            else:
                # 2D array
                sheet = parts[0]
                excel_cell_ranges = parts[1:]
                py_val_ranges = results[name]
                # If lengths don't match, make excel_cell_ranges the same length as py_val_ranges
                if len(excel_cell_ranges) != len(py_val_ranges):
                    if len(excel_cell_ranges) > len(py_val_ranges):
                        excel_cell_ranges = excel_cell_ranges[: len(py_val_ranges)]
                for i in range(len(excel_cell_ranges) - 1):
                    cell_range = excel_cell_ranges[i].strip()
                    cells = wb[sheet][cell_range]
                    values = list(map(lambda x: x[0].value, cells))
                    corresponding_result = py_val_ranges[i]
                    if compare_lists(name, values, corresponding_result):
                        print("✅", name)


if __name__ == "__main__":

    def check_smr_with_cc():
        input_filename = "default-smr-natural-gas-with-cc.json"
        excel_filename = "current-central-steam-methane-reforming-with-co2-sequestration-version-aug-22.xlsm"
        check_formulas(input_filename, excel_filename)

    def check_smr_no_cc():
        input_filename = "default-smr-natural-gas-no-cc.json"
        excel_filename = "current-central-steam-methane-reforming-without-co2-sequestration-version-aug22.xlsm"
        check_formulas(input_filename, excel_filename)

    def check_atr_with_cc():
        input_filename = "default-autothermal-reforming-natural-gas-with-cc.json"
        excel_filename = "current-central-authothermal-reforming-of-natural-gas-with-co2-sequestration-version-aug22.xlsm"
        check_formulas(input_filename, excel_filename)

    def check_pem_electrolysis():
        input_filename = "default-pem-electrolysis.json"
        excel_filename = "current-central-pem-electrolysis-version-nov20.xlsm"
        check_formulas(input_filename, excel_filename)

    def check_solid_oxide_electrolysis():
        input_filename = "default-solid-oxide-electrolysis.json"
        excel_filename = "current-central-solid-oxide-electrolysis-version-nov20.xlsm"
        check_formulas(input_filename, excel_filename)

    def check_all():
        # check_smr_no_cc()
        # print("----------------------------------------")
        # check_smr_with_cc()
        # print("----------------------------------------")
        # check_atr_with_cc()
        check_pem_electrolysis()
        sys.exit()

    if len(sys.argv) > 1:
        if sys.argv[1] == "smr-with-cc":
            check_smr_with_cc()
        elif sys.argv[1] == "smr-no-cc":
            check_smr_no_cc()
        elif sys.argv[1] == "atr":
            check_atr_with_cc()
        elif sys.argv[1] == "pem":
            check_pem_electrolysis()
        elif sys.argv[1] == "soe":
            check_solid_oxide_electrolysis()
        else:
            check_all()
    else:
        check_all()
