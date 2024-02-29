import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib
import numpy as np
from scipy.stats import binom

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


def logical_error_rate(n, p):
    start = (n + 1) // 2
    prob = sum(binom.pmf(k, n, p) for k in range(start, n + 1))
    return prob


for (has_hyperion, draw_std) in [(False, False), (True, False), (True, True)]:

    fig, ax = plt.subplots()

    def draw_line(filename, ls='go-', label='', alpha=1):
        ps, pLs, errs = read_data(filename)
        ax.loglog(ps, pLs, ls, linewidth=2,
                  markersize=5, label=label, alpha=alpha)

    colors = {3: "b", 5: "g", 7: "r", 9: "m"}

    for d in [3, 5, 7, 9]:
        draw_line(
            f"tailored-mwpm/d_{d}.txt", ls=f"{colors[d]}o--", alpha=1 if not has_hyperion else 0.2)

    if draw_std:
        for d in [3, 5, 7, 9]:
            ps = np.logspace(np.log(0.09), np.log(
                0.5), num=20, base=np.e, endpoint=True)
            pLs = [logical_error_rate(d * d, p) for p in ps]
            ax.loglog(ps, pLs, f'{colors[d]}:', linewidth=2, alpha=0.5)

    if has_hyperion:
        for d in [3, 5, 7, 9]:
            draw_line(f"hyperion/d_{d}.txt", ls=f"{colors[d]}o-")

    plt.xlim(0.09, 0.55)
    plt.ylim(3e-7, 1)
    plt.xlabel("physical error rate")
    plt.ylabel("logical error rate")

    legends = []
    labels = []
    if draw_std:
        legends.append(Line2D([0], [0], ls=f":", c="black"))
        labels.append(f"optimal")
    if has_hyperion:
        legends.append(Line2D([0], [0], ls=f"-", c="black"))
        labels.append(f"MWPF")
    legends.append(Line2D([0], [0], ls=f"--", c="black",
                   alpha=1 if not has_hyperion else 0.2))
    labels.append(r"MWPM$^\text{[1]}$")
    for d in [3, 5, 7, 9]:
        legends.append(
            Line2D([0], [0], ls=f"-", c=colors[d], markersize=5, marker="o"))
        labels.append(f"d={d}")
    plt.legend(legends, labels)
    plt.xticks([])
    plt.xticks([])
    ax.set_xticks([0.1, 0.2, 0.3, 0.4, 0.5], [
                  "0.1", "0.2", "0.3", "0.4", "0.5"], minor=True)

    plt.savefig(
        f"tailored_xy_inf_bias_code_capacity_{(2 if draw_std else 1) if has_hyperion else 0}.png", dpi=600)
