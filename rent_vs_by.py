import numpy as np
import pandas as pd
import operator
from functools import reduce
import helpers

# global constants

allocated_monthly_funds = 20000
inflation_rate = 0.04
investment_rate = 0.09

# property purchase

property_price = 1000000
transfer_duty = helpers.transfer_duty(property_price)
monthly_property_taxes = helpers.monthly_property_taxes(property_price)
print(f"monthly_property_taxes: {monthly_property_taxes}")
legal_fees = 50000

bond_interest_rate = 0.105
bond_duration_in_years = 20

property_annual_appreciation = 0.03

purchase_costs = {
    "tax": monthly_property_taxes,
    "levies": -1500,
    "utilities": -1000,
    "maintenance": -500,
    "wages": -1500
}

# property rental

rental_costs = {
    "rent": -9000,
    "utilities": -1000,
    "wages": -2700
}


# results

print("==== Property purchase ===")

total_loan_amount = property_price + transfer_duty + legal_fees
property_final_value = -np.fv(rate=property_annual_appreciation, nper=bond_duration_in_years, pmt=0, pv=property_price)

bond_monthly_payment = np.pmt(bond_interest_rate / 12, bond_duration_in_years * 12, total_loan_amount)
purchase_other_monthly_costs = reduce(operator.add, [x for x in purchase_costs.values()])
purchase_total_monthly_costs = bond_monthly_payment + purchase_other_monthly_costs

purchase_initial_monthly_investment_amount = allocated_monthly_funds \
    + bond_monthly_payment \
    + purchase_other_monthly_costs
purchase_investment_final_value = -np.fv(rate=investment_rate/12, nper=bond_duration_in_years*12, pmt=purchase_initial_monthly_investment_amount, pv=0)

purchase_nett_assets = round(purchase_investment_final_value + property_final_value, 2)

print(f"""
Property price: {property_price:,}
Transfer duty: {round(transfer_duty, 2):,}
Total loan amount: {total_loan_amount:,}
Monthly bond payment: {round(bond_monthly_payment, 2):,}
Monthly other costs: {purchase_other_monthly_costs:,}
Total monthly: {round(purchase_total_monthly_costs, 2):,}
Property value once paid off: {round(property_final_value, 2):,}
Monthly investment amount: {round(purchase_initial_monthly_investment_amount, 2):,}
Final value of investment: {round(purchase_investment_final_value, 2):,}

Nett assets: {purchase_nett_assets:,}
""")


print("==== Property rental ===")

rent_initial_monthly_investment_amount = allocated_monthly_funds + reduce(operator.add, [x for x in rental_costs.values()])
rent_investment_final_value = -np.fv(rate=investment_rate/12, nper=bond_duration_in_years*12, pmt=rent_initial_monthly_investment_amount, pv=0)

rent_net_assets = rent_investment_final_value
rent_total_monthly_costs = reduce(operator.add, [x for x in rental_costs.values()])
total_rent_costs = helpers.cost_of_scenario(rental_costs, inflation_rate, bond_duration_in_years);

print(f"""
Initial monthly rent: {rental_costs['rent']:,}
Initial monthly total cost: {rent_total_monthly_costs:,}
Total of all costs in rental scenario: {round(total_rent_costs, 2):,}
Initial monthly investment:{rent_initial_monthly_investment_amount:,}

Final value of investment: {round(rent_investment_final_value):,}
""")

d = {
    "purchase": [
        f"{round(purchase_total_monthly_costs, 2):,}",
        f"{round(purchase_initial_monthly_investment_amount, 2):,}",
        f"{round(property_final_value, 2):,}",
        f"{round(purchase_investment_final_value, 2):,}",
        f"{round(purchase_nett_assets, 2):,}",
    ],
    "rent": [
        f"{round(rent_total_monthly_costs, 2):,}",
        f"{round(rent_initial_monthly_investment_amount, 2):,}",
        f"N/A",
        f"{round(rent_investment_final_value, 2):,}",
        f"{round(rent_investment_final_value, 2):,}",
    ]
}

results = pd.DataFrame(d, index=["Initial monthly payments",
                       "Initial monthly investment",
                       "Property final value",
                       "Investment final value",
                       "Final nett assets"])

print(results)

scenario_difference = round(abs(rent_net_assets - purchase_nett_assets))

print("\nRent or purchase?\n")
if rent_net_assets > purchase_nett_assets:
    print( "RENT")
elif purchase_nett_assets > rent_net_assets:
    print("PURCHASE")
else:
    print("NO DIFFERENCE")

print(f"Difference: {scenario_difference:,}")
