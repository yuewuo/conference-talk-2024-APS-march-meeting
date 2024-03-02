import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib
import numpy as np

# Font Size
matplotlib.rcParams['font.size'] = 12
matplotlib.rcParams['legend.fontsize'] = 'medium'
matplotlib.rcParams['figure.titlesize'] = 'medium'

# Font Type = Computer Modern Serif (LaTeX)
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.serif'] = 'cmr10'
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['axes.formatter.use_mathtext'] = True


def read_data(filename):
    ps = []
    pLs = []
    errs = []
    with open(filename, "r", encoding="utf8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip("\r\n ")
            if line == "" or line.startswith("#"):
                continue
            spt = line.split(" ")
            p = float(spt[0])
            pL = float(spt[5])
            err = float(spt[7])
            ps.append(p)
            pLs.append(pL)
            errs.append(err)
    return ps, pLs, errs


for has_hyperion in [False, True]:

    fig, ax = plt.subplots()

    def draw_line(filename, ls='go-', label='', alpha=1):
        ps, pLs, errs = read_data(filename)
        ax.loglog(ps, pLs, ls, linewidth=2,
                  markersize=5, label=label, alpha=alpha)

    colors = {3: "b", 5: "g", 7: "r", 9: "m"}

    for d in [3, 5, 7, 9]:
        draw_line(
            f"mwpm/d_{d}.txt", ls=f"{colors[d]}o--", alpha=1 if not has_hyperion else 0.2)

    if has_hyperion:
        for d in [3, 5, 7, 9]:
            draw_line(f"hyperion/d_{d}.txt", ls=f"{colors[d]}o-")

    plt.xlim(3e-5, 0.1)
    plt.ylim(3e-7, 1)
    plt.xlabel("physical error rate")
    plt.ylabel("logical error rate")

    legends = []
    labels = []
    for d in [3, 5, 7, 9]:
        legends.append(
            Line2D([0], [0], ls=f"None", c=colors[d], markersize=5, marker="o"))
        labels.append(f"d={d}")
    legends.append(Line2D([0], [0], ls=f"--", c="grey",
                   alpha=1 if not has_hyperion else 0.2))
    labels.append(f"MWPM")
    if has_hyperion:
        legends.append(Line2D([0], [0], ls=f"-", c="grey"))
        labels.append(f"MWPF")
    plt.legend(legends, labels)

    plt.savefig(
        f"rotated_planar_circuit_level_{1 if has_hyperion else 0}.png", dpi=600)
