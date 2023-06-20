import::here(here, here)
read_fuel_heating_values <- function() {
  lower_heating_values <- list()
  higher_heating_values <- list()
  csvfile <- read.csv(
    here("..", "data", "fuel-heating-values", "fuel-heating-values.csv"),
    header = TRUE
  )
  for (i in 1:nrow(csvfile)) { # nolint: seq_linter.
    row <- csvfile[i, ]
    # fuel_type <- row[1] # nolint
    fuel <- as.character(row[2])
    lhv_mj_per_kg <- as.numeric(row[3])
    hhv_mj_per_kg <- as.numeric(row[4])
    lower_heating_values[[fuel]] <- lhv_mj_per_kg
    higher_heating_values[[fuel]] <- hhv_mj_per_kg
  }
  return(list(lower_heating_values, higher_heating_values))
}

read_conversion_factors <- function() {
  conversions <- list()
  csvfile <- read.csv(here("..", "data", "conversion", "conversions.csv"),
    header = TRUE
  )
  for (i in 1:nrow(csvfile)) { # nolint: seq_linter.
    row <- csvfile[i, ]
    # conversion_type <- as.character(row[1]) # nolint
    from_unit <- as.character(row[2])
    to_unit <- as.character(row[3])
    factor <- as.numeric(row[4])
    # factor_units <- as.character(row[5]) # nolint
    # note <- as.character(row[6]) # nolint
    conversion_name <- ifelse(to_unit != "", paste(from_unit, "to", to_unit, sep = "_"), from_unit) # nolint: line_length_linter.
    conversions[[conversion_name]] <- factor
  }
  return(conversions)
}

read_aeo <- function() {
  df <- read.csv(here("..", "data", "aeo_orig", "2017.csv"), header = TRUE)
  return(list("AEO_2017_Reference_Case" = df))
}
all_aeo <- read_aeo()

get_aeo <- function(price_table) {
  if (price_table == "AEO_2017_Reference_Case") {
    return(all_aeo[[price_table]])
  } else {
    stop(paste("Price table", price_table, "not supported."))
  }
}

read_macrs_depreciation_table <- function() {
  # Read the column headers as integers
  csv_path <- here("..", "data", "macrs", "macrs-depreciation-table.csv")
  df <- read.csv(csv_path, header = TRUE, row.names = 1)
  colnames(df) <- c(3, 5, 7, 10, 15, 20)
  df <- as.data.frame(lapply(df, as.numeric))
  return(df)
}

read_upstream_energy_and_emissions <- function() {
  # Read the column headers as integers
  csv_path <- here("..", "data", "emissions", "table-c1-2010-upstream-energy-and-emissions.csv")
  df <- read.csv(csv_path, header = TRUE, row.names = 1)
  return(df)
}

read_co2_emissions_factors <- function() {
  # Read the column headers as integers
  csv_path <- here("..", "data", "emissions", "table-a-col-k-energy-feedstock-emissions.csv")
  df <- read.csv(csv_path, header = TRUE, row.names = 1)
  return(df)
}

read_labor_index <- function() {
  labor_indices <- list()
  filenames <- c("labor-index.csv", "labor-index-soe.csv")
  for (filename in filenames) {
    csv_path <- here("..", "data", "labor-index", filename)
    labor_indices[[filename]] <- data.frame(read.csv(csv_path, header = TRUE))
    labor_indices[[filename]] <- labor_indices[[filename]][-1,] # skip the first row
    labor_indices[[filename]]$X1 <- as.numeric(labor_indices[[filename]]$X1)
    labor_indices[[filename]]$X2 <- as.numeric(labor_indices[[filename]]$X2)
    colnames(labor_indices[[filename]]) <- c("year", "value")
    labor_indices[[filename]]$year <- as.integer(labor_indices[[filename]]$year)
    labor_indices[[filename]]$value <- as.numeric(labor_indices[[filename]]$value)
  }
  return(labor_indices)
}

read_chemical_price_index <- function() {
  chemical_price_index <- list()
  csvfile <- read.csv(
    here("..", "data", "chemical-price-index", "price-index-orig.csv"),
    header = TRUE
  )
  for (i in 1:nrow(csvfile)) { # nolint: seq_linter.
    row <- csvfile[i, ]
    year <- as.integer(row[1])
    price_index <- as.numeric(row[2])
    chemical_price_index[[year]] <- price_index
  }
  return(chemical_price_index)
}

read_non_energy_material_prices <- function() {
  df <- read.csv(
    here("..", "data", "non-energy-material-prices", "non-energy-material-prices.csv"),
    header = TRUE
  )
  return(df)
}

read_plant_cost_index <- function() {
  plant_cost_index <- list()
  csvfile <- read.csv(
    here("..", "data", "plant-cost-index", "plant-cost-index.csv"),
    header = TRUE
  )
  for (i in 1:nrow(csvfile)) { # nolint: seq_linter.
    row <- csvfile[i, ]
    year <- as.integer(row[1])
    value <- as.numeric(row[2])
    plant_cost_index[[year]] <- value
  }
  return(plant_cost_index)
}

read_consumer_price_index <- function() {
  consumer_price_indices <- list()
  filenames <- c("deflator-orig.csv", "deflator-soe.csv")
  for (filename in filenames) {
    csv_path <- here("..", "data", "gdp-implicit-price-deflator", filename)
    csv_file <- data.frame(read.csv(csv_path, header = TRUE))
    consumer_price_indices[[filename]] <- list()
    for (i in 1:nrow(csv_file)) { # nolint: seq_linter.
      row <- csv_file[i, ]
      year <- as.integer(row[1])
      value <- as.numeric(row[2])
      consumer_price_indices[[filename]][[year]] <- value
    }
  }
  # print(consumer_price_indices[["deflator-soe.csv"]][2001])
  return(consumer_price_indices)
}

read_labor_index <- function() {
  labor_index <- list()
  csvfile <- read.csv(
    here("..", "data", "labor-index", "labor-index.csv"),
    header = TRUE
  )
  for (i in 1:nrow(csvfile)) { # nolint: seq_linter.
    row <- csvfile[i, ]
    year <- as.integer(row[1])
    value <- as.numeric(row[2])
    labor_index[[year]] <- value
  }
  return(labor_index)
}

lhv_hhv <- read_fuel_heating_values()
lower_heating_values <- lhv_hhv[[1]]
higher_heating_values <- lhv_hhv[[2]]
conversion_factors <- read_conversion_factors()
plant_cost_index <- read_plant_cost_index()
consumer_price_index <- read_consumer_price_index()
non_energy_material_prices <- read_non_energy_material_prices()
chemical_price_index <- read_chemical_price_index()
labor_index <- read_labor_index()
macrs_depreciation_table = read_macrs_depreciation_table()
upstream_energy_and_emissions = read_upstream_energy_and_emissions()
co2_emission_factors = read_co2_emissions_factors()
labor_index = read_labor_index()
get_labor_index <- function(year, labor_file) {
  return(labor_index[[labor_file]][[year]])
}
get_lhv <- function(fuel) lower_heating_values[[fuel]]
conversion_factor <- function(from_to) conversion_factors[[from_to]]
get_plant_cost_index <- function(year) plant_cost_index[[year]]
get_cpi <- function(year, cpi_file) {
  return(consumer_price_index[[cpi_file]][[year]])
}
