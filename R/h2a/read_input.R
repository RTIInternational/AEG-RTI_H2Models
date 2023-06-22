read_default_inputs_json <- function(json_filename) {
    input_filepath <- here::here("..", "data", "input", "default", json_filename)
    data <- jsonlite::fromJSON(input_filepath)

    # Split dataframe into list of vectors
    data[["feedstocks"]] <- asplit(data["feedstocks"][[1]], 1)
    data[["utilities"]] <- ifelse(dim(data["utilities"]) > 0, asplit(data["utilities"][[1]], 1), list())
    data[["capital_investments"]] <- asplit(data["capital_investments"][[1]], 1)
    data[["nonenergy_materials"]] <- asplit(data["nonenergy_materials"][[1]], 1)
    return(data)
}

json_filename <- "default-smr-natural-gas-no-cc.json"
user_input <- read_default_inputs_json(json_filename)
