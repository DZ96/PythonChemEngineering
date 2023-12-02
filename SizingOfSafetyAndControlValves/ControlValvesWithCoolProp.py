from scipy.constants import *
from fluids.control_valve import size_control_valve_l
#from thermo.chemical import Chemical
from CoolProp.CoolProp import PropsSI

#Example from https://fluids.readthedocs.io/tutorial.html#friction-factors Control valve sizing Liquid flow

P1 = 300*psi + psi # to Pa
P2 = 275*psi + psi # to Pa
Temp = 273.15 + 45 # to K
P=(P1+P2)/2
rho = PropsSI('D', 'T', Temp, 'P', 100e5, 'propane')
Psat = PropsSI('P', 'T', Temp, 'Q', 1, 'propane')
Pc = PropsSI('Pcrit', 'T', Temp, 'Q', 1, 'propane')
mu =  PropsSI('V', 'T', Temp, 'Q', 1, 'propane')
Q = 800*gallon/minute # to m^3/s
D1 = D2 = 8*inch # to m
d = 3*inch # to m
Kv = size_control_valve_l(rho, Psat, Pc, mu, P1, P2, Q, D1, D2, d, FL=1, Fd=1)
print("The calculated Kv value is: ",Kv)