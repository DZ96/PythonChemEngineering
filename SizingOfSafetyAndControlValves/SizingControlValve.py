# This program will perform sizing of a control valve for a luqid
# The liquid is water. The case can be taken from
# https://fluids.readthedocs.io/Examples/Crane%20TP%20410%20Solved%20Problems/7.27%20Sizing%20Control%20Valves%20for%20Liquid%20Service.html
# I use SI Units instead imperial one

from fluids.units import *

#rho = 60.998*u.lb/u.ft**3 # Water Density imperial units
rho = 977.09*u.kg/u.m**3 # Density in SI Units
mu = 0.00039*u.Pa*u.s #Viscosity in Pa*s
Psat = 0.327*u.bar
Pc = 217.75*u.atm

Q = 946.353*u.l/u.min
P1 = 5.5572*u.bar
P2 = 4.8812*u.bar

NPS, D_pipe, Do_pipe, t = nearest_pipe(NPS=4, schedule=40)

Cvs = [41*u.gal/u.min, 73*u.gal/u.min, 114*u.gal/u.min, 175*u.gal/u.min]
D_valves = [2*u.inch, 2.5*u.inch, 3.0*u.inch, 4*u.inch]

for d, Cv in zip(D_valves, Cvs):
    Kv = size_control_valve_l(rho=rho, Psat=Psat, Pc=Pc, mu=mu, P1=P1, P2=P2, Q=Q, D1=D_pipe, D2=D_pipe,
                             d=d, FL=0.9, Fd=1, allow_choked=True,
                             allow_laminar=True, full_output=False)
    Cv_calc = Kv_to_Cv(Kv)
    if Cv > Cv_calc:
        print('Minimum size is %s' %d)
        break
print('Calculated Cv is %s' %(round(Cv_calc, 3)))
Kv_calc=Cv_to_Kv(Cv)
print("The calculated Kv is:", round(Kv_calc, 3))