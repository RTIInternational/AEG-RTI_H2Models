import os
import csv
import json
from dataclasses import dataclass
from simpleeval import simple_eval
import pandas as pd

# from numpy_financial import npv


@dataclass
class Input:
    input_type: str
    input_name: str
    label: str
    description: str
    orig_name: str


@dataclass
class Formula:
    name: str
    label: str
    formula: str
    orig_name: str


# Get project root directory
rootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Function that reads data/input/default/default-smr-natural-gas-no-cc.json and returns a dictionary {[input_name:str]: input_value}
def read_default_inputs_json(json_file):
    default_inputs = {}
    with open(
        os.path.join(rootDir, "data/input/default", json_file), newline=""
    ) as jsonfile:
        data = json.load(jsonfile)
        for key, value in data.items():
            default_inputs[key] = value
    return default_inputs


# Function that reads inputs.csv and returns a dictionary of Input objects
def read_inputs():
    inputs = {}
    with open(os.path.join(rootDir, "data/input/inputs.csv"), newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip the first row
        for row in reader:
            if row[0].startswith("#"):
                continue
            input_type, input_name, label, description, orig_name = row
            name = input_name if input_name else orig_name
            inputs[name] = Input(input_type, input_name, label, description, orig_name)
    return inputs


# Function that reads data/formula/formulas.csv and returns a list of Formula objects
def read_formulas():
    formulas = []
    with open(
        os.path.join(rootDir, "data/formula/formulas.csv"), newline=""
    ) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip the first row
        for row in reader:
            if row[0].startswith("#"):
                continue
            name, label, formula, orig_name = row
            formulas.append(Formula(name, label, formula, orig_name))
    return formulas


# Function that reads data/fuel-heating-values/fuel-heating-values.csv and returns two dictionaries
# {fuel_name: lower_heating_value} and {fuel_name: higher_heating_value}
def read_fuel_heating_values():
    lower_heating_values = {}
    higher_heating_values = {}
    with open(
        os.path.join(rootDir, "data/fuel-heating-values/fuel-heating-values.csv"),
        newline="",
    ) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip the first row
        for row in reader:
            if row[0].startswith("#"):
                continue
            fuel_type, fuel, lhv_mj_per_kg, hhv_mj_per_kg = row
            lower_heating_values[fuel] = float(lhv_mj_per_kg)
            higher_heating_values[fuel] = float(hhv_mj_per_kg)
    return lower_heating_values, higher_heating_values


# Function that reads data/conversion/conversions.csv and returns a dictionary
# {conversion_name: conversion_value}
def read_conversion_factors():
    conversions = {}
    with open(
        os.path.join(rootDir, "data/conversion/conversions.csv"), newline=""
    ) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip the first row
        for row in reader:
            if row[0].startswith("#"):
                continue
            conversion_type, from_unit, to_unit, factor, factor_units, note = row
            conversion_name = f"{from_unit}_to_{to_unit}" if to_unit else from_unit
            conversions[conversion_name] = float(factor)
    return conversions


# Function that uses pandas to read data/aeo_orig/2017.csv and returns a dataframe
def read_aeo(price_table):
    if price_table != "AEO_2017_Reference_Case":
        raise Exception(f"Price table '{price_table}' not supported.")
    df = pd.read_csv(os.path.join(rootDir, "data/aeo_orig/2017.csv"), index_col=0)
    return df


# Function that reads data/chemical-price-index/price-index-orig.csv and returns a dictionary
# {year: price_index}
def read_chemical_price_index():
    chemical_price_index = {}
    with open(
        os.path.join(rootDir, "data/chemical-price-index/price-index-orig.csv"),
        newline="",
    ) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip the first row
        for row in reader:
            if row[0].startswith("#"):
                continue
            year, price_index = row
            chemical_price_index[int(year)] = float(price_index)
    return chemical_price_index


# Function that uses pandas to read data/non-energy-material-prices/non-energy-material-prices.csv and returns a dataframe
def read_non_energy_material_prices():
    df = pd.read_csv(
        os.path.join(
            rootDir, "data/non-energy-material-prices/non-energy-material-prices.csv"
        ),
        index_col=0,
    )
    return df


def main():
    inputs = read_inputs()
    default_inputs = read_default_inputs_json("default-smr-natural-gas-no-cc.json")
    formulas = read_formulas()
    lhv, hhv = read_fuel_heating_values()
    conversion_factors = read_conversion_factors()
    lookup_dict = default_inputs.copy()
    funcs = {
        "get_lhv": lambda fuel: lhv[fuel],
        "conversion_factor": lambda from_to: conversion_factors[from_to],
    }

    # For each formula, evaluate the formula and add the result to the lookup dictionary
    for f in formulas:
        val = simple_eval(f.formula, names=lookup_dict, functions=funcs)
        name = f.name if f.name else f.orig_name
        lookup_dict[name] = val

    # The costs from the AEO are converted to an LHV basis for use in H2A
    # The calculations for these conversions are below.
    # The price data is updated to the H2A reference year by multiplying by:
    # - The deflator price index from Table B for the H2A reference year from Table A/deflator price index for AEO data year
    # - The price data is converted from HH to LHV by multiplying by the ratio of the HHV to the LHV from Table A (e.g. 1.055 for natural gas, 0.0036 for electricity)
    # - Finally, the price is converted from an mmBTU basis to J basis by dividing by the conversion factor

    analysis_range = range(
        lookup_dict["analysis_period_start"], lookup_dict["analysis_period_end"]
    )

    # Calculate the feedstock cost for a given year
    def get_feedstock_year_price(feedstock, aeo, conversion_factor, year):
        price_for_year = aeo[feedstock["name"]][year]
        return (
            lookup_dict["INFLATION_FACTOR"]
            * feedstock["usage"]
            * price_for_year
            * conversion_factor
        )

    # Get feedstock prices for all years in the analysis period
    def get_feedstock_prices(feedstock):
        unit = feedstock["units"].split("/")[0]
        aeo = read_aeo(feedstock["price_table"])
        conversion_factor = conversion_factors[f"{unit}_to_$/GJ"]
        price_in_startup_year = (
            aeo[feedstock["name"]][default_inputs["startup_year"]] * conversion_factor
        )
        return (
            [
                get_feedstock_year_price(feedstock, aeo, conversion_factor, year)
                for year in analysis_range
            ]
            if feedstock["lookup_prices"]
            else [
                lookup_dict["INFLATION_FACTOR"]
                * feedstock["usage"]
                * price_in_startup_year
            ]
            * len(analysis_range)
        )

    # Table 1: Price per kg H2
    feedstock_price_df = [
        get_feedstock_prices(feedstock) for feedstock in default_inputs["feedstocks"]
    ]

    def get_operation_range(num_analysis_years, construct):
        # If construction time is 0, year 1 is the first year of operation
        operation_years = [1 if construct == 0 else -construct]
        for _ in range(num_analysis_years - 1):
            previous_year = operation_years[-1]
            if previous_year == -1:
                operation_years.append(1)
            else:
                operation_years.append(previous_year + 1)
        return operation_years

    operation_range = get_operation_range(len(analysis_range), lookup_dict["construct"])

    def get_inflation_price_increase_factors():
        return [
            (1 + default_inputs["inflation_rate"])
            ** (year - default_inputs["startup_year"])
            for year in analysis_range
        ]

    inflation_price_increase_factors = get_inflation_price_increase_factors()

    def calculate_feedstock_yearly_cost_for_year(
        operation_year, price, inflation_price_increase_factor
    ):
        if operation_year < 0:
            return 0
        elif operation_year == 1 and default_inputs["start_time"] < 1:
            sum_val = (
                price
                * lookup_dict["plant_output_kg_per_year"]
                * inflation_price_increase_factor
                * default_inputs["percnt_var"]
                * default_inputs["start_time"]
            ) + (
                price
                * lookup_dict["plant_output_kg_per_year"]
                * inflation_price_increase_factor
                * (1 - default_inputs["start_time"])
            )
            return (-1) * sum_val
        elif operation_year <= default_inputs["start_time"]:
            return (
                price
                * lookup_dict["plant_output_kg_per_year"]
                * inflation_price_increase_factor
                * default_inputs["percnt_var"]
            )
        else:
            return (
                price
                * lookup_dict["plant_output_kg_per_year"]
                * inflation_price_increase_factor
            )

    # Table 2: Total cost per year
    def get_feedstock_yearly_cost_by_year(
        operation_range, feedstock_price_list, inflation_price_increase_factors
    ):
        ret_vals = []
        for i, operation_year in enumerate(operation_range):
            ret_vals.append(
                calculate_feedstock_yearly_cost_for_year(
                    operation_year,
                    feedstock_price_list[i],
                    inflation_price_increase_factors[i],
                )
            )
        return ret_vals

    # Column: Feedstock Cost
    def get_all_feedstocks_yearly_cost_by_year(
        operation_range, feedstock_price_df, inflation_price_increase_factors
    ):
        ret_vals = []
        for i, operation_year in enumerate(operation_range):
            # Sum the prices for each feedstock in the feedstock_price_df for the given year
            feedstock_price_list = [feedstock[i] for feedstock in feedstock_price_df]
            feedstock_price_for_year_per_kg_h2 = sum(feedstock_price_list)
            ret_vals.append(
                calculate_feedstock_yearly_cost_for_year(
                    operation_year,
                    feedstock_price_for_year_per_kg_h2,
                    inflation_price_increase_factors[i],
                )
            )
        return ret_vals

    total_feedstock_cost_column = get_all_feedstocks_yearly_cost_by_year(
        operation_range, feedstock_price_df, inflation_price_increase_factors
    )
    # print(total_feedstock_cost_column)

    def npv(r, cfList):
        sum_pv = 0
        for i, pmt in enumerate(cfList, start=1):
            sum_pv += pmt / ((1 + r) ** i)
        return sum_pv

    for feedstock in feedstock_price_df:
        yearly_cost_by_year = get_feedstock_yearly_cost_by_year(
            operation_range, feedstock, inflation_price_increase_factors
        )
        # NPV: Since the first cash flow occurs at the beginning of the first period,
        # the first value is added to the NPV result, not included in the values arguments.
        discounted_value = yearly_cost_by_year[0] + npv(
            lookup_dict["target_after_tax_nominal_irr"], yearly_cost_by_year[1:]
        )
        # X below depends on cell AE116 in the spreadsheet, PV of cash flow for H2 sales (in kg/year)
        # cost_per_kg_h2 = discounted_value / X * (1 + lookup_dict["inflation_rate"]) ** (constuct/lookup_dict["INFLATION_FACTOR"])

    # End of feedstock cost calculations

    non_energy_material_prices = read_non_energy_material_prices()
    chemical_price_index = read_chemical_price_index()

    # Other Materials and Byproducts

    def get_other_material_prices(other_material, num_analysis_years):
        price_source_year = non_energy_material_prices["Source Data Year"][
            other_material["name"]
        ]
        price_index_in_source_year = chemical_price_index[price_source_year]
        price_index_in_ref_year = chemical_price_index[default_inputs["ref_year"]]
        conversion_factor = price_index_in_ref_year / price_index_in_source_year
        price_in_startup_year = (
            non_energy_material_prices["Price"][other_material["name"]]
            * conversion_factor
        )
        if True:  # other_material["lookup_prices"]:
            # FYI: Since every year has the same value, lookup_prices does nothing
            return [
                lookup_dict["INFLATION_FACTOR"]
                * other_material["usage"]
                * price_in_startup_year
            ] * num_analysis_years

    for other_material in default_inputs["other_materials"]:
        print(
            other_material["name"],
            get_other_material_prices(other_material, len(analysis_range)),
        )


if __name__ == "__main__":
    main()
