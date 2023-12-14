import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

gas = ct.Solution("gri30.yaml")

reactor_temp = 1000  # K
reactor_pressure = (3700 / 14.7) * 101325  # Pa

gas.set_equivalence_ratio(phi=1.0, fuel="CH4", oxidizer="O2")
gas.TP = reactor_temp, reactor_pressure

phi_range = np.linspace((1 / 1.5) / (1 / 6), (1 / 200) / (1 / 6), 10)

reactor = ct.IdealGasReactor(contents=gas)
reactor_network = ct.ReactorNet([reactor])

# append time 't'
time_history = ct.SolutionArray(gas, extra="t")
tau_array = []

for i in phi_range:
    # How long we want to run our sim
    estimated_ignition_delay = 0.1
    t = 0
    gas.set_equivalence_ratio(phi=i, fuel="CH4", oxidizer="O2")
    gas.TP = reactor_temp, reactor_pressure
    reactor = ct.IdealGasReactor(contents=gas)
    reactor_network = ct.ReactorNet([reactor])

    while t < estimated_ignition_delay:
        t = reactor_network.step()

        # append state
        time_history.append(reactor.thermo.state, t=t)

    reference_species = "OH"

    i_ign = time_history(reference_species).Y.argmax()
    tau = time_history.t[i_ign]
    tau_array.append(tau)
    print(f"computed ignition delay: {tau:.5e} seconds")

mr = 1 / (phi_range * (1 / 6))
fig, ax = plt.subplots()
ax.plot(mr, tau_array, "-o")
ax.set_xlabel("MR")
ax.set_ylabel(r"$\tau$")
ax.set_yscale("log")
plt.show()
