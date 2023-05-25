import sys
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

from openpyxl import load_workbook
from run import run_model
from h2a.util import compare_lists, compare_value
from h2a.read_input import read_formulas_json


def check_formulas(input_filename, excel_filename):
  formulas = read_formulas_json()

  results = run_model(input_filename)
  wb = load_workbook(filename = excel_filename, data_only=True)

  # For each formula with an excel_loc with a comma, split the string to get the sheet and cell/range
  # Then check that the value in the cell/range matches the value in the results dictionary
  for formula in formulas:
      if "excel_loc" in formula and "," in formula["excel_loc"]:
          name = (
              formula["name"]
              if "name" in formula and formula["name"] != ""
              else formula["orig_name"]
          )
          parts = formula["excel_loc"].split(",")
          if len(parts) == 2:
              sheet, cell = parts
              cell = cell.strip()
              # If excel_filename is "current-central-steam-methane-reforming-with-co2-sequestration-version-aug-22.xlsm"
              # and the sheet is "Input_Sheet_Template" and the cell row is greater than 90, subtract 1 from the row
              if ((excel_filename == "current-central-steam-methane-reforming-with-co2-sequestration-version-aug-22.xlsm"
                   or excel_filename == "current-central-authothermal-reforming-of-natural-gas-with-co2-sequestration-version-aug22.xlsm")
                  and sheet == "Input_Sheet_Template" and int(cell[1:]) > 90):
                  cell = cell[0] + str(int(cell[1:])-1)

              if excel_filename == "current-central-steam-methane-reforming-without-co2-sequestration-version-aug22.xlsm" and sheet == "Carbon Sequestration":
                  continue # No use in checking unused formulas

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
          else:
              # 2D array
              sheet = parts[0]
              cell_ranges = parts[1:]
              for i in range(len(cell_ranges) - 1):
                  cell_range = cell_ranges[i].strip()
                  cells = wb[sheet][cell_range]
                  values = list(map(lambda x: x[0].value, cells))
                  corresponding_result = results[name][i]
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

    def check_all():
        check_smr_no_cc()
        print("----------------------------------------")
        check_smr_with_cc()
        print("----------------------------------------")
        check_atr_with_cc()
        sys.exit()

    if len(sys.argv) > 1:
        if sys.argv[1] == "smr-with-cc":
            check_smr_with_cc()
        elif sys.argv[1] == "smr-no-cc":
            check_smr_no_cc()
        elif sys.argv[1] == "atr":
            check_atr_with_cc()
        else:
            check_all()
    else:
        check_all()