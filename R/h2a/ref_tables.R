import::from(here, here)
read_fuel_heating_values <- function() {
  lower_heating_values <- list()
  higher_heating_values <- list()
  csvfile <- read.csv(
    file.path("data", "fuel-heating-values", "fuel-heating-values.csv"),
    header = TRUE
  )
  for (i in 1:nrow(csvfile)) { # nolint: seq_linter.
    row <- csvfile[i, ]
    if (startsWith(csvfile[i, 1], "#")) {
      next
    }
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
  csvfile <- read.csv(file.path("data", "conversion", "conversions.csv"),
    header = TRUE
  )
  for (i in 1:nrow(csvfile)) { # nolint: seq_linter.
    row <- csvfile[i, ]
    if (startsWith(csvfile[i, 1], "#")) {
      next
    }
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

read_chemical_price_index <- function() {
  chemical_price_index <- list()
  csvfile <- read.csv(
    here("..", "data", "chemical-price-index", "price-index-orig.csv"),
    header = TRUE
  )
  for (i in 1:nrow(csvfile)) { # nolint: seq_linter.
    row <- csvfile[i, ]
    if (startsWith(csvfile[i, 1], "#")) {
      next
    }
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
    if (startsWith(csvfile[i, 1], "#")) {
      next
    }
    year <- as.integer(row[1])
    value <- as.numeric(row[2])
    plant_cost_index[[year]] <- value
  }
  return(plant_cost_index)
}

read_consumer_price_index <- function() {
  consumer_price_index <- list()
  csvfile <- read.csv(
    here("..", "data", "gdp-implicit-price-deflator", "deflator-orig.csv"),
    header = TRUE
  )
  for (i in 1:nrow(csvfile)) { # nolint: seq_linter.
    row <- csvfile[i, ]
    if (startsWith(csvfile[i, 1], "#")) {
      next
    }
    year <- as.integer(row[1])
    value <- as.numeric(row[2])
    consumer_price_index[[year]] <- value
  }
  return(consumer_price_index)
}

read_labor_index <- function() {
  labor_index <- list()
  csvfile <- read.csv(
    here("..", "data", "labor-index", "labor-index.csv"),
    header = TRUE
  )
  for (i in 1:nrow(csvfile)) { # nolint: seq_linter.
    row <- csvfile[i, ]
    if (startsWith(csvfile[i, 1], "#")) {
      next
    }
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
get_lhv <- function(fuel) lower_heating_values[[fuel]]
conversion_factor <- function(from_to) conversion_factors[[from_to]]
get_plant_cost_index <- function(year) plant_cost_index[[year]]
get_cpi <- function(year) consumer_price_index[[year]]
