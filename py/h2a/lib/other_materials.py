#
# This file is programmatically generated by py_writer.py; do not edit
#
from h2a.helpers import get
from h2a.ref_tables import non_energy_material_prices, chemical_price_index


def get_other_material_price_conversion_factor(other_material, ref_year):
    """Get the conversion factor for converting Other Material prices from source year to reference year dollars"""
    return get(chemical_price_index, ref_year) / get(
        chemical_price_index,
        get(
            get(non_energy_material_prices, "Source Data Year"),
            get(other_material, "name"),
        ),
    )


def get_other_material_price_for_year(year, other_material, INFLATION_FACTOR, ref_year):
    """Calculate the price of a given Other Material for a year (although year is not used in this function)"""
    return (
        INFLATION_FACTOR
        * get(other_material, "usage")
        * (
            get(
                get(non_energy_material_prices, "Price"),
                get(other_material, "name"),
            )
            * get_other_material_price_conversion_factor(other_material, ref_year)
        )
    )


def prices_for_other_material(
    other_material, analysis_range, INFLATION_FACTOR, ref_year
):
    """Get prices for a given Other Material over a range of years"""
    return list(
        map(
            lambda year: get_other_material_price_for_year(
                year, other_material, INFLATION_FACTOR, ref_year
            ),
            analysis_range,
        )
    )


def get_other_material_price_df(
    other_materials, analysis_range, INFLATION_FACTOR, ref_year
):
    """Get a dataframe of Other Material prices over a range of years"""
    return list(
        map(
            lambda other_material: prices_for_other_material(
                other_material, analysis_range, INFLATION_FACTOR, ref_year
            ),
            other_materials,
        )
    )
