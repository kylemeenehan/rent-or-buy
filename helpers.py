import numpy as np

def transfer_duty(property_price):
    if (property_price < 500000):
        return 0
    elif (property_price >= 500000 and property_price <= 1000000):
        return property_price * 0.05
    else:
        return property_price * 0.08

def monthly_property_taxes(market_value):
    if (market_value <= 200000):
        return 0
    else:
        rateable_value = market_value - 200000
        return -(rateable_value * 0.006161) / 12


def total_paid_for_monthly_cost(monthly_cost, annual_inflation, duration_in_years):
    amount = np.fv(rate=annual_inflation, nper=duration_in_years, pmt=monthly_cost*12, pv=0)
    return round(amount, 2)

def cost_of_scenario(cost_dict, annual_inflation, duration_in_years):
    total_cost = 0;

    for cost_type, amount in cost_dict.items():
        total_cost_for_type = total_paid_for_monthly_cost(amount, annual_inflation, duration_in_years)
        total_cost = total_cost + total_cost_for_type
        print(f"Total cost of {cost_type}: {round(total_cost_for_type, 2)}")
    return round(total_cost, 2)


