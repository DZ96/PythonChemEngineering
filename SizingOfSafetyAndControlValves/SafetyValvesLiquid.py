from fluids.units import *
from fluids.safety_valve import API520_A_g
from fluids.safety_valve import API520_A_l
from CoolProp.CoolProp import PropsSI
from math import pi
from itertools import islice
import re # importing re module for creating regex expression

##### Start Block with necessary input data
Fluid = "Water"
P_operation=101325+6e05 # pressure in pa
Temp_operation = 25+273.15
P_std=101325
Temp_std= 15+273.15 # The standard conditions for Leser safety valves. T=15C and p= 101 325 Pa
DischargeCoeff=0.4
Q = 7.696/3600 #  m^3/s
Q_units = Q*u.m**3/u.s
backpressure_buildup = 0.018e05 #build up backup pressure
overpressure = 0.1 # Overpressure as fraction


rho = PropsSI("D", "T", Temp_std, "P", P_std, Fluid)
rho_units = PropsSI("D", "T", Temp_std, "P", P_std, Fluid)*u.kg/u.m**3
m = rho*Q # mass flow rate, kg/s
m_units = rho_units*Q_units
mu = PropsSI("V", "T", Temp_operation, "P", P_operation, Fluid)
mu_unit=mu*u.Pa*u.s
print("The mass flow is:", round(m_units,3))
print("The mass flow in kg/h is",round(m*3600,3) ) # For easier comparison with Leser PDFs
print("The density is:", rho_units)
#print("The viscosity is", mu_unit)
P1 = (1+overpressure)*P_operation + 101325.0 # upstream relieving pressure, Pa
P2 = backpressure_buildup + 101325.0 # backpressure, Pa

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

A0 = API520_A_l(m=m, rho=rho, P1=P1, P2=P2, overpressure=overpressure, Kd=DischargeCoeff, Kw=0.97, Kc=1.0, Kv=1.0)
A0_units= A0*1e06*u.mm**2
print("The start area is",A0_units)

from math import pi
D = (A0*4/pi)**0.5
D_units = (A0_units*4/pi)**0.5
print("The initial diamater is", round(D_units,3))
v = Q/A0
Re = rho*v*D/mu
#print("The velocity is:",v)
#print("The Re number is:", round(Re, 3))

Kv = API520_Kv(Re, '10E') # Compute the viscosity correction
A = API520_A_l(m=m, rho=rho, P1=P1, P2=P2, overpressure=overpressure, Kd=DischargeCoeff, Kc=1.0, Kv=Kv)*1e6*u.mm**2 #Compute the final area
print("The final minimum area is:", round(A,3))
d=(4*A/pi)**0.5
print("The final necessary diameter is :", round(d,3))

