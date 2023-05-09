#
# This file is programmatically generated by py_writer.py; do not edit
#
from h2a.helpers import YEAR_1, get, length


def access(i, table, row):
    """Safely access a value in a table"""
    if row - i >= YEAR_1 and row - i < length(get(table, i)):
        return get(get(table, i), row - i)
    else:
        return 0


def diagonal(table, row, recovery_index_range):
    """Get the diagonal cells of a table given a row, e.g. diagonal(table, 2, 3) returns [table[0,2], table[1,1], table[2,0]]"""
    return list(map(lambda i: access(i, table, row), recovery_index_range))


def calculate_depreciation_charge(
    year, recovery_index_range, depreciation_calculation_table
):
    """Calculate the depreciation charge for a given year by summing the diagonal"""
    return sum(diagonal(depreciation_calculation_table, year, recovery_index_range))


def get_depreciation_charges(
    analysis_index_range, recovery_index_range, depreciation_calculation_table
):
    """Get the depreciation charges"""
    return list(
        map(
            lambda year: calculate_depreciation_charge(
                year, recovery_index_range, depreciation_calculation_table
            ),
            analysis_index_range,
        )
    )


def get_depr_charge(
    charge, i, total_remaining_depreciation_charges, anal_period, construct
):
    """Get the depreciation charge"""
    if i == anal_period + construct - 1:
        return -charge - total_remaining_depreciation_charges
    else:
        return -charge


def get_depreciation_charges_column(
    depreciation_charges,
    analysis_index_range,
    total_remaining_depreciation_charges,
    anal_period,
    construct,
):
    """Get the depreciation charges column for the Cash Flow Analysis"""
    return list(
        map(
            lambda charge, i: get_depr_charge(
                charge, i, total_remaining_depreciation_charges, anal_period, construct
            ),
            depreciation_charges,
            analysis_index_range,
        )
    )
