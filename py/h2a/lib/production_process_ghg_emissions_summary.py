#
# This file is programmatically generated by py_writer.py; do not edit
#
from h2a.helpers import FIRST, get, length, round_num, sum_args


def convert_to_metric_tons_per_year(emission, plant_output_kg_per_year):
    """Converts a value in kg per kg H2 to metric tons per year"""
    return round_num(emission * plant_output_kg_per_year / 1000, -2)


def get_total_in_metric_tons_per_year(
    total_process_pollutants_produced_kg_per_kg_h2, plant_output_kg_per_year
):
    """Convert total emissions for each GHG to metric tons per year"""
    return list(
        map(
            lambda emission: convert_to_metric_tons_per_year(
                emission, plant_output_kg_per_year
            ),
            total_process_pollutants_produced_kg_per_kg_h2,
        )
    )


def calculate_co2_captured_kg_per_kg_h2(
    i, total_feedstock_pollutants_produced_kg_per_kg_h2, CO2_Capture_Efficiency
):
    """Calculates the amount of CO2 captured per kg of H2 produced"""
    if i == FIRST:
        return (
            get(total_feedstock_pollutants_produced_kg_per_kg_h2, i)
            * CO2_Capture_Efficiency
        )
    else:
        return 0


def get_co2_captured_kg_per_kg_h2(
    total_feedstock_pollutants_produced_kg_per_kg_h2, CO2_Capture_Efficiency
):
    """Gets the amount of CO2 captured per kg of H2 produced for CO2, returns 0 other GHGs"""
    return list(
        map(
            lambda i: calculate_co2_captured_kg_per_kg_h2(
                i,
                total_feedstock_pollutants_produced_kg_per_kg_h2,
                CO2_Capture_Efficiency,
            ),
            range(length(total_feedstock_pollutants_produced_kg_per_kg_h2)),
        )
    )


def get_co2_captured_metric_tons_per_year(
    co2_captured_kg_per_kg_h2, plant_output_kg_per_year
):
    """Gets the amount of CO2 captured in metric tons per year"""
    return list(
        map(
            lambda captured: convert_to_metric_tons_per_year(
                captured, plant_output_kg_per_year
            ),
            co2_captured_kg_per_kg_h2,
        )
    )


def subtract(amount_produced, amount_captured):
    """Subtracts two values"""
    return amount_produced - amount_captured


def get_total_process_emissions_kg_per_kg_h2(
    total_process_pollutants_produced_kg_per_kg_h2, co2_captured_kg_per_kg_h2
):
    """Gets the total process emissions in kg per kg H2"""
    return list(
        map(
            lambda amount_produced, amount_captured: subtract(
                amount_produced, amount_captured
            ),
            total_process_pollutants_produced_kg_per_kg_h2,
            co2_captured_kg_per_kg_h2,
        )
    )


def get_total_process_emissions_metric_tons_per_year(
    total_process_emissions_kg_per_kg_h2, plant_output_kg_per_year
):
    """Gets the total process emissions in metric tons per year"""
    return list(
        map(
            lambda emission: convert_to_metric_tons_per_year(
                emission, plant_output_kg_per_year
            ),
            total_process_emissions_kg_per_kg_h2,
        )
    )


def get_total_well_to_pump_emissions_kg_per_kg_h2(
    total_upstream_emissions_kg_per_kg_h2, total_process_emissions_kg_per_kg_h2
):
    """Gets the total well to pump emissions in kg per kg H2"""
    return list(
        map(
            lambda upstream, process: sum_args(upstream, process),
            total_upstream_emissions_kg_per_kg_h2,
            total_process_emissions_kg_per_kg_h2,
        )
    )