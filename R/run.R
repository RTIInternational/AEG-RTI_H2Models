# here i_am declares the current directory as the root of the project
# Subsequent calls to here() will be relative to this directory

here::i_am("run.R")
import::from(here, here)

# Import the user input
import::from("read_input.R", user_input, .directory = here("h2a"))

# Import the H2A model
import::from("formulas.R", calculate, .directory = here("h2a"))

# Run the model
results <- calculate(user_input)
print(results)
