from fluids.units import *
from fluids.safety_valve import API520_A_g
from fluids.safety_valve import API520_A_l
from CoolProp.CoolProp import PropsSI
from math import pi
from itertools import islice
import re # importing re module for creating regex expression

a1 = []
a2 = []
a3 = []
a4 = []
a5 = []
a6 = []
a7 = []
with open('InputDataLiquid.txt') as f:
    for line in islice(f, 1, None):
        data = line.split()
        a1.append(float(data[0]))
        a2.append(float(data[1]))
        a3.append(float(data[2]))
        a4.append(float(data[3]))
        a5.append(float(data[4]))
        a6.append(float(data[5]))
        a7.append(str(data[6]))

P_std=101325
Temp_std= 15+273.15 # The standard conditions for Leser safety valves. T=15C and p= 101 325 Pa
P_operation = a1[0] # pressure in pa
Temp_operation = a2[0] # Temperature in Kelvin
DischargeCoeff= a3[0]
Q = a4[0]
backpressure_buildup = a5[0]  #build up backup pressure
overpressure = a6[0]
Fluid = a7[0]
Q_units = Q*u.m**3/u.h

##### OLD Start Block with necessary input data
#Fluid = "Water"
#P_operation=101325+6e05 # pressure in pa
#Temp_operation = 25+273.15
#P_std=101325
#Temp_std= 15+273.15 # The standard conditions for Leser safety valves. T=15C and p= 101 325 Pa
#DischargeCoeff=0.4
#Q = 7.696/3600 #  m^3/s
#Q_units = Q*u.m**3/u.s
#backpressure_buildup = 0.018e05 #build up backup pressure
#overpressure = 0.1 # Overpressure as fraction
#### OLD CODE END

rho = PropsSI("D", "T", Temp_std, "P", P_std, Fluid)
rho_units = PropsSI("D", "T", Temp_std, "P", P_std, Fluid)*u.kg/u.m**3
m = rho*Q/3600 # mass flow rate, kg/s
m_units = rho_units*Q_units
mu = PropsSI("V", "T", Temp_operation, "P", P_operation, Fluid)
mu_unit=mu*u.Pa*u.s
print("The mass flow is:", round(m_units,3))
#print("The mass flow in kg/h is",round(m*3600,3) ) # For easier comparison with Leser PDFs
print("The density is:", rho_units)
#print("The viscosity is", mu_unit)
P1 = (1+overpressure)*P_operation + 101325.0 # upstream relieving pressure, Pa
P2 = backpressure_buildup + 101325.0 # backpressure, Pa

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

Kv = API520_Kv(Re) #Compute the viscosity correction # ERROR IN KV
#print("Kv is", Kv)
Kv_f=float(Kv)
#print("Kv_f",Kv_f)
A = API520_A_l(m=m, rho=rho, P1=P1, P2=P2, overpressure=overpressure, Kd=DischargeCoeff, Kc=1.0, Kv=Kv_f)*1e06#Compute the final area
A_units = A*u.mm**2
A_stripped = round(API520_A_l(m=m, rho=rho, P1=P1, P2=P2, overpressure=overpressure, Kd=DischargeCoeff, Kc=1.0, Kv=Kv_f)*1e6, 3)
print("The final minimum area is:", round(A_units,3))
#print("A_stripped",A_stripped)
d=(4*A/pi)**0.5*u.mm
d_stripped = (4*A_stripped/pi)**0.5
print("The final minimum diameter is :", round(d,3))


results = {"The discharge area in mm is":A_stripped, "The necessary diameter in mm is ": d_stripped, "The volume flow in m3 per hours is": Q}
with open("ResultsAsDicLiquid.txt", "w") as f:
    f.write(str(results))
    f.close()

# reading line by line
with open('ResultsAsDicLiquid.txt', 'r') as f:
    # looping the para and iterating
    # each line
    text = f.read()

    # getting the pattern for [],(),{}
    # brackets and replace them to empty  string
    # creating the regex pattern & use re.sub()
    patn = re.sub(r"[\([{})''\]]", '', text)
#print(patn)

with open("Results.txt", "w") as f:
    f.write(patn)
    f.close()