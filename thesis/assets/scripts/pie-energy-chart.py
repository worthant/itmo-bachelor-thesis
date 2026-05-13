"""
plot_energy_pie.py
Pie-chart распределения энергии по этапам.
"""

import matplotlib.pyplot as plt

plt.rcParams.update(
    {
        "font.family": "Times New Roman",
        "font.size": 11,
    }
)

labels = [
    "Инициализация\n(20,9%)",
    "Захват аудио\n(24,1%)",
    "MFCC\n(6,7%)",
    "Инференс\n(15,0%)",
    "Индикация\n(27,6%)",
    "Завершение\n(5,0%)",
    "Глубокий сон\n(0,7%)",
]
sizes = [20.9, 24.1, 6.7, 15.0, 27.6, 5.0, 0.7]
colors = ["#fde2e4", "#fff1c1", "#c7e9c0", "#9ecae1", "#fdae6b", "#d9d9d9", "#e8f4f8"]

fig, ax = plt.subplots(figsize=(7, 6))
wedges, texts = ax.pie(
    sizes,
    labels=labels,
    colors=colors,
    startangle=90,
    wedgeprops=dict(edgecolor="black", linewidth=0.8),
    textprops={"fontsize": 10},
)
ax.set_title("Распределение энергии цикла каскадной обработки по этапам")
plt.tight_layout()
plt.savefig("energy_pie.pdf", dpi=300)
plt.savefig("energy_pie.png", dpi=200)
