#
# This file is programmatically generated by py_writer.py; do not edit
#
from h2a.helpers import append, get


def calculate_working_cap_reserve_for_year(
    year,
    i,
    WorkingCap,
    fixed_cost,
    feedstock_cost,
    other_raw_material_cost,
    variable_cost,
):
    """Calculate the cash from working capital reserve for a given year"""
    if year < 0:
        return 0
    else:
        return WorkingCap * (
            (
                get(fixed_cost, i)
                + get(feedstock_cost, i)
                + get(other_raw_material_cost, i)
                + get(variable_cost, i)
            )
            - (
                get(fixed_cost, i - 1)
                + get(feedstock_cost, i - 1)
                + get(other_raw_material_cost, i - 1)
                + get(variable_cost, i - 1)
            )
        )


def get_working_cap_reserve_rows(
    operation_range,
    analysis_index_range,
    WorkingCap,
    fixed_cost_column,
    total_feedstock_cost_column,
    other_raw_material_cost_column,
    variable_cost_column,
):
    """Get the rows for the working capital reserve"""
    return list(
        map(
            lambda year, i: calculate_working_cap_reserve_for_year(
                year,
                i,
                WorkingCap,
                fixed_cost_column,
                total_feedstock_cost_column,
                other_raw_material_cost_column,
                variable_cost_column,
            ),
            operation_range,
            analysis_index_range,
        )
    )


def get_working_cap_reserve_column(working_cap_reserve_rows):
    """Get the column for the working capital reserve"""
    return append(working_cap_reserve_rows, -sum(working_cap_reserve_rows))