import fastf1

import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import fastf1
import fastf1.plotting

fastf1.plotting.setup_mpl()

session = fastf1.get_session(2025, "Australia", "Q")
session.load()  # Need to have this line to load circuit info below
circuit_info = session.get_circuit_info()

session.load()
fast_leclerc = session.laps.pick_driver("LEC").pick_fastest()
lec_car_data = fast_leclerc.get_car_data().add_distance()
t_cl = lec_car_data["Distance"]
vCar_cl = lec_car_data["Speed"]
fast_ham = session.laps.pick_driver("HAM").pick_fastest()
ham_car_data = fast_ham.get_car_data().add_distance()
t_lh = ham_car_data["Distance"]
vCar_lh = ham_car_data["Speed"]

delta = vCar_lh - vCar_cl

# The rest is just plotting
fig, ax = plt.subplots()
ax.plot(t_cl, vCar_cl, label="LEC")
ax.plot(t_lh, vCar_lh, label="HAM")
# Draw vertical dotted lines at each corner that range from slightly below the
# minimum speed to slightly above the maximum speed.
v_min = lec_car_data["Speed"].min()
v_max = lec_car_data["Speed"].max()
ax.vlines(
    x=circuit_info.corners["Distance"],
    ymin=v_min - 20,
    ymax=v_max + 20,
    linestyles="dotted",
    colors="grey",
)

# Plot the corner number just below each vertical line.
# For corners that are very close together, the text may overlap. A more
# complicated approach would be necessary to reliably prevent this.
for _, corner in circuit_info.corners.iterrows():
    txt = f"{corner['Number']}{corner['Letter']}"
    ax.text(
        corner["Distance"],
        v_min - 30,
        txt,
        va="center_baseline",
        ha="center",
        size="small",
    )

ax.set_xlabel("Distance in m")
ax.set_ylabel("Speed in km/h")
ax.legend()

# Manually adjust the y-axis limits to include the corner numbers, because
# Matplotlib does not automatically account for text that was manually added.
ax.set_ylim([v_min - 40, v_max + 20])
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Speed [Km/h]")
ax.set_title("Ferrari")
ax.legend()
plt.show()


fig, ax = plt.subplots()
ax.plot(t_cl, delta, label="delta: HAM - LEC")
# Draw vertical dotted lines at each corner that range from slightly below the
# minimum speed to slightly above the maximum speed.
delta_min = delta.min()
delta_max = delta.max()
ax.vlines(
    x=circuit_info.corners["Distance"],
    ymin=delta_min - 20,
    ymax=delta_max + 20,
    linestyles="dotted",
    colors="grey",
)

# Plot the corner number just below each vertical line.
# For corners that are very close together, the text may overlap. A more
# complicated approach would be necessary to reliably prevent this.
for _, corner in circuit_info.corners.iterrows():
    txt = f"{corner['Number']}{corner['Letter']}"
    ax.text(
        corner["Distance"],
        delta_min - 30,
        txt,
        va="center_baseline",
        ha="center",
        size="small",
    )

ax.set_xlabel("Distance in m")
ax.set_ylabel("Speed in km/h")
ax.legend()

# Manually adjust the y-axis limits to include the corner numbers, because
# Matplotlib does not automatically account for text that was manually added.
ax.set_ylim([delta_min - 40, delta_max + 20])
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Delta Speed [km/hr]")
ax.legend()
plt.show()
