#
# This file is programmatically generated by py_writer.py; do not edit
#
from h2a.helpers import get, length


def calculate_feedstock_cost_for_year(
    year,
    price,
    inflation_price_increase_factor,
    start_time,
    plant_output_kg_per_year,
    percnt_var,
):
    """Calculate the cost of a feedstock for a given year"""
    if year < 0:
        return 0
    elif year == 1 and start_time < 1:
        return -(
            (
                price
                * plant_output_kg_per_year
                * inflation_price_increase_factor
                * percnt_var
                * start_time
            )
            + (
                price
                * plant_output_kg_per_year
                * inflation_price_increase_factor
                * (1 - start_time)
            )
        )
    elif year <= start_time:
        return -(
            price
            * plant_output_kg_per_year
            * inflation_price_increase_factor
            * percnt_var
        )
    else:
        return -(price * plant_output_kg_per_year * inflation_price_increase_factor)


def get_feedstock_costs(
    years,
    prices,
    inflation_price_increase_factors,
    start_time,
    plant_output_kg_per_year,
    percnt_var,
):
    """Calculate the cost of a feedstock over a range of years"""
    return list(
        map(
            lambda year, price, inflation_price_increase_factor: calculate_feedstock_cost_for_year(
                year,
                price,
                inflation_price_increase_factor,
                start_time,
                plant_output_kg_per_year,
                percnt_var,
            ),
            years,
            prices,
            inflation_price_increase_factors,
        )
    )


def feedstock_prices_from_df(feedstock_price_df, i):
    """For a given year (i), return price of each feedstock"""
    return list(map(lambda feedstock: get(feedstock, i), feedstock_price_df))


def get_total_feedstock_costs(
    operation_range,
    feedstock_price_df,
    inflation_price_increase_factors,
    start_time,
    plant_output_kg_per_year,
    percnt_var,
):
    """Calculate the total cost of all feedstocks over a range of years"""
    return list(
        map(
            lambda year: calculate_feedstock_cost_for_year(
                get(operation_range, year),
                sum(feedstock_prices_from_df(feedstock_price_df, year)),
                get(inflation_price_increase_factors, year),
                start_time,
                plant_output_kg_per_year,
                percnt_var,
            ),
            range(length(operation_range)),
        )
    )
