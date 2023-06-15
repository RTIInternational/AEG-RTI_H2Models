#
# This file is programmatically generated by py_writer.py; do not edit
#
from h2a.helpers import get


def calculate_variable_cost_for_year(
    year,
    utility_price,
    material_price,
    inflation_price_increase_factor,
    plant_output_kg_per_year,
    percnt_var,
    start_time,
    inflated_othervar,
):
    """Calculate the variable cost for a given year"""
    if year < 0:
        return 0
    elif year == 1 and start_time < 1:
        return -(
            (
                (
                    (utility_price + material_price) * plant_output_kg_per_year
                    + inflated_othervar
                )
                * inflation_price_increase_factor
                * percnt_var
                * start_time
            )
            + (
                (utility_price + material_price)
                * plant_output_kg_per_year
                * inflation_price_increase_factor
                * (1 - start_time)
            )
        )
    elif year <= start_time:
        return (
            -(
                (utility_price + material_price) * plant_output_kg_per_year
                + inflated_othervar
            )
            * inflation_price_increase_factor
            * percnt_var
        )
    else:
        return (
            -(
                (utility_price + material_price) * plant_output_kg_per_year
                + inflated_othervar
            )
            * inflation_price_increase_factor
        )


def prices_from_df(price_df, i):
    """For a given year (i), return a list containing the price of each material"""
    return list(map(lambda prices: get(prices, i), price_df))


def get_variable_cost_column(
    operation_range,
    analysis_index_range,
    utility_price_df,
    nonenergy_material_price_df,
    inflation_price_increase_factors,
    plant_output_kg_per_year,
    percnt_var,
    start_time,
    inflated_othervar,
):
    """Other Variable Operating Costs column"""
    return list(
        map(
            lambda year, i, inflation_price_increase_factor: calculate_variable_cost_for_year(
                year,
                sum(prices_from_df(utility_price_df, i)),
                sum(prices_from_df(nonenergy_material_price_df, i)),
                inflation_price_increase_factor,
                plant_output_kg_per_year,
                percnt_var,
                start_time,
                inflated_othervar,
            ),
            operation_range,
            analysis_index_range,
            inflation_price_increase_factors,
        )
    )
