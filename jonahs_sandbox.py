import sys
import cantera as ct
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"

plt.ion()

T = 1000 * 5 / 9
P = 3600 * 101325 / 14.7

OF = 15

gas = ct.Solution("gri30.yaml")

gas.Y = {"CH4": 0.935, "C2H6": 0.062, "C3H8": 0.002, "N2": 0.0002, "O2": OF}
gas.TP = T, P

# gas1()
#
# gas1.equilibrate('HP')
# gas1()
#
# rf = gas1.forward_rates_of_progress
# rr = gas1.reverse_rates_of_progress
# for i in range(gas1.n_reactions):
#    if gas1.is_reversible(i) and rf[i] != 0.0:
#        print(' %4i  %10.4g  ' % (i, (rf[i] - rr[i])/rf[i]))
#

r = ct.ConstPressureReactor(gas)

sim = ct.ReactorNet([r])
time = 0.0
states = ct.SolutionArray(gas, extra=["t"])

print("%10s %10s %10s %14s" % ("t [s]", "T [K]", "P [Pa]", "u [J/kg]"))
# for n in range(100):
#    time += 1.e+4
#    sim.advance(time)
#    states.append(r.thermo.state, t=time*1e3)
#    print('%10.3e %10.3f %10.3f %14.6e' % (sim.time, r.T,
#                                           r.thermo.P, r.thermo.u))
time = 0.0
tout = 1e8
stop_flag = False
temp = T
while time < tout:
    time = sim.step()
    states.append(r.thermo.state, t=time * 1e3)
    y = r.Y[gas.species_index("CH4")]
    temp = r.T

    if y < 1e-13:
        reactime = time
        print("found it")

    # if temp > 1.5 * T and stop_flag == False:
    #     tout = time * 1.5
    #     stop_flag = True

    print("%10.3e %10.3f %10.3f %14.6e" % (sim.time, r.T, r.thermo.P, r.thermo.u))

sf = pd.DataFrame({"t": states.t, "T": states.T})

fig = px.line(sf, x="t", y="T", title="Temp vs Time")
fig = px.scatter(sf, x="t", y="T", title="Temp vs Time")
fig.show()


plt.clf()
plt.subplot(2, 2, 1)
plt.plot(states.t, states.T)
plt.xlabel("Time (ms)")
plt.ylabel("Temperature (K)")
plt.grid()
plt.subplot(2, 2, 2)
plt.plot(states.t, states.X[:, gas.species_index("CH4")])
plt.xlabel("Time (ms)")
plt.ylabel("CH4 Mole Fraction")
plt.grid()
plt.subplot(2, 2, 3)
plt.plot(states.t, states.X[:, gas.species_index("O2")])
plt.xlabel("Time (ms)")
plt.ylabel("O2 Mole Fraction")
plt.grid()
plt.subplot(2, 2, 4)
plt.plot(states.t, states.X[:, gas.species_index("H2O")])
plt.xlabel("Time (ms)")
plt.ylabel("H2O Mole Fraction")
plt.grid()
plt.tight_layout()
plt.show()
