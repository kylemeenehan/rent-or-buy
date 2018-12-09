import numpy as np
import pandas as pd
import operator
from functools import reduce

# global constants

allocated_monthly_funds = 20000
inflation_rate = 0.04
investment_rate = 0.09

# property purchase

property_price = 1000000
initiation_fee = 50000

bond_interest_rate = 0.105
bond_duration_in_years = 20

property_annual_appreciation = 0.02

purchase_costs = {
    "tax": 100,
    "levies": 1500,
    "utilities": 1000,
    "maintenance": 500,
    "wages": 1500
}

# property rental

rental_costs = {
    "rent": 6000,
    "utilities": 1000,
    "wages": 2700
}

def total_paid_for_monthly_cost(monthly_cost, annual_inflation=inflation_rate):
    amount = np.fv(rate=annual_inflation, nper=bond_duration_in_years, pmt=monthly_cost*12, pv=0)
    return round(amount, 2)

def cost_of_scenario(cost_dict):
    total_cost = 0;

    for cost_type, amount in cost_dict.items():
        total_cost_for_type = total_paid_for_monthly_cost(amount)
        total_cost = total_cost + total_cost_for_type
        print(f"Total cost of {cost_type}: {round(total_cost_for_type, 2)}")
    return total_cost


# results

print("==== Property purchase ===")

total_loan_amount = property_price + initiation_fee
bond_monthly_payment = np.pmt(bond_interest_rate / 12, bond_duration_in_years * 12, total_loan_amount)
property_final_value = -np.fv(rate=property_annual_appreciation, nper=bond_duration_in_years, pmt=0, pv=property_price)

purchase_other_monthly_costs = reduce(operator.add, [x for x in purchase_costs.values()])

initial_monthly_investment_amount = allocated_monthly_funds \
    + bond_monthly_payment \
    - reduce(operator.add, [x for x in purchase_costs.values()])
investment_final_value = -np.fv(rate=investment_rate/12, nper=bond_duration_in_years*12, pmt=initial_monthly_investment_amount, pv=0)

purchase_nett_assets = round(investment_final_value + property_final_value, 2)

output_purchase = f"""
Total loan amount: {total_loan_amount}
Monthly bond payment: {round(bond_monthly_payment, 2)}
Monthly other costs: {purchase_other_monthly_costs}
Total monthly: {round(bond_monthly_payment - purchase_other_monthly_costs, 2)}
Property value once paid off: {round(property_final_value, 2)}

Monthly investment amount: {round(initial_monthly_investment_amount, 2)}
Final value of investment: {round(investment_final_value, 2)}

Nett assets: {purchase_nett_assets:,}

"""
print(output_purchase)


print("==== Property rental ===")

initial_monthly_investment_amount = allocated_monthly_funds - reduce(operator.add, [x for x in rental_costs.values()])
investment_final_value = -np.fv(rate=investment_rate/12, nper=bond_duration_in_years*12, pmt=initial_monthly_investment_amount, pv=0)

rent_net_assets = investment_final_value

print(f"Initial monthly rent: {rental_costs['rent']}")

total_rent_cost = cost_of_scenario(rental_costs);
print(f"Total of all costs in rental scenario: {round(total_rent_cost, 2)}")

output_rent = f"""
Initial monthly investment:{initial_monthly_investment_amount}
Final value of investment: {round(investment_final_value):,}
"""

print(output_rent)

scenario_difference = round(abs(rent_net_assets - purchase_nett_assets))

print("Rent or purchase?\n")
if rent_net_assets > purchase_nett_assets:
    print( "RENT")
elif purchase_nett_assets > rent_net_assets:
    print("PURCHASE")
else:
    print("NO DIFFERENCE")

print(f"Difference: {scenario_difference:,}")
