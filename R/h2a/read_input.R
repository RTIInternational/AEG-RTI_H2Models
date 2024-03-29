options(digits = 13)

read_default_inputs_json <- function(json_filename) {
    input_filepath <- here::here("..", "data", "input", "default", json_filename)
    data <- jsonlite::fromJSON(input_filepath)

    # Split dataframe into list of vectors
    data[["feedstocks"]] <- ifelse(dim(data["feedstocks"][[1]]) > 0, asplit(data["feedstocks"][[1]], 1), list())

    # Using longform if statements to avoid strange behavior with ifelse
    if (length(data[["utilities"]]) > 0) {
        data[["utilities"]] <- asplit(data["utilities"][[1]], 1)
    } else {
        data[["utilities"]] <- list()
    }
    data[["capital_investments"]] <- asplit(data["capital_investments"][[1]], 1)
    data[["nonenergy_materials"]] <- asplit(data["nonenergy_materials"][[1]], 1)
    return(data)
}
