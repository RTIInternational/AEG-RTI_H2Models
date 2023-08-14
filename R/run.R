# here i_am declares the current directory as the root of the project
# Subsequent calls to here() will be relative to this directory
here::i_am("run.R")
import::from(here, here)
library(tidyverse)

# Parse CLI args as a list of files
# args <- commandArgs(trailingOnly = TRUE)
# 
# args = c(
#   'default-smr-natural-gas-no-cc.json',
#   'default-smr-natural-gas-with-cc.json',
#   'default-autothermal-reforming-natural-gas-with-cc.json',
#   'default-solid-oxide-electrolysis.json',
#   'default-pem-electrolysis.json'
# )

###############################################################
###############################################################
inputs = read.csv("./parameters/parameters.csv")
output_filename = "sample_results.csv" # should include ".csv"
###############################################################
###############################################################

# which default model to start with
args = inputs$baseline
# add the .json suffix everywhere
for (i in 1:length(args)) {
  args[i] = paste0(args[i],".json")
}
num_vars = ncol(inputs) - 1

# Import the user input
import::from("read_input.R", read_default_inputs_json, .directory = here("h2a"))
# Import the H2A model
import::from("formulas.R", calculate, .directory = here("h2a"))
# Import output processing
# import::here(json_to_df, .from = "output_processing.R", .directory = here("h2a"))
import::from("output_processing.R", make_plots, .directory = here("h2a"))
import::from("output_processing.R", json_to_df, .directory = here("h2a"))

run <- function(json_filename, change_vars = c(), change_vals = c(), label = NA) {
    print(change_vars)
    print(change_vals)
    # read the default inputs for whichever model we're given  
    user_input <- read_default_inputs_json(json_filename)
    
    # if we need to change any variables, enter this loop
    if(length(change_vars) > 0) {
      # grab the field names from the json
      fields = names(user_input)
      # loop through each parameter we want to change
      for (j in 1:length(change_vars)) {
        print(change_vars[j])
        # identify where in the json we're looking
        location = which(fields == change_vars[j])
        
        # replace the input value with the one given by the user
        if (!(is.na(change_vals[j]))) {
          print(change_vals[j])
          user_input[[location]] = change_vals[j]
        }
      }
      # now proceed
      model_name = paste0(str_replace(json_filename,".json",""),"-",label,".json")
    } else {
      model_name = json_filename
    }
    
    # Run the model
    results_list = calculate(user_input)
    results_json = jsonlite::toJSON(results_list)
    jsonlite::write_json(results_json,paste0("./Output/",model_name))
    
    return(list(
      "input" = user_input,
      "list" = results_list,
      "json" = results_json
    ))
}

# Loop over files
results_df = data.frame()
i = 1 # counter
for (json_filename in args) {
  if(num_vars == 0) {
    suppressWarnings({results = run(json_filename)})
    model_name = json_filename
  } else {
    vars = colnames(inputs)[2:ncol(inputs)]
    vals = suppressWarnings({as.numeric(unlist(inputs[i,2:ncol(inputs)], use.names = FALSE))}) # note: this will coerce strings such as "default" into NAs, we'll check for this later
    suppressWarnings({results = run(json_filename, change_vars = vars, change_vals = vals, label = i)})
    #results = r
    model_name = paste0(str_replace(json_filename,".json",""),"-",i,".json")
  }
  
  df_row = json_to_df(results$list, model_name)
  
  results_df = dplyr::bind_rows(results_df, df_row)

  write.csv(results_df, paste0("./output/",output_filename), row.names = FALSE)
  
  i = i + 1 # increment
}

make_plots(output_filename)




