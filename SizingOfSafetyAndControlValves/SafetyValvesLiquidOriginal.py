from fluids.safety_valve import API520_A_l
from fluids.safety_valve import API520_Kv
Q = 6814*1.6666666666666667e-05 # L/min to m^3/s
rho = 0.9*999 # specific gravity times density of water kg/m^3
m = rho*Q # mass flow rate, kg/s
print("The mass flow is",m)
overpressure = 0.1
P_design_g = 1724E3 # design pressure, guage
P1 = (1+overpressure)*P_design_g + 101325.0 # upstream relieving pressure, Pa
backpressure = 0.2
mu = 0.388 # viscosity, Pa*s, converted from 2000 Saybolt Universal Seconds
P2 = backpressure*P_design_g + 101325.0 # backpressure, Pa
A0 = API520_A_l(m=m, rho=rho, P1=P1, P2=P2, overpressure=overpressure, Kd=0.65, Kw=0.97, Kc=1.0, Kv=1.0)
print("The start area in m2 is",A0)

from math import pi
D = (A0*4/pi)**0.5
v = Q/A0
Re = rho*v*D/mu
print("The Re number is:", round(Re, 3))

Kv = API520_Kv(Re, '10E') # Compute the viscosity correction
A = API520_A_l(m=m, rho=rho, P1=P1, P2=P2, overpressure=overpressure, Kd=0.65, Kc=1.0, Kv=Kv)*10e4 #Compute the final area
print("The final minimum area in cm2 is:", round(A,3))
d=(4*A/pi)**0.5
print("The necessary diameter in cm is :", round(d,3))
