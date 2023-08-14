error_check1 = function(input_filename) {
  # check for csv extension  
  if (substr(input_filename,nchar(input_filename) - 3, nchar(input_filename)) == ".csv") {
    if (file.exists(input_filename)) {
      t = 5
    } else {
      stop(paste0("Error: input file with name ",input_filename, " does not exist. Please check spelling and directory structure"))
    }
  } else {
    stop(paste0("Error: please include the .csv suffix when defining input_filename. And don't even think about giving me a .xlsx file!"))
  }
}

error_check2 = function(output_filename) {
  if (substr(output_filename,nchar(output_filename) - 3, nchar(output_filename)) == ".csv") {
    t = 5
  } else {
    stop(paste0("Error: please include the .csv suffix when defining output_filename"))
  }
}

error_check3 = function(model_name) {
  if (substr(model_name, nchar(model_name) - 4, nchar(model_name)) == ".json") {
    stop(paste0("Error: please do not include '.json' in the baseline column of the input spreadsheet"))
  } else {
    if (model_name %in% c(
      'default-autothermal-reforming-natural-gas-with-cc',
      'default-pem-electrolysis',
      'default-smr-natural-gas-no-cc',
      'default-smr-natural-gas-with-cc',
      'default-solid-oxide-electrolysis'
    )) {
      t = 5
    } else {
      stop(paste0("Error: baseline model name ", model_name, "is not one of the 5 accepted NREL H2 model names: 'default-autothermal-reforming-natural-gas-with-cc', 'default-pem-electrolysis', 'default-smr-natural-gas-no-cc', 'default-smr-natural-gas-with-cc', 'default-solid-oxide-electrolysis'"))
    }
  }
}

error_check4 = function(var_list) {
  schema = jsonlite::read_json("../data/input/default/input.schema.json")
  valid_names = names(schema$properties)
  for (var in var_list) {
    if (var %in% valid_names) {
      t = 5
    } else {
      stop(paste0("Error: variable ", var, " from input sheet is not a valid H2 variable. See 'data/input/default/input.schema.json' for details on each acceptable field."))
    }
  }
}