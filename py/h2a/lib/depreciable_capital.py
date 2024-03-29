#
# This file is programmatically generated by py_writer.py; do not edit
#
from h2a.helpers import TRUE


def calculate_annual_depreciable_capital(
    year, replacement_cost_for_year, total_initial_depreciable_capital
):
    """Calculate the annual depreciable capital for a given year"""
    if year < 0:
        return 0
    elif year == 1:
        return total_initial_depreciable_capital - replacement_cost_for_year
    else:
        return -replacement_cost_for_year


def get_annual_depreciable_capital(
    operation_range, replacement_costs, total_initial_depreciable_capital
):
    """Get the annual depreciable capital column of the depreciation calculation table"""
    return list(
        map(
            lambda year, replacement_cost_for_year: calculate_annual_depreciable_capital(
                year, replacement_cost_for_year, total_initial_depreciable_capital
            ),
            operation_range,
            replacement_costs,
        )
    )
