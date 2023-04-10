# Producer Price Index by Industry: Chemical Manufacturing (PCU325325)

## Files

price-index-orig.csv is the original table from the H2A Excel workbook. The Excel sheet said Index 1982=100, but it clearly used index 2000=100.

price-index-updated.csv is the updated version as of April 2023. The index by default was set to 2012=100.

## Use in H2A formulas

The table is commonly used with 2 years to calculate a ratio, like so:

ref_year / current_year = price_index_table[2016]/price_index_table[2018] = 0.958

## Original H2A Title & Information

TABLE B4 - SRI Chemical Price Index
SRI Inorganic Price Index  (Index, 1982=100), Current Index at http://www.sriconsulting.com/CEH/
Location in workbook: HyARC Physical Property Data, K91
Base date: December 1984 for the Producer price index - chemical mfg (adjusted to 1982 base)
5/15/17:  Same information as BLS data for Chemical Mfg:  https://data.bls.gov/pdq/SurveyOutputServlet
3/1/2022 source: https://alfred.stlouisfed.org/series?seid=PCU325325

## Organization Renames

SRI Consulting (Stanford Research Institute) became SRI International. It authored the Chemical Economics Handbook (CEH) since 1950. Publishing was taken over by IHS Markit, which is now part of S&P Global. CEH is now located behind a paywall at https://www.spglobal.com/commodityinsights/en/ci/products/chemical-economics-handbooks.html

## Citation
U.S. Bureau of Labor Statistics, Producer Price Index by Industry: Chemical Manufacturing [PCU325325], retrieved from FRED, Federal Reserve Bank of St. Louis; https://fred.stlouisfed.org/series/PCU325325, April 8, 2023
