#
# This file is programmatically generated by py_writer.py; do not edit
#
def calculate_salvage_value(year, inflation_price_increase_factor, salvage, plant_life):
    if year == plant_life:
        return inflation_price_increase_factor * salvage
    else:
        return 0


def get_salvage_column(
    operation_range, inflation_price_increase_factors, salvage, plant_life
):
    """Salvage Value column"""
    return list(
        map(
            lambda year, inflation_price_increase_factor: calculate_salvage_value(
                year, inflation_price_increase_factor, salvage, plant_life
            ),
            operation_range,
            inflation_price_increase_factors,
        )
    )