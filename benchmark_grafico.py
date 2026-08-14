"""Gera gráficos a partir de benchmark_resultados.csv.

Produz:
  - benchmark_heatmap.png   : balanced_accuracy (método x dataset), com destaque
                              do melhor método por base e células de erro em cinza;
  - benchmark_melhor.png    : baseline vs. melhor método por base (barras).

Uso:
    python benchmark.py                 # gera o CSV
    python benchmark_grafico.py         # gera os PNGs a partir do CSV
"""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

CSV = Path("benchmark_resultados.csv")
if not CSV.exists():
    raise SystemExit("Rode 'python benchmark.py' primeiro para gerar benchmark_resultados.csv")

rows = list(csv.reader(CSV.open(encoding="utf-8")))
header = rows[0]
datasets = header[3:]
baseline = {}
data = {}          # metodo -> {dataset: valor|None}
tipos = {}
for r in rows[1:]:
    nome, tipo, status = r[0], r[1], r[2]
    vals = {}
    for d, cell in zip(datasets, r[3:]):
        vals[d] = None if cell == "ERRO" else float(cell)
    if nome == "__baseline__":
        baseline = vals
    else:
        data[nome] = vals
        tipos[nome] = tipo

metodos = list(data.keys())
# ordena por média (desc) para o heatmap ficar legível
def media(n):
    xs = [v for v in data[n].values() if v is not None]
    return np.mean(xs) if xs else -1
metodos.sort(key=media, reverse=True)

M = np.full((len(metodos), len(datasets)), np.nan)
for i, n in enumerate(metodos):
    for j, d in enumerate(datasets):
        v = data[n][d]
        if v is not None:
            M[i, j] = v

# ---------------------------------------------------------------- heatmap
paleta = LinearSegmentedColormap.from_list("acc", ["#f7fbff", "#6baed6", "#08306b"])
paleta.set_bad("#e6e6e6")  # células de erro (NaN)

fig, ax = plt.subplots(figsize=(1.6 + 1.5 * len(datasets), 0.34 * len(metodos) + 1.5))
im = ax.imshow(np.ma.masked_invalid(M), cmap=paleta, vmin=0.5, vmax=1.0, aspect="auto")

ax.set_xticks(range(len(datasets)))
ax.set_xticklabels(datasets, rotation=25, ha="right", fontsize=9)
ax.set_yticks(range(len(metodos)))
ax.set_yticklabels(metodos, fontsize=8)

# melhor método por base -> borda vermelha
for j, d in enumerate(datasets):
    col = [(i, data[metodos[i]][d]) for i in range(len(metodos)) if data[metodos[i]][d] is not None]
    if not col:
        continue
    best_i = max(col, key=lambda t: t[1])[0]
    ax.add_patch(plt.Rectangle((j - 0.5, best_i - 0.5), 1, 1, fill=False,
                               edgecolor="#d62728", lw=2.2))

# anotações
for i in range(len(metodos)):
    for j in range(len(datasets)):
        v = M[i, j]
        if np.isnan(v):
            ax.text(j, i, "×", ha="center", va="center", color="#999", fontsize=8)
        else:
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7,
                    color="white" if v > 0.8 else "#08306b")

cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
cbar.set_label("balanced accuracy", fontsize=9)
ax.set_title("itmofs-lab — desempenho por método e base\n"
             "(borda vermelha = melhor por base; × = não executou)", fontsize=11)
fig.tight_layout()
fig.savefig("benchmark_heatmap.png", dpi=150, bbox_inches="tight")
plt.close(fig)

# ---------------------------------------------------------------- barras baseline vs melhor
melhor_nome, melhor_val = {}, {}
for d in datasets:
    col = [(n, data[n][d]) for n in metodos if data[n][d] is not None]
    bn, bv = max(col, key=lambda t: t[1])
    melhor_nome[d], melhor_val[d] = bn, bv

x = np.arange(len(datasets))
w = 0.38
fig, ax = plt.subplots(figsize=(1.6 + 1.4 * len(datasets), 4.6))
b1 = ax.bar(x - w / 2, [baseline[d] for d in datasets], w, label="baseline (todas as features)",
            color="#b0b7bd")
b2 = ax.bar(x + w / 2, [melhor_val[d] for d in datasets], w, label="melhor FS (top-10)",
            color="#2b7bba")
ax.set_xticks(x)
ax.set_xticklabels(datasets, rotation=15, ha="right", fontsize=9)
ax.set_ylim(0, 1.08)
ax.set_ylabel("balanced accuracy")
ax.set_title("Baseline vs. melhor seleção de características por base", fontsize=12)
ax.legend(fontsize=9, loc="lower right")
for d, xi in zip(datasets, x):
    ax.text(xi + w / 2, melhor_val[d] + 0.015, melhor_nome[d], ha="center", fontsize=7,
            rotation=0, color="#2b7bba")
ax.bar_label(b1, fmt="%.2f", padding=2, fontsize=7)
fig.tight_layout()
fig.savefig("benchmark_melhor.png", dpi=150, bbox_inches="tight")
plt.close(fig)

print("Gerados: benchmark_heatmap.png, benchmark_melhor.png")
