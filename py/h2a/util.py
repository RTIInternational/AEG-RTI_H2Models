import os

# Get project root directory
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

NUM_DECIMALS = 3

# Validation function used by check_formulas.py
def compare_lists(name, excel_vals, py_vals):
    # For excel_vals, convert None to 0
    excel_vals = [0 if x is None else x for x in excel_vals]

    # For both excel_vals and py_vals, round to 4 decimal places
    excel_vals = [round(x, NUM_DECIMALS) for x in excel_vals]
    py_vals = [round(x, NUM_DECIMALS) for x in py_vals]
    
    try:
        # Iterate through each value in excel_vals and py_vals and compare if the values are within 1% of each other
        # (Also account for 'divide by 0' errors)
        for i in range(len(excel_vals)):
            if excel_vals[i] == 0:
                assert py_vals[i] == 0
            else:
                assert abs(excel_vals[i] - py_vals[i]) / excel_vals[i] < 0.01
        return True
    except AssertionError:
        # Print each value side by side
        print("❌", name)
        print("Excel", "Python")
        for i in range(len(excel_vals)):
            print(excel_vals[i], py_vals[i])
        return False

# Validation function used by check_formulas.py
def compare_value(name, excel_val, py_val):
    # Convert None to 0
    excel_val = 0 if excel_val is None else excel_val

    # For both excel_val and py_val, round to 4 decimal places
    excel_val = round(excel_val, NUM_DECIMALS)
    py_val = round(py_val, NUM_DECIMALS)
    
    try:
        assert excel_val == py_val
        return True
    except AssertionError:
        # Print each value side by side
        print("❌", name)
        print("   Excel: ", excel_val)
        print("   Python:", py_val)
        return False