import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline as CS
from scipy.optimize import minimize
df = pd.read_csv("daily-treasury-rates.csv")

X = np.array([.083333, 1/6, .25, 1/3,.5,1,2,3,5,7,10,20,30])
y = np.array(df.iloc[0,1:])
spline = CS(X,y)
#tenor in years, freq in times per year, face in dollars, coupon in percentage points.
def calc_price(freq, tenor, face, coupon_rate, spread):
    x_payments = np.linspace(1/freq,tenor,freq*tenor)
    total_flow_value = 0
    for i in x_payments:
        rfr = spline(i) / 100
        yld = rfr + (spread / 10000)
        coupon_payment = (coupon_rate / 100) * face / freq
        
        discounted_flow = coupon_payment/((1+yld)**i)
        
        total_flow_value += discounted_flow
      
    total_flow_value += face/((1+yld)**tenor)
   
    return total_flow_value

def error_term(spread, freq, tenor, face, coupon_rate, price):
    return (price-calc_price(freq, tenor, face, coupon_rate, spread))**2

#an example

x0 = [0]
p0 = (2,10,100,10,102)

min_obj = minimize(error_term, x0, args=p0,method='SLSQP')
print(min_obj.x, min_obj.message, min_obj.success)
print(calc_price(1,10,1000,10,0))