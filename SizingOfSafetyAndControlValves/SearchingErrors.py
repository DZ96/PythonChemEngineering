from fluids.units import *
from fluids.safety_valve import API520_A_g
from fluids.safety_valve import API520_Kv
from CoolProp.CoolProp import PropsSI

P_operation=7.013e+05 # pressure in pa
Temp_operation = 20+273.15
P_std=101325
Temp_std= 15+273.15
Fluid = "Nitrogen" # Here you can choose the working fluid from CoolProp database.
Q = 474.323 #  m^3/h
rho = PropsSI("D", "T", Temp_std, "P", P_std, Fluid)
m_flow=rho*Q
#m_flow_unit = Q_units*rho_units # mass flow rate, kg/h
print("The mass flow is: ",m_flow)
mu = PropsSI("V", "T", Temp_operation, "P", P_operation, Fluid)
print("The viscosity is: ",mu)

A0=API520_A_g(m=24270/3600., T=348., Z=0.90, MW=51., k=1.11, P1=670E3, Kb=1, Kc=1)
print("A0=", A0)