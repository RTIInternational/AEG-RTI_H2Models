# Non-Energy Materials and Byproducts

The file `non-energy-material-prices.csv` is sourced from the Non-Energy Material Prices tab of the original H2A workbook. Its original source data is unknown.

## Use in H2A formulas

Each data cell in the table is a base value that will be multiplied by a ratio to update costs to reference year dollars. The ratio is calculated like so:

ref_year / source_year = price_index_table[2016]/price_index_table[2005] = 1.426054458

The price table index is located at `data/chemical-price-index`
