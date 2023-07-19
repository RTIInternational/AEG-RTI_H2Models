#install.packages("purrr")

library(jsonlite)
library(purrr)

change_values <- function(json_file, field_names, list_of_values) {
  #load the JSON file
  json_data <- fromJSON(json_file)
  
  #create an empty list storing JSON outputs
  json_outputs <- list()
  
  #iterate the list of field names and their relevant list of values
  for (i in seq_along(field_names)) {
    field_name <- field_names[[i]]
    values <- list_of_values[[i]]
    
    #modify the JSON object for each field name and its list of values
    json_results <- map(values, function(value) {
      modified_json <- json_data
      modified_json[[field_name]] <- value
      return(modified_json)
    })
    
    #adds JSON outputs to main list
    json_outputs[[field_name]] <- json_results
  }
  
  #return  list of JSON outputs
  return(json_outputs)
}

#list of field names to modify
field_names_to_modify <- c("CO2_Capture_Efficiency", "plant_life", "real_irr")

#list of lists of values, one for each field name
values_lists <- list(
  list_of_values1 = c(90:95),
  list_of_values2 = c(35, 40, 45),
  list_of_values3 = c(0.06, 0.08, 0.1)
)

#provide the path of the JSON file you want to modify
json_file_path <- 'C:/Users/matth/Downloads/default-smr-natural-gas-no-cc.json'

results <- change_values(json_file_path, field_names_to_modify, values_lists)
View(results)

#specify the target directory
output_directory <- "C:/Users/matth/OneDrive/Documents/AEG-RTI_H2Models/R"

#save each modified JSON object as a .json file in the target directory
for (i in seq_along(field_names_to_modify)) {
  field_name <- field_names_to_modify[[i]]
  for (j in seq_along(results[[field_name]])) {
    file_path <- file.path(output_directory, paste0("output_", field_name, "_", j, ".json"))
    #convert JSON object to a character string using toJSON
    json_string <- toJSON(results[[field_name]][[j]], auto_unbox = TRUE)
    #write the JSON string to the file
    write(json_string, file = file_path)
  }
}
