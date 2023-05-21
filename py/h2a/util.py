import os

# Get project root directory
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Validation function used by check_formulas.py
def check(excel_vals, py_vals):
    # For excel_vals, convert None to 0
    excel_vals = [0 if x is None else x for x in excel_vals]

    # For both excel_vals and py_vals, round to 4 decimal places
    excel_vals = [round(x, 4) for x in excel_vals]
    py_vals = [round(x, 4) for x in py_vals]
    
    try:
        assert excel_vals == py_vals
    except AssertionError:
        # Print each value side by side
        print("Excel", "Python")
        for i in range(len(excel_vals)):
            print(excel_vals[i], py_vals[i])