from fluids.units import *
from fluids.safety_valve import API520_A_g
from CoolProp.CoolProp import PropsSI
from math import pi
from itertools import islice

# The "standard" conditions for Leser safety valves. T=15C and p= 101 325 Pa. This is needed for comparison
P_std=101325
Temp_std= 15+273.15

a1 = []
a2 = []
a3 = []
a4 = []
a5 = []
a6 = []
a7 = []

with open('InputData.txt') as f:
    for line in islice(f, 1, None):
        data = line.split()
        a1.append(float(data[0]))
        a2.append(float(data[1]))
        a3.append(float(data[2]))
        a4.append(float(data[3]))
        a5.append(float(data[4]))
        a6.append(float(data[5]))
        a7.append(str(data[6]))


P_operation = a1[0] # pressure in pa
Temp_operation = a2[0] # Temperature in Kelvin
DischargeCoeff= a3[0]
Q = a4[0]
backpressure_buildup = a5[0]  #build up backup pressure
overpressure = a6[0]
Fluid = a7[0]
Q_units = Q*u.m**3/u.h

#######Old Code with Input inside the Script
##### Start Block with necessary input data
#P_operation=101325+5e05 # pressure in pa
#Temp_operation = 25+273.15
#P_std=101325
#Temp_std= 15+273.15
#DischargeCoeff=0.688
#Q = 1325.396 #  m^3/h # At "standard" conditions for Leser safety valves. T=15C and p= 101 325 Pa It is needed for comparison
#Q_units = Q*u.m**3/u.h
#Fluid = "Oxygen" # Here you can choose the working fluid from CoolProp database.
#backpressure_buildup = 2.335e+05 #build up backup pressure
#overpressure = 0.1 # Overpressure as fraction
##### End Block with necessary input data


MolarMass = PropsSI("M", Fluid)*1e03 # Converting the molar mass from kg/mol to g/mol
#print("The Molar Mass is", round(MolarMass,3)) # The print command was to check the value.
rho = PropsSI("D", "T", Temp_std, "P", P_std, Fluid)
rho_units = PropsSI("D", "T", Temp_std, "P", P_std, Fluid)*u.kg/u.m**3
Z_factor= PropsSI("Z", "T", Temp_std, "P", P_std, Fluid)
#print("The compressiblilty factor is equal to: ", Z_factor) # Just to check the value. Output generally not interesting
m_flow=rho*Q
m_flow_unit = Q_units*rho_units # mass flow rate, kg/h
print("The mass flow is: ",m_flow_unit)
mu = PropsSI("V", "T", Temp_operation, "P", P_operation, Fluid)
mu_unit=mu*u.Pa*u.s
#print("The viscosity is: ",mu_unit) # Just to check the value. Output generally not interesting


P1 = (1+overpressure)*P_operation + 101325.0 # upstream relieving pressure, Pa
A0=API520_A_g(m=m_flow/3600., T=Temp_operation, Z=Z_factor, MW=MolarMass, k=1.11, P1=P1, P2=backpressure_buildup, Kd=DischargeCoeff)*1e06*u.mm**2
#A0=API520_A_g(m=m_flow/3600., T=Temp_operation, Z=Z_factor, MW=28., k=1.11, P1=P1, P2=backpressure_buildup, Kd=0.6)*1*10**6
print("The discharge area is",round(A0, 3))
d=((4*A0/pi)**0.5)
print("The necessary diameter  is :", round(d,3))

