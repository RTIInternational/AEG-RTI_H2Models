read_default_inputs_json <- function(json_file) {
  default_inputs <- list()
  data <- jsonlite::read_json(file.path("data", "input", "default", json_file))
  for (key in names(data)) {
    default_inputs[[key]] <- data[[key]]
  }
  return(default_inputs)
}

read_formulas <- function() {
  formulas <- list()
  csvfile <- read.csv(file.path("data", "formula", "formulas.csv"),
    header = TRUE
  )
  for (i in 1:nrow(csvfile)) { # nolint: seq_linter.
    if (startsWith(csvfile[i, 1], "#")) {
      next
    }
    name <- csvfile[i, 1]
    label <- csvfile[i, 2]
    formula <- csvfile[i, 3]
    orig_name <- csvfile[i, 4]
    formulas[[i]] <- list(name = name, label = label, formula = formula, orig_name = orig_name) # nolint: line_length_linter.
  }
  return(formulas)
}

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


main <- function() {
  default_inputs <- read_default_inputs_json(
    "default-smr-natural-gas-no-cc.json"
  )
  formulas <- read_formulas()
  lhv_hhv <- read_fuel_heating_values()
  lower_heating_values <- lhv_hhv[[1]]
  higher_heating_values <- lhv_hhv[[2]]
  conversion_factors <- read_conversion_factors()

  # Functions used in formulas
  get_lhv <- function(fuel) lower_heating_values[[fuel]]
  conversion_factor <- function(from_to) conversion_factors[[from_to]]

  # Assign default inputs to global environment
  for (i in 1:length(default_inputs)) {
    assign(names(default_inputs)[i], default_inputs[[i]])
  }
  # Assign formulas to global environment
  # If $name exists, use it as the variable name
  # Otherwise, use $orig_name
  # The variable value is $formula, evaluated
  for (i in 1:length(formulas)) {
    name <- formulas[[i]]$name
    orig_name <- formulas[[i]]$orig_name
    formula <- formulas[[i]]$formula
    val <- unix::eval_safe(eval(parse(text = formula)))
    if (name != "") {
      assign(name, val)
    } else {
      assign(orig_name, val)
    }
  }
  # Mmmm, global variables (╯°□°）╯︵ ┻━┻)
  # TODO: change formula "assign" to return a list of variables
  print(INFLATION_FACTOR)
}
main()
