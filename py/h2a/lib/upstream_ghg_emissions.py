#
# This file is programmatically generated by py_writer.py; do not edit
#
from h2a.helpers import FIRST, SECOND, THIRD, get
from h2a.ref_tables import upstream_energy_and_emissions


def calculate_ghg_emission_for_feedstock_and_ghg_column(
    column_name, feedstock, energy_input
):
    """Get the ghg emission for a feedstock"""
    return energy_input * get(
        get(upstream_energy_and_emissions, column_name), get(feedstock, "name")
    )


def iterate_over_ghg_columns_for_feedstock(
    feedstock, energy_input, greenhouse_gas_column_names
):
    """Iterate over the ghg columns for a feedstock"""
    return list(
        map(
            lambda column_name: calculate_ghg_emission_for_feedstock_and_ghg_column(
                column_name, feedstock, energy_input
            ),
            greenhouse_gas_column_names,
        )
    )


def get_upstream_ghg_emissions_for_feedstocks(
    feedstocks, energy_input_GJ_per_kg_h2, greenhouse_gas_column_names
):
    """Get upstream GHG emissions for feedstocks"""
    return list(
        map(
            lambda feedstock, energy_input: iterate_over_ghg_columns_for_feedstock(
                feedstock, energy_input, greenhouse_gas_column_names
            ),
            feedstocks,
            energy_input_GJ_per_kg_h2,
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


def get_upstream_total_ghg_emissions_for_feedstocks(
    upstream_ghg_emissions_kg_per_kg_h2, GHG_CO2_factor, GHG_CH4_factor, GHG_N2O_factor
):
    """Get upstream total GHG emissions for feedstocks"""
    return list(
        map(
            lambda emission: calculate_total_ghg_emission_for_feedstock(
                emission, GHG_CO2_factor, GHG_CH4_factor, GHG_N2O_factor
            ),
            upstream_ghg_emissions_kg_per_kg_h2,
        )
    )
