# AEO

## Conversion

The costs from the AEO are converted to an LHV basis for use in this model. The calculations for these conversions are below.

The price data is updated to the H2A reference year by multiplying by:

1. (deflator price index from Table B for the H2A reference year from Table A/deflator price index for AEO data year)

2. The price data is converted from HHV to LHV by multiplying by the ratio of the HHV to the LHV from Table A

3. Finally, the price is converted from an mmBTU basis to J basis by dividing by the conversion factor

## Example

AEO_2014 at A88 and AEO_2014 at A103. The second table is source data from AEO. The first table does the above calculations on the source data.

Electricity and woody biomass is just multiplied by the price deflator. Natural gas and coal feedstock prices are multiplied by all 3: deflator, HHV/LHV, 1/mmBTU_to_GJ.