import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import cantera as ct

print(f"Runnning Cantera version: {ct.__version__}")

mr = 1
phi = (1 / mr) / (1 / 4)  # 4 for methalox, anyways

plt.rcParams["axes.labelsize"] = 18
plt.rcParams["xtick.labelsize"] = 12
plt.rcParams["ytick.labelsize"] = 12
plt.rcParams["figure.autolayout"] = True
plt.rcParams["figure.dpi"] = 120

plt.style.use("ggplot")

gas = ct.Solution("gri30.yaml")

# Define the reactor temperature and pressure
reactor_temperature = 1000  # Kelvin
reactor_pressure = 101325  # Pascals

gas.TP = reactor_temperature, reactor_pressure

# Define the fuel, oxidizer and set the stoichiometry
gas.set_equivalence_ratio(phi=phi, fuel="CH4", oxidizer="O2")

# Create a batch reactor object and add it to a reactor network
# In this example, the batch reactor will be the only reactor
# in the network
# r = ct.IdealGasReactor(contents=gas, name="Batch Reactor")
r = ct.Reactor(contents=gas, name="Batch Reactor")
reactor_network = ct.ReactorNet([r])

# use the above list to create a DataFrame
time_history = ct.SolutionArray(gas, extra="t")


def ignition_delay(states, species):
    """
    This function computes the ignition delay from the occurence of the
    peak in species' concentration.
    """
    i_ign = states(species).Y.argmax()
    return states.t[i_ign]


reference_species = "oh"

# Tic
t0 = time.time()

# This is a starting estimate. If you do not get an ignition within this time, increase it
estimated_ignition_delay_time = 1000
t = 0

counter = 1
while t < estimated_ignition_delay_time:
    t = reactor_network.step()
    if not counter % 10:
        # We will save only every 10th value. Otherwise, this takes too long
        # Note that the species concentrations are mass fractions
        time_history.append(r.thermo.state, t=t)
    counter += 1

# We will use the 'oh' species to compute the ignition delay
tau = ignition_delay(time_history, reference_species)

# Toc
t1 = time.time()

print(f"Computed Ignition Delay: {tau:.3e} seconds. Took {t1-t0:3.2f}s to compute")

# If you want to save all the data - molefractions, temperature, pressure, etc
# uncomment the next line
# time_history.to_csv("time_history.csv")

plt.figure()
plt.plot(time_history.t, time_history(reference_species).Y, "-o")
plt.xlabel("Time (s)")
plt.ylabel("$Y_{OH}$")

plt.xlim([0, 0.05])
plt.arrow(
    0,
    0.008,
    tau,
    0,
    width=0.0001,
    head_width=0.0005,
    head_length=0.001,
    length_includes_head=True,
    color="r",
    shape="full",
)
plt.annotate(
    r"$Ignition Delay: \tau_{ign}$", xy=(0, 0), xytext=(0.01, 0.0082), fontsize=16
)
"""
NTC Plotting -----------------------------------------------------------------------------------------------------------
"""

# Make a list of all the temperatures we would like to run simulations at
T = np.hstack((np.arange(1800, 900, -100), np.arange(975, 475, -25)))

estimated_ignition_delay_times = np.ones_like(T, dtype=float)

# Make time adjustments for the highest and lowest temperatures. This we do empirically
estimated_ignition_delay_times[:6] = 6 * [0.1]
estimated_ignition_delay_times[-4:-2] = 10
estimated_ignition_delay_times[-2:] = 100

# Now create a SolutionArray out of these
ignition_delays = ct.SolutionArray(
    gas, shape=T.shape, extra={"tau": estimated_ignition_delay_times}
)
ignition_delays.set_equivalence_ratio(phi=phi, fuel="CH4", oxidizer="O2")
ignition_delays.TP = T, reactor_pressure

for i, state in enumerate(ignition_delays):
    # Setup the gas and reactor
    gas.TPX = state.TPX
    # r = ct.IdealGasReactor(contents=gas, name="Batch Reactor")
    r = ct.Reactor(contents=gas, name="Batch Reactor")
    reactor_network = ct.ReactorNet([r])

    reference_species_history = []
    time_history = []

    t0 = time.time()

    t = 0
    while t < estimated_ignition_delay_times[i]:
        t = reactor_network.step()
        time_history.append(t)
        reference_species_history.append(gas[reference_species].X[0])

    i_ign = np.array(reference_species_history).argmax()
    tau = time_history[i_ign]
    t1 = time.time()

    print(
        f"Computed Ignition Delay: {tau:.3e} seconds for T={state.T}K. Took {t1 - t0:3.2f}s to compute"
    )

    ignition_delays[i].tau = tau

fig = plt.figure()
ax = fig.add_subplot(111)
ax.semilogy(1000 / (ignition_delays.T * (9 / 5)), ignition_delays.tau, "o-")
ax.set_ylabel("Ignition Delay (s)")
ax.set_xlabel(r"$\frac{1000}{T (R)}$", fontsize=18)

# Add a second axis on top to plot the temperature for better readability
ax2 = ax.twiny()
ticks = ax.get_xticks()
ax2.set_xticks(ticks)
ax2.set_xticklabels((1000 / ticks).round(1))
ax2.set_xlim(ax.get_xlim())
ax2.set_xlabel("Temperature: $T(R)$")
