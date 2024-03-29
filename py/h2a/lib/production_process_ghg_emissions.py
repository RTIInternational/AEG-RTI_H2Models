#
# This file is programmatically generated by py_writer.py; do not edit
#
from h2a.helpers import FIRST, SECOND, THIRD, concat, get, get_cell, split, to_num
from h2a.ref_tables import co2_emission_factors, conversion_factor


def calculate_ghg_emission_for_feedstock_and_ghg_column(column_name, feedstock):
    """Get the ghg emission for a feedstock"""
    return (
        get_cell(co2_emission_factors, get(feedstock, "name"), column_name)
        * to_num(get(feedstock, "usage"))
        * conversion_factor(
            concat(get(split(get(feedstock, "units"), "/"), FIRST), "_to_$/GJ")
        )
    )


def iterate_over_ghg_columns_for_feedstock(feedstock, greenhouse_gas_column_names):
    """Iterate over the ghg columns for a feedstock"""
    return list(
        map(
            lambda column_name: calculate_ghg_emission_for_feedstock_and_ghg_column(
                column_name, feedstock
            ),
            greenhouse_gas_column_names,
        )
    )


def get_production_process_ghg_emissions_for_feedstocks(
    feedstocks, greenhouse_gas_column_names
):
    """Get production process GHG emissions for feedstocks"""
    return list(
        map(
            lambda feedstock: iterate_over_ghg_columns_for_feedstock(
                feedstock, greenhouse_gas_column_names
            ),
            feedstocks,
        )
    )


def calculate_total_ghg_emission_for_feedstock(
    emission, GHG_CO2_factor, GHG_CH4_factor, GHG_N2O_factor
):
    """Get the ghg emission for a feedstock"""
    return (
        get(emission, FIRST) * GHG_CO2_factor
        + get(emission, SECOND) * GHG_CH4_factor
        + get(emission, THIRD) * GHG_N2O_factor
    )


def get_production_process_total_ghg_emissions_for_feedstocks(
    production_process_ghg_emissions_kg_per_kg_h2,
    GHG_CO2_factor,
    GHG_CH4_factor,
    GHG_N2O_factor,
):
    """Get production process total GHG emissions for feedstocks"""
    return list(
        map(
            lambda emission: calculate_total_ghg_emission_for_feedstock(
                emission, GHG_CO2_factor, GHG_CH4_factor, GHG_N2O_factor
            ),
            production_process_ghg_emissions_kg_per_kg_h2,
        )
    )
