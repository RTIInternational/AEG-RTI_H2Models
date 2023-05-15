#
# This file is programmatically generated by py_writer.py; do not edit
#
from h2a.inputs import *
from h2a.lib.after_tax_income import get_after_tax_income_column
from h2a.lib.capital_investments import capital_investment_costs
from h2a.lib.cashflow import get_aftertax_post_depreciation_cashflow, get_cumulative_cashflow_column, get_pretax_cashflow_column
from h2a.lib.cashflow_meta import get_inflation_price_increase_factors, get_operation_range
from h2a.lib.debt_financing import determine_interest_payment, determine_principal_payment
from h2a.lib.decommissioning import get_decom_costs_column
from h2a.lib.depreciable_capital import get_annual_depreciable_capital
from h2a.lib.depreciation_calculation import get_depreciation_calculation_table
from h2a.lib.depreciation_charges import get_depreciation_charges, get_depreciation_charges_column
from h2a.lib.feedstock_costs import get_total_feedstock_costs
from h2a.lib.feedstock_prices import get_feedstock_price_df
from h2a.lib.fixed_costs import get_fixed_cost_column
from h2a.globals import CEPCIinflator, CPIinflator, INFLATION_FACTOR, analysis_period_end, analysis_period_start, plant_output_kg_per_year
from h2a.lib.h2_sales import get_h2_sales_kg_per_year
from h2a.helpers import YEAR_1, get, irr, length, npv, seq_along, skip, slice
from h2a.lib.initial_equity import get_initial_equity_depr_cap
from h2a.lib.nonenergy_materials import get_nonenergy_material_price_df
from h2a.lib.other_non_depreciable_capital_cost import get_other_non_depreciable_capital_cost_column
from h2a.lib.other_raw_material_costs import get_other_raw_material_cost_column
from h2a.lib.predepreciation_income import get_predepreciation_income_column
from h2a.ref_tables import chemical_price_index, conversion_factor, get_lhv, labor_index
from h2a.lib.replacement_costs import get_replacement_costs
from h2a.lib.revenue_h2_sales import get_revenue_h2_sales_column
from h2a.lib.salvage import get_salvage_column
from h2a.lib.taxable_income import get_taxable_income_column
from h2a.lib.total_taxes import get_total_taxes_column
from h2a.lib.variable_costs import get_variable_cost_column
from h2a.lib.working_capital_reserve import get_working_cap_reserve_column, get_working_cap_reserve_rows

H2_LHV_MJ_p_kg = get_lhv("Hydrogen")
print('H2_LHV_MJ_p_kg: ', H2_LHV_MJ_p_kg)

output_energy_MMBtu_per_year = plant_output_kg_per_year * H2_LHV_MJ_p_kg / 1000 / conversion_factor("mmBTU_to_GJ")
print('output_energy_MMBtu_per_year: ', output_energy_MMBtu_per_year)

output_energy_MJ_per_year = plant_output_kg_per_year * H2_LHV_MJ_p_kg
print('output_energy_MJ_per_year: ', output_energy_MJ_per_year)

nominal_irr = ((1 + real_irr) * (1 + inflation_rate)) - 1
print('nominal_irr: ', nominal_irr)

percentage_debt_financing = 1 - percentage_equity_financing
print('percentage_debt_financing: ', percentage_debt_financing)

target_after_tax_nominal_irr = (1 + real_irr)*(1 + inflation_rate) - 1
print('target_after_tax_nominal_irr: ', target_after_tax_nominal_irr)

analysis_range = range(analysis_period_start, analysis_period_end)
print('analysis_range: ', analysis_range)

analysis_index_range = seq_along(analysis_range)
print('analysis_index_range: ', analysis_index_range)

feedstock_price_df = get_feedstock_price_df(feedstocks, analysis_range, startup_year)
print('feedstock_price_df: ', feedstock_price_df)

operation_range = get_operation_range(analysis_index_range, construct)
print('operation_range: ', operation_range)

inflation_price_increase_factors = get_inflation_price_increase_factors(analysis_range, inflation_rate, startup_year)
print('inflation_price_increase_factors: ', inflation_price_increase_factors)

total_feedstock_cost_column = get_total_feedstock_costs(operation_range, feedstock_price_df, inflation_price_increase_factors, start_time, plant_output_kg_per_year, percnt_var)
print('total_feedstock_cost_column: ', total_feedstock_cost_column)

discounted_value_feedstock_cost = get(total_feedstock_cost_column, YEAR_1) + npv(target_after_tax_nominal_irr, skip(total_feedstock_cost_column, 1))
print('discounted_value_feedstock_cost: ', discounted_value_feedstock_cost)

direct_cap = sum(capital_investment_costs(capital_investments))
print('direct_cap: ', direct_cap)

CO2_seq = 0
print('CO2_seq: ', CO2_seq)

site_preparation_cost = (0.02 * CO2_seq / (CEPCIinflator * CPIinflator)) + (0.159872128446844 * direct_cap / (CEPCIinflator * CPIinflator))
print('site_preparation_cost: ', site_preparation_cost)

engineering_and_design_cost = (0.1 * CO2_seq / (CEPCIinflator * CPIinflator)) + (0.11599636520534 * direct_cap / (CEPCIinflator * CPIinflator))
print('engineering_and_design_cost: ', engineering_and_design_cost)

process_contingency_cost = 0
print('process_contingency_cost: ', process_contingency_cost)

project_contingency_cost = 0.247793627342024 * direct_cap / (CEPCIinflator * CPIinflator)
print('project_contingency_cost: ', project_contingency_cost)

other_depreciable_capital_cost = 40137000
print('other_depreciable_capital_cost: ', other_depreciable_capital_cost)

upfront_permitting_costs = (0.15 * CO2_seq / (CEPCIinflator * CPIinflator)) + (0.11599636520534 * direct_cap / (CEPCIinflator * CPIinflator))
print('upfront_permitting_costs: ', upfront_permitting_costs)

depr_cap = direct_cap + CO2_seq + (CEPCIinflator * CPIinflator) * (site_preparation_cost + engineering_and_design_cost + process_contingency_cost + project_contingency_cost + other_depreciable_capital_cost + upfront_permitting_costs)
print('depr_cap: ', depr_cap)

replacement_costs = get_replacement_costs(operation_range, inflation_price_increase_factors, replace_factor, depr_cap, ref_year, startup_year, inflation_rate)
print('replacement_costs: ', replacement_costs)

discounted_value_replacement_costs = get(replacement_costs, YEAR_1) + npv(nominal_irr, skip(replacement_costs, 1))
print('discounted_value_replacement_costs: ', discounted_value_replacement_costs)

land_cost = acres_required * cost_per_acre * CPIinflator
print('land_cost: ', land_cost)

other_non_depreciable_capital_cost = 0
print('other_non_depreciable_capital_cost: ', other_non_depreciable_capital_cost)

non_dep_cap = land_cost + other_non_depreciable_capital_cost
print('non_dep_cap: ', non_dep_cap)

total_cap = depr_cap + non_dep_cap
print('total_cap: ', total_cap)

depr_cap_infl = (total_cap - non_dep_cap) * INFLATION_FACTOR
print('depr_cap_infl: ', depr_cap_infl)

non_dep_infl = non_dep_cap * INFLATION_FACTOR
print('non_dep_infl: ', non_dep_infl)

total_capital_investment = depr_cap_infl + non_dep_infl
print('total_capital_investment: ', total_capital_investment)

initial_equity_depr_cap = get_initial_equity_depr_cap(analysis_index_range, inflation_price_increase_factors, depr_cap_infl, percentage_equity_financing, percent_cap1, percent_cap2, percent_cap3, percent_cap4)
print('initial_equity_depr_cap: ', initial_equity_depr_cap)

discounted_value_initial_equity_depr_cap = get(initial_equity_depr_cap, YEAR_1) + npv(nominal_irr, skip(initial_equity_depr_cap, 1))
print('discounted_value_initial_equity_depr_cap: ', discounted_value_initial_equity_depr_cap)

other_non_depreciable_capital_cost_column = get_other_non_depreciable_capital_cost_column(analysis_index_range, inflation_price_increase_factors, non_dep_infl)
print('other_non_depreciable_capital_cost_column: ', other_non_depreciable_capital_cost_column)

discounted_value_other_non_depreciable_capital_cost = get(other_non_depreciable_capital_cost_column, YEAR_1) + npv(nominal_irr, skip(other_non_depreciable_capital_cost_column, 1))
print('discounted_value_other_non_depreciable_capital_cost: ', discounted_value_other_non_depreciable_capital_cost)

decom = decom_percent * depr_cap_infl
print('decom: ', decom)

decom_costs_column = get_decom_costs_column(operation_range, inflation_price_increase_factors, decom, plant_life)
print('decom_costs_column: ', decom_costs_column)

discounted_value_decom_costs = get(decom_costs_column, YEAR_1) + npv(nominal_irr, skip(decom_costs_column, 1))
print('discounted_value_decom_costs: ', discounted_value_decom_costs)

salvage = salvage_perct * total_capital_investment
print('salvage: ', salvage)

salvage_column = get_salvage_column(operation_range, inflation_price_increase_factors, salvage, plant_life)
print('salvage_column: ', salvage_column)

FTE_HOURS_PER_YEAR = 2080
print('FTE_HOURS_PER_YEAR: ', FTE_HOURS_PER_YEAR)

labor_cost_inflator = get(labor_index, ref_year) / get(labor_index, BasisYear)
print('labor_cost_inflator: ', labor_cost_inflator)

labor_cost = total_plant_staff * (labor_cost_per_hour * labor_cost_inflator) * FTE_HOURS_PER_YEAR
print('labor_cost: ', labor_cost)

overhead_GA = labor_cost * overhead_rate
print('overhead_GA: ', overhead_GA)

tax_insurance = tax_ins_rate * total_cap
print('tax_insurance: ', tax_insurance)

total_fixed_cost = labor_cost + overhead_GA + tax_insurance + (CEPCIinflator*CPIinflator) * (licensing + rent + material_cost_maintenance_and_repairs + production_cost_maintenance_and_repairs + other_fees + other_fixed)
print('total_fixed_cost: ', total_fixed_cost)

inflated_fixed = total_fixed_cost * INFLATION_FACTOR
print('inflated_fixed: ', inflated_fixed)

fixed_cost_column = get_fixed_cost_column(operation_range, inflation_price_increase_factors, inflated_fixed, percnt_fixed, start_time)
print('fixed_cost_column: ', fixed_cost_column)

discounted_value_fixed_cost = get(fixed_cost_column, YEAR_1) + npv(target_after_tax_nominal_irr, skip(fixed_cost_column, 1))
print('discounted_value_fixed_cost: ', discounted_value_fixed_cost)

total_tax_rate = fed_tax_rate + state_tax_rate * (1 - fed_tax_rate)
print('total_tax_rate: ', total_tax_rate)

percentage_debt_financing = 1 - percentage_equity_financing
print('percentage_debt_financing: ', percentage_debt_financing)

initial_capital_financed = -depr_cap_infl * percentage_debt_financing * get(inflation_price_increase_factors, YEAR_1)
print('initial_capital_financed: ', initial_capital_financed)

LAST_ANALYSIS_YEAR = anal_period + construct - 1
print('LAST_ANALYSIS_YEAR: ', LAST_ANALYSIS_YEAR)

principal_payments_column = determine_principal_payment(debt_period, analysis_index_range, LAST_ANALYSIS_YEAR, initial_capital_financed)
print('principal_payments_column: ', principal_payments_column)

interest_payments_column = determine_interest_payment(debt_period, analysis_index_range, initial_capital_financed, debt_interest)
print('interest_payments_column: ', interest_payments_column)

discounted_value_interest_payments = get(interest_payments_column, YEAR_1) + npv(target_after_tax_nominal_irr, skip(interest_payments_column, 1))
print('discounted_value_interest_payments: ', discounted_value_interest_payments)

h2_sales_kg_per_year = get_h2_sales_kg_per_year(operation_range, plant_output_kg_per_year, percnt_revs, start_time)
print('h2_sales_kg_per_year: ', h2_sales_kg_per_year)

discounted_value_total_h2_sales_kg = get(h2_sales_kg_per_year, YEAR_1) + npv(real_irr, skip(h2_sales_kg_per_year, 1))
print('discounted_value_total_h2_sales_kg: ', discounted_value_total_h2_sales_kg)

LCOE_contribution_h2_sales_kg = discounted_value_total_h2_sales_kg * (1 - total_tax_rate)
print('LCOE_contribution_h2_sales_kg: ', LCOE_contribution_h2_sales_kg)

discounted_value_total_salvage_value = get(salvage_column, YEAR_1) + npv(target_after_tax_nominal_irr, skip(salvage_column, 1))
print('discounted_value_total_salvage_value: ', discounted_value_total_salvage_value)

nonenergy_material_price_df = get_nonenergy_material_price_df(nonenergy_materials, analysis_range, INFLATION_FACTOR, ref_year)
print('nonenergy_material_price_df: ', nonenergy_material_price_df)

var_misc = other_variable_operating_costs * get(chemical_price_index, ref_year) / get(chemical_price_index, BasisYear)
print('var_misc: ', var_misc)

waste_treat = waste_treatment_costs * get(chemical_price_index, ref_year) / get(chemical_price_index, BasisYear)
print('waste_treat: ', waste_treat)

solidwaste_treat = solid_waste_disposal_costs * get(chemical_price_index, ref_year) / get(chemical_price_index, BasisYear)
print('solidwaste_treat: ', solidwaste_treat)

CO2_OandMcost = 0
print('CO2_OandMcost: ', CO2_OandMcost)

inflated_othervar = INFLATION_FACTOR * (var_misc + royalties + operator_profit + CO2_OandMcost + waste_treat + solidwaste_treat)
print('inflated_othervar: ', inflated_othervar)

variable_cost_column = get_variable_cost_column(operation_range, analysis_index_range, nonenergy_material_price_df, inflation_price_increase_factors, plant_output_kg_per_year, percnt_var, start_time, inflated_othervar)
print('variable_cost_column: ', variable_cost_column)

discounted_value_variable_cost = get(variable_cost_column, YEAR_1) + npv(target_after_tax_nominal_irr, skip(variable_cost_column, 1))
print('discounted_value_variable_cost: ', discounted_value_variable_cost)

total_other_raw = other_material_costs * get(chemical_price_index, ref_year) / get(chemical_price_index, BasisYear)
print('total_other_raw: ', total_other_raw)

inflated_otherraw = total_other_raw * INFLATION_FACTOR
print('inflated_otherraw: ', inflated_otherraw)

other_raw_material_cost_column = get_other_raw_material_cost_column(operation_range, inflation_price_increase_factors, inflated_otherraw, percnt_var, start_time)
print('other_raw_material_cost_column: ', other_raw_material_cost_column)

discounted_value_other_raw_material_cost = get(other_raw_material_cost_column, YEAR_1) + npv(target_after_tax_nominal_irr, skip(other_raw_material_cost_column, 1))
print('discounted_value_other_raw_material_cost: ', discounted_value_other_raw_material_cost)

working_cap_reserve_rows = get_working_cap_reserve_rows(slice(operation_range, end = length(operation_range) - 1), slice(analysis_index_range, end = length(analysis_index_range) - 1), WorkingCap, fixed_cost_column, total_feedstock_cost_column, other_raw_material_cost_column, variable_cost_column)
print('working_cap_reserve_rows: ', working_cap_reserve_rows)

working_cap_reserve_column = get_working_cap_reserve_column(working_cap_reserve_rows)
print('working_cap_reserve_column: ', working_cap_reserve_column)

discounted_value_working_cap_reserve = get(working_cap_reserve_column, YEAR_1) + npv(nominal_irr, skip(working_cap_reserve_column, 1))
print('discounted_value_working_cap_reserve: ', discounted_value_working_cap_reserve)

LCOE_contribution_capital_costs = -(discounted_value_initial_equity_depr_cap + discounted_value_replacement_costs + discounted_value_working_cap_reserve + discounted_value_other_non_depreciable_capital_cost)
print('LCOE_contribution_capital_costs: ', LCOE_contribution_capital_costs)

total_initial_depreciable_capital = -(initial_capital_financed + sum(initial_equity_depr_cap))
print('total_initial_depreciable_capital: ', total_initial_depreciable_capital)

annual_depreciable_capital = get_annual_depreciable_capital(operation_range, replacement_costs, total_initial_depreciable_capital)
print('annual_depreciable_capital: ', annual_depreciable_capital)

recovery_range = range(1, 22)
print('recovery_range: ', recovery_range)

depreciation_calculation_table = get_depreciation_calculation_table(recovery_range, operation_range, depr_type, depr_length, annual_depreciable_capital)
print('depreciation_calculation_table: ', depreciation_calculation_table)

recovery_index_range = seq_along(recovery_range)
print('recovery_index_range: ', recovery_index_range)

depreciation_charges = get_depreciation_charges(analysis_index_range, recovery_index_range, depreciation_calculation_table)
print('depreciation_charges: ', depreciation_charges)

remaining_depreciation_range = range(anal_period+construct, anal_period+construct+depr_length+1)
print('remaining_depreciation_range: ', remaining_depreciation_range)

remaining_depreciation_charges = get_depreciation_charges(remaining_depreciation_range, recovery_index_range, depreciation_calculation_table)
print('remaining_depreciation_charges: ', remaining_depreciation_charges)

total_remaining_depreciation_charges = sum(remaining_depreciation_charges)
print('total_remaining_depreciation_charges: ', total_remaining_depreciation_charges)

depreciation_charges_column = get_depreciation_charges_column(depreciation_charges, analysis_index_range, total_remaining_depreciation_charges, anal_period, construct)
print('depreciation_charges_column: ', depreciation_charges_column)

discounted_value_depreciation_charges = get(depreciation_charges_column, YEAR_1) + npv(nominal_irr, skip(depreciation_charges_column, 1))
print('discounted_value_depreciation_charges: ', discounted_value_depreciation_charges)

LCOE_contribution_depreciation = discounted_value_depreciation_charges * total_tax_rate
print('LCOE_contribution_depreciation: ', LCOE_contribution_depreciation)

LCOE_contribution_principal_payments = -(get(principal_payments_column, YEAR_1) + npv(nominal_irr, skip(principal_payments_column, 1)))
print('LCOE_contribution_principal_payments: ', LCOE_contribution_principal_payments)

LCOE_contribution_operation_costs = -(discounted_value_total_salvage_value + discounted_value_decom_costs + discounted_value_fixed_cost + discounted_value_feedstock_cost + discounted_value_other_raw_material_cost + discounted_value_variable_cost + discounted_value_interest_payments) * (1-total_tax_rate)
print('LCOE_contribution_operation_costs: ', LCOE_contribution_operation_costs)

H2_price_nominal = ((LCOE_contribution_capital_costs + LCOE_contribution_depreciation + LCOE_contribution_principal_payments + LCOE_contribution_operation_costs) / LCOE_contribution_h2_sales_kg) * (1 + inflation_rate) ** construct
print('H2_price_nominal: ', H2_price_nominal)

H2_price_real = H2_price_nominal / INFLATION_FACTOR
print('H2_price_real: ', H2_price_real)

revenue_h2_sales = get_revenue_h2_sales_column(operation_range, inflation_price_increase_factors, H2_price_nominal, plant_output_kg_per_year, percnt_revs, start_time)
print('revenue_h2_sales: ', revenue_h2_sales)

predepreciation_income_column = get_predepreciation_income_column(revenue_h2_sales, salvage_column, decom_costs_column, fixed_cost_column, total_feedstock_cost_column, other_raw_material_cost_column, variable_cost_column, interest_payments_column)
print('predepreciation_income_column: ', predepreciation_income_column)

taxable_income_column = get_taxable_income_column(predepreciation_income_column, depreciation_charges_column)
print('taxable_income_column: ', taxable_income_column)

tax_credit = tax_credit_per_year * CPIinflator
print('tax_credit: ', tax_credit)

Upstream_CO2_taxpYear = 0
print('Upstream_CO2_taxpYear: ', Upstream_CO2_taxpYear)

Proc_CO2_taxpYear = 0
print('Proc_CO2_taxpYear: ', Proc_CO2_taxpYear)

total_taxes_column = get_total_taxes_column(taxable_income_column, total_tax_rate, tax_credit, Upstream_CO2_taxpYear, Proc_CO2_taxpYear)
print('total_taxes_column: ', total_taxes_column)

after_tax_income_column = get_after_tax_income_column(predepreciation_income_column, total_taxes_column)
print('after_tax_income_column: ', after_tax_income_column)

aftertax_post_depreciation_cashflow_column = get_aftertax_post_depreciation_cashflow(initial_equity_depr_cap, replacement_costs, working_cap_reserve_column, other_non_depreciable_capital_cost_column, predepreciation_income_column, total_taxes_column, principal_payments_column)
print('aftertax_post_depreciation_cashflow_column: ', aftertax_post_depreciation_cashflow_column)

cumulative_cashflow_column = get_cumulative_cashflow_column(aftertax_post_depreciation_cashflow_column, analysis_index_range)
print('cumulative_cashflow_column: ', cumulative_cashflow_column)

pretax_cashflow = get_pretax_cashflow_column(initial_equity_depr_cap, replacement_costs, working_cap_reserve_column, other_non_depreciable_capital_cost_column, predepreciation_income_column, principal_payments_column)
print('pretax_cashflow: ', pretax_cashflow)

after_tax_nominal_IRR = irr(aftertax_post_depreciation_cashflow_column)
print('after_tax_nominal_IRR: ', after_tax_nominal_IRR)

pre_tax_nominal_IRR = irr(pretax_cashflow)
print('pre_tax_nominal_IRR: ', pre_tax_nominal_IRR)

