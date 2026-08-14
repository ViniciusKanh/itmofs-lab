"""Diversidade entre seletores do itmofs-lab.

Para escolher as bases de um ensemble (EFS), queremos seletores COMPLEMENTARES:
que acertem features diferentes, não os mesmos. Este script ajusta cada método
UMA vez no treino (o teste nunca entra), pega o conjunto de features escolhido, e
mede a concordância (Jaccard) entre CADA PAR de métodos.

  - Jaccard alto  -> métodos redundantes (escolhem quase as mesmas features)
  - Jaccard baixo -> métodos diversos    -> bons candidatos a formar par no ensemble

Saídas: diversidade.csv (matriz), diversidade.png (heatmap) e
        diversidade_pares.csv (pares mais diversos e mais redundantes).

Uso:
    python diversidade.py [--dataset breast_cancer] [--completo]
"""

from __future__ import annotations

import argparse
import csv
import itertools
import warnings

warnings.filterwarnings("ignore")

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

import itmofs_lab as fs  # noqa: E402
import benchmark as bench  # noqa: E402


def coletar(dataset, completo):
    from sklearn.model_selection import train_test_split
    X, y = bench.carregar(dataset)
    X, y = np.asarray(X, float), np.asarray(y)
    p = X.shape[1]
    kval = min(bench.K, p - 1)
    Xtr, _, ytr, _ = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

    metodos = bench.metodos_executaveis(rapido=not completo, completo=completo)
    selecoes = {}
    for nome in metodos:
        s = fs.spec(nome)
        try:
            Xa, _, _ = bench.preprocessa(s, Xtr, Xtr)
            m = fs.get(nome, **bench.kwargs_de(nome, kval)).fit(Xa, ytr)
            selecoes[nome] = set(int(i) for i in m.selected_)
        except Exception:
            pass
    return selecoes, kval, p


def jaccard(A, B):
    u = len(A | B)
    return len(A & B) / u if u else 1.0


def main():
    ap = argparse.ArgumentParser(description="Diversidade entre seletores (EFS).")
    ap.add_argument("--dataset", default="breast_cancer")
    ap.add_argument("--completo", action="store_true")
    args = ap.parse_args()

    selecoes, kval, p = coletar(args.dataset, args.completo)
    nomes = sorted(selecoes)
    n = len(nomes)
    print(f"itmofs-lab {fs.__version__} | dataset={args.dataset} | "
          f"{n} métodos | k={kval} | p={p}")

    # matriz de Jaccard
    M = np.zeros((n, n))
    for i, j in itertools.product(range(n), range(n)):
        M[i, j] = jaccard(selecoes[nomes[i]], selecoes[nomes[j]])

    # CSV da matriz
    with open("diversidade.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["metodo"] + nomes)
        for i, nome in enumerate(nomes):
            w.writerow([nome] + [f"{M[i, j]:.3f}" for j in range(n)])

    # pares mais diversos e mais redundantes
    pares = []
    for i, j in itertools.combinations(range(n), 2):
        pares.append((nomes[i], nomes[j], M[i, j]))
    pares.sort(key=lambda t: t[2])
    with open("diversidade_pares.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["metodo_a", "metodo_b", "jaccard", "grupo"])
        for a, b, v in pares[:15]:
            w.writerow([a, b, f"{v:.3f}", "mais_diversos"])
        for a, b, v in pares[-15:][::-1]:
            w.writerow([a, b, f"{v:.3f}", "mais_redundantes"])

    print("\nPares MAIS DIVERSOS (bons para o ensemble):")
    for a, b, v in pares[:8]:
        print(f"  {a} + {b}   Jaccard={v:.2f}")
    print("\nPares MAIS REDUNDANTES (evitar juntos):")
    for a, b, v in pares[-6:][::-1]:
        print(f"  {a} + {b}   Jaccard={v:.2f}")

    # heatmap
    pal = LinearSegmentedColormap.from_list("jac", ["#2ca25f", "#ffffcc", "#d62728"])
    fig, ax = plt.subplots(figsize=(0.34 * n + 2, 0.34 * n + 2))
    im = ax.imshow(M, cmap=pal, vmin=0, vmax=1)
    ax.set_xticks(range(n)); ax.set_xticklabels(nomes, rotation=90, fontsize=6)
    ax.set_yticks(range(n)); ax.set_yticklabels(nomes, fontsize=6)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Jaccard (verde = diverso, vermelho = redundante)", fontsize=8)
    ax.set_title(f"Diversidade entre seletores — {args.dataset}\n"
                 "(concordância das features escolhidas; k=10)", fontsize=10)
    fig.tight_layout()
    fig.savefig("diversidade.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("\nArquivos: diversidade.csv, diversidade_pares.csv, diversidade.png")


if __name__ == "__main__":
    main()
