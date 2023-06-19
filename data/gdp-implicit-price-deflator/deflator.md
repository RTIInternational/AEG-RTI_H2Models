# Gross Domestic Product: Implicit Price Deflator (GDPDEF)

## Files

deflator-orig.csv is the original table from the H2A Excel workbook. The Excel sheet said Index 2005=100, but it clearly used index 2009=100. The title also was incorrect, reading "Deflator Price" instead of "Price Deflator".

deflator-updated.csv is the updated version as of March 2023. The index by default was set to 2012=100.

deflator-soe.csv is an older version used in `current-central-solid-oxide-electrolysis-version-nov20.xlsm`

## Use in H2A formulas

The table is commonly used with 2 years to calculate a ratio, like so:

ref_year / current_year = deflator_table[2016]/deflator_table[2018] = 0.958

The table is referenced from the Capital Costs sheet as "The Consumer Price Inflator (CPI)", "used to deflate all dollars from the current year to the Reference Year."

## Original H2A Title

TABLE B - GDP Implicit Deflator Price Index

Location in workbook: HyARC Physical Property Data, A91

## Citation
U.S. Bureau of Economic Analysis, Gross Domestic Product: Implicit Price Deflator [GDPDEF], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/GDPDEF, March 30, 2023.

