#!interpreter [optional-arg]
# -*- coding: utf-8 -*-
## WORK IN PROGRESS ##

# The Hospitality Data Analysis Python Package
""" hospitalitydatascience will be a comprehensive python package for 
hospitlality data analytics and data science for hospitality industry.

It provides:

- restaurant analytics
- hotel analytics
- airline analytics (coming soon... )

Using multipledispatch function overloading  hospitalitydatasicnece package 
can handle multiple data type scenarios from the given input to provide the correct output. 


The hospitalitydatascience package is licensed under the  GNU General Public License v3 (GPLv3)
"""

# https://www.python.org/dev/peps/pep-0257/
DOCLINES = (__doc__ or '').split("\n")

__author__ = "Jonathan N. Winters"
__copyright__ = 'Copyright 2020, hospitalitydatascience'
__credits__ = ['']
__version__ = "2020.6.dev2"
__license__ = "GNU General Public License v3 (GPLv3)"
__maintainer__ = 'Jonathan N. Winters'
__email__ = 'jnw25@cornell.edu'
__status__ = 'Dev'



# WIP TYPE HINTING VS MULTIPLEDISPTACH 
'''
def hello_name(name: str) -> str:
    return(f"Hello {name}")
'''


# DEPENDENCIES
# Note: Requires -- pip3 install multipledispatch
import multipledispatch
from multipledispatch import dispatch 

import pandas as pd
# Note: Requires -- pip3 install pandas


import numpy as np
# Note: Requires -- pip3 install numpy

# Define a function
def getModuleName():
    return("hospitalitydatascience")


'''
Revenue Analysis
Sales per Square Foot = Annual Sales / Square Foot
'''

'''
# The following methods are used to calculate Revenue Per Available Room
'''
@dispatch(int,int)
def revPAR(rooms_revenue, num_rooms_available):
  """Revenue per Available Room taking 2 Integers."""
  return(rooms_revenue/num_rooms_available)

@dispatch(float,float)
def revPAR(rooms_revenue, num_rooms_available):
  """Revenue per Available Room taking 2 Floats."""
  return(rooms_revenue/num_rooms_available)

@dispatch(list,list)
def revPAR(rooms_revenue, num_rooms_available):
  """Revenue per Available Room taking 2 Lists."""
  return(sum(rooms_revenue)/sum(num_rooms_available))

@dispatch(np.ndarray,np.ndarray)
def revPAR(rooms_revenue_arr, num_rooms_available_arr):
  """Revenue per Available Room taking 2 NumPy Arrays."""
  return(sum(rooms_revenue_arr)/sum(num_rooms_available_arr))

@dispatch(list,int,int)
def revPAR(rooms_revenue_list, num_rooms, num_days):
  """Revenue per Available Room taking a List of rooms revenue and two Integers for the number of rooms and number of days."""
  return(sum(rooms_revenue_list)/(num_rooms * num_days))

@dispatch(np.ndarray,int,int)
def revPAR(rooms_revenue_arr, num_rooms, num_days):
  """Revenue per Available Room taking a NumPy Array of rooms revenue and two Integers for the number of rooms and number of days."""
  return(sum(rooms_revenue_arr)/(num_rooms * num_days))

@dispatch(list,int,float)
def revPAR(rooms_revenue_list, num_rooms, num_days):
  """Revenue per Available Room taking a List of rooms revenue an Integer for the num rooms and a Float for number of days."""
  return(sum(rooms_revenue_list)/(num_rooms * num_days))

@dispatch(np.ndarray,int,float)
def revPAR(rooms_revenue_arr, num_rooms, num_days):
  """Revenue per Available Room taking a NumPy Array of rooms revenue an Integer for the num rooms and a Float for number of days."""
  return(sum(rooms_revenue_arr)/(num_rooms * num_days))

'''
# The following methods are used to calculate Revenue Per Available Seat Hour
RevPASH = Total Revenue ÷ Seat Hours
Seat Hours = Number of Seats x Hours Open
#https://www.lightspeedhq.com/blog/how-to-improve-your-revpash/ 
'''
@dispatch(int,int)
def revPASH(seat_revenue, num_seat_hours):
  """Revenue per Available Seat Hour taking 2 Integers."""
  return(seat_revenue/num_seat_available)

@dispatch(float,float)
def revPASH(seat_revenue, num_seat_available):  
  """Revenue per Available Seat Hour taking 2 Floats."""
  return(seat_revenue/num_seat_available)

@dispatch(list,list)
def revPASH(seat_revenue, num_seat_available):
    """Revenue per Available Seat Hour taking 2 Lists."""
  return(sum(seat_revenue)/sum(num_seat_available))

@dispatch(np.ndarray,np.ndarray)
def revPASH(seat_revenue_arr, num_seat_available_arr):
      """Revenue per Available Seat Hour taking 2 NumPy Arrays."""
  return(sum(seat_revenue_arr)/sum(num_seat_available_arr))

@dispatch(list,int,int)
def revPASH(seat_revenue_list, num_seat, num_days):
    """Revenue per Available Seat Hour taking a List of rooms revenue and two Integers for the number of rooms and number of days."""
  return(sum(seat_revenue_list)/(num_seat * num_days))

@dispatch(list,float,float)
def revPASH(seat_revenue_arr, num_seat, num_days):
  return(sum(seat_revenue_arr)/(num_seat * num_days))


'''
# The following methods are used to calculate Revenue Per Squarefoot
'''
@dispatch(int,int)
def revSQFT(total_revenue, total_sqft):
  """Revenue per Square Foot taking 2 Integers."""
  return(sum(seat_revenue_arr)/(num_seat * num_days))

@dispatch(float,float)
def revSQFT(total_revenue, total_sqft):
      """Revenue per Square Foot taking 2 Floats."""
  return(sum(seat_revenue_arr)/(num_seat * num_days))

@dispatch(list,list)
def revSQFT(revenue_per_location_arr, sqft_per_location_arr):
    """Revenue per Square Foot taking 2 Lists."""
  return(sum(revenue_per_location_arr)/sum(sqft_per_location_arr))

@dispatch(np.ndarray,np.ndarray)
def revSQFT(revenue_per_location_arr, sqft_per_location_arr):
    """Revenue per Square Foot taking 2 NumPy Arrays."""
  return(sum(revenue_per_location_arr)/sum(sqft_per_location_arr))


'''
@dispatch(np.array,np.array)
def revPASH(rooms_revenue, num_rooms_available):
  return(sum(rooms_revenue)/sum(num_rooms_available))
'''


'''
Occupancy Analysis
'''

'''
Restaurant Analysis
https://www.buzztime.com/business/blog/8-restaurant-metrics-you-should-know/ 
https://www.touchbistro.com/blog/21-restaurant-metrics-and-how-to-calculate-them/
Magic Quadrant? Four Quadrant? 
Prime Costs - https://www.lightspeedhq.com/blog/restaurant-prime-cost-formula/
Costs of Goods Sold (CoGS) + Total Labor Cost
PrimeCostPercantage = Prime Cost / Total Sales
CoGS for the period  = (Beginning Inventory of F&B) + (Purchases) – (Ending Inventory) 
Contribution Margin
Food Cost Percentage = Item Cost/Selling Price
Contribution Margin = Selling Price – Cost of Ingredients
Menu Item Profitability = (Number of Items Sold x Menu Price) – (Number of Items Sold x Item Portion Cost)
Average Cover = Total Sales / Number of Covers
Table Turn Time = Number of Guests Served* / Number of Seats
Ticket Time = Closed Time - TimeOfCreation

'''

'''
Operation Analytics
'''

'''
Delivery Analytics



'''

'''
Labor Analysis
Labor Cost Percentage = Labor / Sales
Employee Turnover Rate = (Employees Departed / Number of Employees) x 100
'''

'''
Break Even Point Analysis
'''


'''
HVAC Analysis
'''


'''
Financials
EBITDA = Operating Profit + Amortization Expense + Depreciation Expense
Gross Profit = Total Revenue – CoGS
Gross Profit Margin = (Gross Profit / Total Revenue) x 100
Inventory Turnover = CoGs / ( (Beginning Inventory + Ending Inventory) / 2)
Net Profit Margin = (Gross Sales – Operating Expense) / Gross Sales
Overhead Rate = Total Fixed Costs / Total Amount of Hours Open

'''

'''
Customer Analysis
CAC =  Marketing Expenses / Total New Customers Acquired
Customer Retention Rate =( (Total Customers – Total New Customers) / Total Customers) x 100

'''


'''
Report Builder
 Class, report, flags = QUARTERLY, MONTHLY, ANNUAL
 Week start on Monday or Sunday? 

'''


'''
Mapping
https://data.world/city-of-ny/tjus-cn27
https://data.world/dcopendata/hotels
'''

