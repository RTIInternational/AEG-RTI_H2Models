#
# This file is programmatically generated by py_writer.py; do not edit
#
from h2a.globals import CEPCIinflator, CPIinflator
from h2a.helpers import get


def calculate_capital_investment_cost(capital_investment):
    return (
        get(capital_investment, "cost")
        * CEPCIinflator
        * CPIinflator
        * get(capital_investment, "installation_cost_factor")
    )


def capital_investment_costs(capital_investments):
    """H2A Total Direct Capital Cost"""
    return list(
        map(
            lambda capital_investment: calculate_capital_investment_cost(
                capital_investment
            ),
            capital_investments,
        )
    )
