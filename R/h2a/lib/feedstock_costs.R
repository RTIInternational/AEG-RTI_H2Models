#
# This file is programmatically generated by py_writer.py; do not edit
#
import::here(FIRST, get, num_range, sum_list, .from = "helpers.R", .directory = here("h2a"))
calculate_feedstock_cost_for_year <- function(year, price, inflation_price_increase_factor, start_time, plant_output_kg_per_year, percnt_var) {
    #'Calculate the cost of a feedstock for a given year
    if (year < 0) {
        return(0)
    }
    else if (year == 1 && start_time < 1) {
        return(-(( price * plant_output_kg_per_year * inflation_price_increase_factor * percnt_var * start_time ) + ( price * plant_output_kg_per_year * inflation_price_increase_factor * (1 - start_time) )))
    }
    else if (year <= start_time) {
        return(-(price * plant_output_kg_per_year * inflation_price_increase_factor * percnt_var))
    }
    else {
        return(-(price * plant_output_kg_per_year * inflation_price_increase_factor))
    }
}
get_feedstock_costs <- function(years, prices, inflation_price_increase_factors, start_time, plant_output_kg_per_year, percnt_var) {
    #'Calculate the cost of a feedstock over a range of years
    return(mapply(function(year, price, inflation_price_increase_factor) list(calculate_feedstock_cost_for_year(year, price, inflation_price_increase_factor, start_time, plant_output_kg_per_year, percnt_var)), years, prices, inflation_price_increase_factors) )
}
feedstock_prices_from_df <- function(feedstock_price_df, i) {
    #'For a given year (i), return price of each feedstock
    return(mapply(function(feedstock) list(get(feedstock, i)), feedstock_price_df) )
}
get_total_feedstock_costs <- function(operation_range, feedstock_price_df, inflation_price_increase_factors, start_time, plant_output_kg_per_year, percnt_var) {
    #'Calculate the total cost of all feedstocks over a range of years
    return(mapply(function(year) list(calculate_feedstock_cost_for_year(get(operation_range, year), sum_list(feedstock_prices_from_df(feedstock_price_df, year)), get(inflation_price_increase_factors, year), start_time, plant_output_kg_per_year, percnt_var)), num_range(FIRST, length(operation_range) + FIRST)) )
}
