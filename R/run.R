# here i_am declares the current directory as the root of the project
# Subsequent calls to here() will be relative to this directory
here::i_am("run.R")
import::from(here, here)

# Parse CLI args as a list of files
args <- commandArgs(trailingOnly = TRUE)

# Import the user input
import::from("read_input.R", read_default_inputs_json, .directory = here("h2a"))
# Import the H2A model
import::from("formulas.R", calculate, .directory = here("h2a"))

# Loop over files
for (json_filename in args) {
    user_input <- read_default_inputs_json(json_filename)

    # Run the model
    results <- calculate(user_input)
}
