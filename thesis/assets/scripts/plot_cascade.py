"""
plot_cascade_annotated.py
Строит график тока с цветными полосами по состояниям FSM.
Сохраняет в cascade_annotated.pdf
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("synced_cascade_log.csv", names=["t_ms", "v", "i_ma", "state"])
df["t_s"] = df["t_ms"] / 1000.0

state_colors = {
    "SLEEP":     "#e8f4f8",
    "HW_BOOT":   "#fde2e4",
    "RECORD":    "#fff1c1",
    "MFCC":      "#c7e9c0",
    "INFERENCE": "#9ecae1",
    "RESULT":    "#fdae6b",
    "SHUTDOWN":  "#d9d9d9",
}

plt.rcParams.update({
    "font.family": "Times New Roman",
    "font.size": 11,
    "axes.linewidth": 0.8,
})

fig, ax = plt.subplots(figsize=(10, 4))

# подкрашиваем участки по состояниям
prev_state = df["state"].iloc[0]
start_t = df["t_s"].iloc[0]
for i in range(1, len(df)):
    if df["state"].iloc[i] != prev_state:
        ax.axvspan(start_t, df["t_s"].iloc[i],
                   color=state_colors.get(prev_state, "white"), alpha=0.5)
        start_t = df["t_s"].iloc[i]
        prev_state = df["state"].iloc[i]
ax.axvspan(start_t, df["t_s"].iloc[-1],
           color=state_colors.get(prev_state, "white"), alpha=0.5)

ax.plot(df["t_s"], df["i_ma"], color="black", linewidth=0.8)
ax.set_xlabel("Время, с")
ax.set_ylabel("Ток, мА")
ax.set_title("Профиль тока полного цикла каскадной обработки")
ax.grid(alpha=0.3)

# легенда состояний
from matplotlib.patches import Patch
handles = [Patch(color=c, alpha=0.5, label=s) for s, c in state_colors.items()]
ax.legend(handles=handles, loc="upper right", ncol=4, fontsize=9)

plt.tight_layout()
plt.savefig("cascade_annotated.pdf", dpi=300)
plt.savefig("cascade_annotated.png", dpi=200)
