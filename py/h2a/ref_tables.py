import os
import csv
import json
import pandas as pd
from .util import root_dir


# Function that reads data/fuel-heating-values/fuel-heating-values.csv and returns two dictionaries
# {fuel_name: lower_heating_value} and {fuel_name: higher_heating_value}
def read_fuel_heating_values():
    lower_heating_values = {}
    higher_heating_values = {}
    with open(
        os.path.join(root_dir, "data/fuel-heating-values/fuel-heating-values.csv"),
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
        os.path.join(root_dir, "data/conversion/conversions.csv"), newline=""
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
def read_aeo():
    df = pd.read_csv(os.path.join(root_dir, "data/aeo_orig/2017.csv"), index_col=0)
    return {"AEO_2017_Reference_Case": df}


all_aeo = read_aeo()


# def get_aeo(price_table):
#     if price_table != "AEO_2017_Reference_Case":
#         raise Exception(f"Price table '{price_table}' not supported.")
#     return all_aeo[price_table]


# Function that reads data/chemical-price-index/price-index-orig.csv and returns a dictionary
# {year: price_index}
def read_chemical_price_index():
    chemical_price_index = {}
    with open(
        os.path.join(root_dir, "data/chemical-price-index/price-index-orig.csv"),
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
            root_dir, "data/non-energy-material-prices/non-energy-material-prices.csv"
        ),
        index_col=0,
    )
    return df


def read_plant_cost_index():
    plant_cost_index = {}
    with open(
        os.path.join(root_dir, "data/plant-cost-index/plant-cost-index.csv"),
        newline="",
    ) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # skip the first row
        for row in reader:
            if row[0].startswith("#"):
                continue
            year, value = row
            plant_cost_index[int(year)] = float(value)
    return plant_cost_index


def read_consumer_price_index():
    consumer_price_indices = {}
    filenames = ["deflator-orig.csv", "deflator-soe.csv"]
    for filename in filenames:
        with open(
            os.path.join(root_dir, f"data/gdp-implicit-price-deflator/{filename}"),
            newline="",
        ) as csvfile:
            consumer_price_indices[filename] = {}
            reader = csv.reader(csvfile)
            next(reader)  # skip the first row
            for row in reader:
                if row[0].startswith("#"):
                    continue
                year, value = row
                consumer_price_indices[filename][int(year)] = float(value)
    return consumer_price_indices


def read_labor_index():
    labor_indices = {}
    filenames = ["labor-index.csv", "labor-index-soe.csv"]
    for filename in filenames:
        with open(
            os.path.join(root_dir, f"data/labor-index/{filename}"),
            newline="",
        ) as csvfile:
            labor_indices[filename] = {}
            reader = csv.reader(csvfile)
            next(reader)  # skip the first row
            for row in reader:
                if row[0].startswith("#"):
                    continue
                year, value = row
                labor_indices[filename][int(year)] = float(value)
    return labor_indices


def read_macrs_depreciation_table():
    # Read the column headers as integers
    csv_path = os.path.join(root_dir, "data/macrs/macrs-depreciation-table.csv")
    df = pd.read_csv(csv_path, index_col=0, header=0, names=[3, 5, 7, 10, 15, 20], dtype={3:float, 5:float, 7:float, 10:float, 15:float, 20:float})
    return df

def read_upstream_energy_and_emissions():
    # Read the column headers as integers
    csv_path = os.path.join(root_dir, "data/emissions/table-c1-2010-upstream-energy-and-emissions.csv")
    df = pd.read_csv(csv_path, index_col=0, header=0)
    return df

def read_co2_emissions_factors():
    csv_path = os.path.join(root_dir, "data/emissions/table-a-col-k-energy-feedstock-emissions.csv")
    df = pd.read_csv(csv_path, index_col=0, header=0)
    return df

lhv, hhv = read_fuel_heating_values()
conversion_factors = read_conversion_factors()
plant_cost_index = read_plant_cost_index()
consumer_price_index = read_consumer_price_index()
non_energy_material_prices = read_non_energy_material_prices()
chemical_price_index = read_chemical_price_index()
labor_index = read_labor_index()
get_lhv = lambda fuel: lhv[fuel]
get_labor_index = lambda year, labor_file: labor_index[labor_file][year]
conversion_factor = lambda from_to: conversion_factors[from_to]
get_plant_cost_index = lambda year: plant_cost_index[year]
get_cpi = lambda year, cpi_file: consumer_price_index[cpi_file][year]
get_aeo = (
    lambda price_table: all_aeo[price_table]
    if price_table == "AEO_2017_Reference_Case"
    else Exception(f"Price table '{price_table}' not supported.")
)
macrs_depreciation_table = read_macrs_depreciation_table()
get_macrs = lambda year, depr_length: macrs_depreciation_table[depr_length][year]
get_macrs_col = lambda depr_length: macrs_depreciation_table[depr_length]
upstream_energy_and_emissions = read_upstream_energy_and_emissions()
co2_emission_factors = read_co2_emissions_factors()
# print(upstream_energy_and_emissions["Total Energy"]["Industrial Electricity"])
# print(macrs_depreciation_table["3"])
