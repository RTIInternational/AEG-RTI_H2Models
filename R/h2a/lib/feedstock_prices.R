#
# This file is programmatically generated by py_writer.py; do not edit
#
import::here(FIRST, concat, get, get_cell, split, to_num, .from = "helpers.R", .directory = here("h2a"))
import::here(conversion_factor, get_aeo, .from = "ref_tables.R", .directory = here("h2a"))
get_feedstock_price_for_year <- function(year, feedstock, INFLATION_FACTOR) {
    #'Get the price of a feedstock for a given year
    return(get_cell(get_aeo(get(feedstock, 'price_table')), year, get(feedstock, 'name')) * to_num(get(feedstock, 'usage')) * conversion_factor(concat(get(split(get(feedstock, 'units'),'/'), FIRST), '_to_$/GJ')) * INFLATION_FACTOR)
}
lookup_prices_for_feedstock <- function(analysis_range, feedstock, INFLATION_FACTOR) {
    #'Lookup prices for a given feedstock over a range of years
    return(mapply(function(year) list(get_feedstock_price_for_year(year, feedstock, INFLATION_FACTOR)), analysis_range) )
}
get_feedstock_price_for_startup_year <- function(year, feedstock, startup_year, INFLATION_FACTOR) {
    #'Get the price of a feedstock for the startup year
    return(get_cell(get_aeo(get(feedstock, 'price_table')), year, get(feedstock, 'startup_year')) * to_num(get(feedstock, 'usage')) * conversion_factor(concat(get(split(get(feedstock, 'units'),'/'), FIRST), '_to_$/GJ')) * INFLATION_FACTOR)
}
fixed_prices_for_feedstock <- function(analysis_range, feedstock, startup_year, INFLATION_FACTOR) {
    #'Get fixed prices for a given feedstock over a range of years
    return(mapply(function(year) list(get_feedstock_price_for_startup_year(year, feedstock, startup_year, INFLATION_FACTOR)), analysis_range) )
}
select_feedstock_prices <- function(feedstock, analysis_range, startup_year, INFLATION_FACTOR) {
    #'For a given feedstock, select whether to lookup prices or use a fixed price
    if (get(feedstock, 'lookup_prices')) {
        return(lookup_prices_for_feedstock(analysis_range, feedstock, INFLATION_FACTOR))
    }
    else {
        return(fixed_prices_for_feedstock(analysis_range, feedstock, startup_year, INFLATION_FACTOR))
    }
}
get_feedstock_price_df <- function(feedstocks, analysis_range, startup_year, INFLATION_FACTOR) {
    #'Get a dataframe of prices by feedstock and year
    return(mapply(function(feedstock) list(select_feedstock_prices(feedstock, analysis_range, startup_year, INFLATION_FACTOR)), feedstocks) )
}
