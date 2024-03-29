#
# This file is programmatically generated by py_writer.py; do not edit
#
from h2a.helpers import TRUE


def calculate_fixed_cost(
    year, inflation_price_increase_factor, inflated_fixed, percnt_fixed, start_time
):
    if year < 0:
        return 0
    elif year == 1 and start_time < 1:
        return -(
            (inflated_fixed * percnt_fixed * start_time)
            + (inflated_fixed * (1 - start_time))
        )
    elif year <= start_time:
        return -(inflated_fixed * percnt_fixed * inflation_price_increase_factor)
    else:
        return -(inflated_fixed * inflation_price_increase_factor)


def get_fixed_cost_column(
    operation_range,
    inflation_price_increase_factors,
    inflated_fixed,
    percnt_fixed,
    start_time,
):
    """Fixed Operating Costs column"""
    return list(
        map(
            lambda year, inflation_price_increase_factor: calculate_fixed_cost(
                year,
                inflation_price_increase_factor,
                inflated_fixed,
                percnt_fixed,
                start_time,
            ),
            operation_range,
            inflation_price_increase_factors,
        )
    )
