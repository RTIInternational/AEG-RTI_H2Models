#
# This file is programmatically generated by py_writer.py; do not edit
#
def calculate_decom_cost(year, inflation_price_increase_factor, decom, plant_life):
    if year == plant_life:
        return -inflation_price_increase_factor * decom
    else:
        return 0


def get_decom_costs_column(
    operation_range, inflation_price_increase_factors, decom, plant_life
):
    """Decommissioning Costs column"""
    return list(
        map(
            lambda year, inflation_price_increase_factor: calculate_decom_cost(
                year, inflation_price_increase_factor, decom, plant_life
            ),
            operation_range,
            inflation_price_increase_factors,
        )
    )
