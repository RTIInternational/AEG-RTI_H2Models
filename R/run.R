# here i_am declares the current directory as the root of the project
# Subsequent calls to here() will be relative to this directory
here::i_am("run.R")
import::from(here, here)

# Parse CLI args as a list of files
args <- commandArgs(trailingOnly = TRUE)

# args = c('default-smr-natural-gas-no-cc.json') # runs
# args = c('default-smr-natural-gas-with-cc.json') # runs
# args = c('default-pem-electrolysis.json') # does not run
# args = c('default-solid-oxide-electrolysis.json') # runs
# args = c('default-autothermal-reforming-natural-gas-with-cc.json') # runs
args = c(
  'default-smr-natural-gas-no-cc.json',
  'default-smr-natural-gas-with-cc.json',
  'default-autothermal-reforming-natural-gas-with-cc.json',
  'default-solid-oxide-electrolysis.json',
  'default-pem-electrolysis.json'
)
output_filename = "sample_results.csv" # should include ".csv"

# Import the user input
import::from("read_input.R", read_default_inputs_json, .directory = here("h2a"))
# Import the H2A model
import::from("formulas.R", calculate, .directory = here("h2a"))
# Import output processing
import::from("output_processing.R", json_to_df, .directory = here("h2a"))
import::from("output_processing.R", cost_barplot, .directory = here("h2a"))
import::from("output_processing.R", emissions_barplot, .directory = here("h2a"))
import::from("output_processing.R", lifecycle_barplot, .directory = here("h2a"))
import::from("output_processing.R", make_plots, .directory = here("h2a"))


run <- function(json_filename) {
    user_input <- read_default_inputs_json(json_filename)

    # Run the model
    results_list = calculate(user_input)
    results_json = toJSON(results_list)
    write_json(results_json,paste0("./Output/",json_filename))
    
    return(list(
      "input" = user_input,
      "list" = results_list,
      "json" = results_json
    ))
}

# Loop over files
results_df = data.frame()
for (json_filename in args) {
    results = run(json_filename)
    

    df_row = json_to_df(results$list, json_filename)

    results_df = bind_rows(results_df, df_row)

    write.csv(results_df, paste0("./output/",output_filename), row.names = FALSE)
}

make_plots(output_filename)


