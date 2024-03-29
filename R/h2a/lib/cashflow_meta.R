#
# This file is programmatically generated by py_writer.py; do not edit
#
import::here(FIRST, .from = "helpers.R", .directory = here("h2a"))
determine_operation_year <- function(i, construct) {
    #'Helper function in generating the list of operation years
    if ((i - FIRST) == construct) {
        return(1)
    }
    else if ((i - FIRST) < construct) {
        return(-construct + (i - FIRST))
    }
    else {
        return((i - FIRST) - construct + 1)
    }
}
get_operation_range <- function(analysis_year_num_range, construct) {
    #'Get the range of plant operation years
    return(mapply(function(i) list(determine_operation_year(i, construct)), analysis_year_num_range) )
}
determine_inflation_price_increase_factor <- function(year, inflation_rate, startup_year) {
    #'Helper function in generating the list of inflation price increase factors
    return((1 + inflation_rate) ** (year - startup_year))
}
get_inflation_price_increase_factors <- function(analysis_range, inflation_rate, startup_year) {
    #'Get the inflation price increase factors over the analysis range
    return(mapply(function(year) list(determine_inflation_price_increase_factor(year, inflation_rate, startup_year)), analysis_range) )
}
