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
          sheet, cell = formula["excel_loc"].split(",")
          cell = cell.strip()
          # If excel_filename is "current-central-steam-methane-reforming-with-co2-sequestration-version-aug-22.xlsm"
          # and the sheet is "Input_Sheet_Template" and the cell row is greater than 90, subtract 1 from the row
          if excel_filename == "current-central-steam-methane-reforming-with-co2-sequestration-version-aug-22.xlsm" and sheet == "Input_Sheet_Template" and int(cell[1:]) > 90:
              cell = cell[0] + str(int(cell[1:])-1)

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

if __name__ == "__main__":
    def check_with_cc():
        input_filename = "default-smr-natural-gas-with-cc.json"
        excel_filename = "current-central-steam-methane-reforming-with-co2-sequestration-version-aug-22.xlsm"
        check_formulas(input_filename, excel_filename)

    def check_no_cc():
        input_filename = "default-smr-natural-gas-no-cc.json"
        excel_filename = "current-central-steam-methane-reforming-without-co2-sequestration-version-aug22.xlsm"
        check_formulas(input_filename, excel_filename)

    def check_both():
        check_no_cc()
        print("----------------------------------------")
        check_with_cc()
        sys.exit()

    if len(sys.argv) > 1:
        if sys.argv[1] == "with-cc":
            check_with_cc()
        elif sys.argv[1] == "no-cc":
            check_no_cc()
        else:
            check_both()
    else:
        check_both()
