from numpy import *
from matplotlib.pyplot import *
import CoolProp.CoolProp as cp

matplotlib.use("Qt5Agg")

sp_vol = logspace(-3, 1, 100)
density = 1 / sp_vol

T = linspace(-240, -110, 12)
leg = []
for t in T:
    T1 = t + 273.15
    p1 = cp.PropsSI("P", "D", density, "T", T1, "nitrogen")
    print(T1)
    loglog(sp_vol, p1)
    leg.append(f"T = {T1}")

xlabel("Specific Volume [m^3/kg]")
ylabel("Pressure [MPa]")
# axis([0.001, 3, 0.01, 100])
legend(leg, loc="upper right")
show()
