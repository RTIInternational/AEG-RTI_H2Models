read_default_inputs_json <- function(json_filename) {
    input_filepath <- here::here("..", "data", "input", "default", json_filename)
    data <- jsonlite::fromJSON(input_filepath)
    return(data)
}

json_filename <- "default-smr-natural-gas-no-cc.json"
user_input <- read_default_inputs_json(json_filename)
