from fluids.units import *
from fluids.safety_valve import API520_A_g
from fluids.safety_valve import API520_A_l
from fluids.safety_valve import API520_A_steam
from fluids.safety_valve import API520_B
from fluids.safety_valve import API521_noise
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
with open('InputDataSteam.txt') as f:
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
m = a4[0]/3600
backpressure_buildup = a5[0]  #build up backup pressure
overpressure = a6[0]
Fluid = a7[0]


##### Start Block with necessary input data
#Fluid = "Water"
#P_operation=101325+6e05 # pressure in pa
#Temp_operation = 168.229+273.15
#P_std=101325
#Temp_std= 15+273.15 # The standard conditions for Leser safety valves. T=15C and p= 101 325 Pa
#DischargeCoeff=0.6
#Q = 89.024/3600 #  m^3/s
#Q_units = Q*u.m**3/u.s
#backpressure_buildup = 0.04e05 #build up backup pressure
#overpressure = 0.1 # Overpressure as fraction

#m = 351.506/3600 # mass flow rate, kg/s
#m_units = m*u.kg/u.s
#mu = PropsSI("V", "T", Temp_operation, "P", P_operation, Fluid)
#mu_unit=mu*u.Pa*u.s

m_units = m*u.kg/u.s
print("The mass flow is:", round(m_units,3))
P1 = (1+overpressure)*P_operation + 101325.0 # upstream relieving pressure, Pa
#P2 = backpressure_buildup + 101325.0 # backpressure, Pa


Kb = API520_B(P_operation, backpressure_buildup, overpressure)
A = API520_A_steam(m=m, T=Temp_operation, P1=P1, Kd=DischargeCoeff, Kb=Kb, Kc=1.0)*1e06
#A_units= A*1e06*u.mm**2
A_units= A*u.mm**2
print("The area is",A_units)
from math import pi
d = (A*4/pi)**0.5
d_units = (A_units*4/pi)**0.5
print("The diameter is",round(d_units,3))


results = {"The discharge area in mm2 is":A, "The necessary diameter in mm is ": d, "The mass flow in kg per sec is": m}
with open("ResultsAsDicSteam.txt", "w") as f:
    f.write(str(results))
    f.close()

# reading line by line
with open('ResultsAsDicSteam.txt', 'r') as f:
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

###### Optional Block for calculating the noise
#Noise = API521_noise(m=m, P1=P1, P2=101325, c=500.4, r=1)
#print("The noise in decibels is", Noise)
