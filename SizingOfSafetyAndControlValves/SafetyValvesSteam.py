from fluids.units import *
from fluids.safety_valve import API520_A_g
from fluids.safety_valve import API520_A_l
from fluids.safety_valve import API520_A_steam
from fluids.safety_valve import API520_B
from CoolProp.CoolProp import PropsSI
from math import pi
from itertools import islice
import re # importing re module for creating regex expression

##### Start Block with necessary input data
Fluid = "Water"
P_operation=101325+6e05 # pressure in pa
Temp_operation = 168.229+273.15
P_std=101325
Temp_std= 15+273.15 # The standard conditions for Leser safety valves. T=15C and p= 101 325 Pa
DischargeCoeff=0.6
#Q = 89.024/3600 #  m^3/s
#Q_units = Q*u.m**3/u.s
backpressure_buildup = 0.04e05 #build up backup pressure
overpressure = 0.1 # Overpressure as fraction

m = 351.506/3600 # mass flow rate, kg/s
m_units = m*u.kg/u.s
#mu = PropsSI("V", "T", Temp_operation, "P", P_operation, Fluid)
#mu_unit=mu*u.Pa*u.s
print("The mass flow is:", round(m_units,3))
P1 = (1+overpressure)*P_operation + 101325.0 # upstream relieving pressure, Pa
#P2 = backpressure_buildup + 101325.0 # backpressure, Pa

##### OLD CODE
#Q = 6814*1.6666666666666667e-05 # L/min to m^3/s
#rho = 0.9*999 # specific gravity times density of water kg/m^3
#m = rho*Q # mass flow rate, kg/s
#print("The mass flow is",m)
#overpressure = 0.1
#P_design_g = 1724E3 # design pressure, guage
#P1 = (1+overpressure)*P_design_g + 101325.0 # upstream relieving pressure, Pa
#backpressure = 0.2
#mu = 0.388 # viscosity, Pa*s, converted from 2000 Saybolt Universal Seconds
#P2 = backpressure*P_design_g + 101325.0 # backpressure, Pa
#A0 = API520_A_l(m=m, rho=rho, P1=P1, P2=P2, overpressure=overpressure, Kd=0.65, Kw=0.97, Kc=1.0, Kv=1.0)
#print("The start area in m2 is",A0)
##### END OLD CODE

Kb = API520_B(P_operation, backpressure_buildup, overpressure)
A = API520_A_steam(m=m, T=Temp_operation, P1=P1, Kd=DischargeCoeff, Kb=Kb, Kc=1.0)
A_units= A*1e06*u.mm**2
print("The start area is",A_units)
from math import pi
d = (A_units*4/pi)**0.5
print("The diameter is",round(d,3))





