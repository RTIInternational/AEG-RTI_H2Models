#
# This file is programmatically generated by py_writer.py; do not edit
#
from h2a.helpers import concat, get, split
from h2a.ref_tables import conversion_factor, upstream_energy_and_emissions


def calculate_energy_input_for_feedstock(feedstock):
    """Get the energy input value for a feedstock"""
    return get(feedstock, "usage") * conversion_factor(
        concat(get(split(get(feedstock, "units"), "/"), 0), "_to_$/GJ")
    )


def get_energy_input_for_feedstocks(feedstocks):
    """Get a dataframe of the energy input value for each feedstock"""
    return list(
        map(
            lambda feedstock: calculate_energy_input_for_feedstock(feedstock),
            feedstocks,
        )
    )


def calculate_upstream_energy_usage_for_feedstock_and_energy_column(
    column_name, feedstock, energy_input
):
    """Get the upstream energy usage for a feedstock"""
    return (
        energy_input
        / 1000000
        * get(get(upstream_energy_and_emissions, column_name), get(feedstock, "name"))
    )


def iterate_over_energy_columns_for_feedstock(
    feedstock, energy_input, upstream_energy_usage_column_names
):
    """Iterate over the energy columns for a feedstock"""
    return list(
        map(
            lambda column_name: calculate_upstream_energy_usage_for_feedstock_and_energy_column(
                column_name, feedstock, energy_input
            ),
            upstream_energy_usage_column_names,
        )
    )


def get_upstream_energy_usage_for_feedstocks(
    feedstocks, energy_input_GJ_per_kg_h2, upstream_energy_usage_column_names
):
    """Get the upstream energy usage for the feedstocks"""
    return list(
        map(
            lambda feedstock, energy_input: iterate_over_energy_columns_for_feedstock(
                feedstock, energy_input, upstream_energy_usage_column_names
            ),
            feedstocks,
            energy_input_GJ_per_kg_h2,
        )
    )