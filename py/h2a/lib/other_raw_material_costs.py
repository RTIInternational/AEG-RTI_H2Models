#
# This file is programmatically generated by py_writer.py; do not edit
#
def calculate_other_raw_material_cost(
    year, inflation_price_increase_factor, inflated_otherraw, percnt_var, start_time
):
    if year < 0:
        return 0
    elif year == 1 and start_time < 1:
        return -(
            (
                inflated_otherraw
                * inflation_price_increase_factor
                * percnt_var
                * start_time
            )
            + (inflated_otherraw * inflation_price_increase_factor * (1 - start_time))
        )
    elif year <= start_time:
        return -(inflated_otherraw * percnt_var * inflation_price_increase_factor)
    else:
        return -(inflated_otherraw * inflation_price_increase_factor)


def get_other_raw_material_cost_column(
    operation_range,
    inflation_price_increase_factors,
    inflated_otherraw,
    percnt_var,
    start_time,
):
    """Other Raw Material Cost"""
    return list(
        map(
            lambda year, inflation_price_increase_factor: calculate_other_raw_material_cost(
                year,
                inflation_price_increase_factor,
                inflated_otherraw,
                percnt_var,
                start_time,
            ),
            operation_range,
            inflation_price_increase_factors,
        )
    )
