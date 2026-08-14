"""Estabilidade de seleção dos métodos do itmofs-lab.

Mede o quanto cada seletor escolhe as MESMAS features quando o treino é
reamostrado — critério central para escolher bases de um ensemble (EFS).
Usa SOMENTE o treino (o teste nunca entra); em cada repetição faz uma
subamostragem do treino, reajusta o pré-processamento e o seletor, e coleta
o conjunto selecionado.

Métricas (média sobre todos os pares de repetições):
  - Jaccard médio:  |A∩B| / |A∪B|   (0 = nada em comum, 1 = idêntico)
  - Índice de Kuncheva: corrige a concordância esperada ao acaso
        (r - k²/p) / (k - k²/p),  r = |A∩B|, k = nº de features, p = total
        (~0 = aleatório, 1 = perfeitamente estável)

Saídas: estabilidade.csv e estabilidade.png

Uso:
    python estabilidade.py [--dataset breast_cancer] [--repeats 20] [--completo]
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

import itmofs_lab as fs  # noqa: E402
import benchmark as bench  # reaproveita carregar/preprocessa/metodos/kwargs  # noqa: E402


def kuncheva(assinaturas, p):
    """Índice de estabilidade de Kuncheva (média sobre pares)."""
    pares = list(itertools.combinations(range(len(assinaturas)), 2))
    vals = []
    for i, j in pares:
        A, B = assinaturas[i], assinaturas[j]
        k = (len(A) + len(B)) / 2.0
        if k == 0:
            continue
        r = len(A & B)
        denom = k - (k * k) / p
        if abs(denom) < 1e-12:
            continue
        vals.append((r - (k * k) / p) / denom)
    return float(np.mean(vals)) if vals else float("nan")


def jaccard_medio(assinaturas):
    pares = list(itertools.combinations(range(len(assinaturas)), 2))
    vals = []
    for i, j in pares:
        A, B = assinaturas[i], assinaturas[j]
        u = len(A | B)
        vals.append(len(A & B) / u if u else 1.0)
    return float(np.mean(vals)) if vals else float("nan")


def medir(dataset, repeats, completo, k=None):
    X, y = bench.carregar(dataset)
    X, y = np.asarray(X, float), np.asarray(y)
    p = X.shape[1]
    kval = min(k or bench.K, p - 1)
    metodos = bench.metodos_executaveis(rapido=not completo, completo=completo)

    rng = np.random.RandomState(42)
    # separa um treino fixo; a estabilidade reamostra DENTRO do treino
    n = X.shape[0]
    idx_all = np.arange(n)
    tr_idx, _ = _split(idx_all, y, test_size=0.3, seed=42)
    Xtr_full, ytr_full = X[tr_idx], y[tr_idx]
    n_tr = len(tr_idx)

    print(f"itmofs-lab {fs.__version__} | dataset={dataset} | p={p} | "
          f"treino={n_tr} | repetições={repeats} | k={kval}")
    print(f"{len(metodos)} métodos\n")
    print(f"{'método':22s} {'Kuncheva':>9s} {'Jaccard':>8s} {'n_sel':>6s}")
    print("-" * 50)

    resultados = []
    for nome in metodos:
        s = fs.spec(nome)
        assinaturas = []
        for r in range(repeats):
            sub = rng.choice(n_tr, size=int(0.9 * n_tr), replace=False)  # subamostra 90%
            Xs, ys = Xtr_full[sub], ytr_full[sub]
            try:
                Xa, _, _ = bench.preprocessa(s, Xs, Xs)  # ajusta só na subamostra
                m = fs.get(nome, **bench.kwargs_de(nome, kval)).fit(Xa, ys)
                assinaturas.append(set(int(i) for i in m.selected_))
            except Exception:
                pass
        if len(assinaturas) < 2:
            print(f"{nome:22s} {'ERRO':>9s}")
            continue
        ku = kuncheva(assinaturas, p)
        ja = jaccard_medio(assinaturas)
        nsel = float(np.mean([len(a) for a in assinaturas]))
        resultados.append((nome, ku, ja, nsel, s.component_type))
        print(f"{nome:22s} {ku:9.3f} {ja:8.3f} {nsel:6.1f}")

    resultados.sort(key=lambda t: (-t[1] if not np.isnan(t[1]) else 1))
    return resultados, dataset, kval


def _split(idx, y, test_size, seed):
    from sklearn.model_selection import train_test_split
    return train_test_split(idx, test_size=test_size, stratify=y, random_state=seed)


def salvar(resultados, dataset, kval=10):
    with open("estabilidade.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["metodo", "tipo", "kuncheva", "jaccard_medio", "n_selecionadas"])
        for nome, ku, ja, ns, tipo in resultados:
            w.writerow([nome, tipo, f"{ku:.4f}", f"{ja:.4f}", f"{ns:.2f}"])

    nomes = [r[0] for r in resultados]
    kus = [r[1] for r in resultados]
    cores = ["#2b7bba" if k >= 0.75 else "#6baed6" if k >= 0.5 else "#f0a35e"
             for k in kus]
    fig, ax = plt.subplots(figsize=(8, 0.32 * len(nomes) + 1.2))
    ax.barh(range(len(nomes)), kus, color=cores)
    ax.set_yticks(range(len(nomes)))
    ax.set_yticklabels(nomes, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlim(0, 1)
    ax.axvline(0.75, color="#888", ls="--", lw=1)
    ax.set_xlabel("índice de estabilidade de Kuncheva  (1 = muito estável)")
    ax.set_title(f"Estabilidade de seleção — {dataset}\n"
                 f"(reamostragem 90% do treino; k={kval}; linha = 0.75)", fontsize=11)
    for i, k in enumerate(kus):
        ax.text(k + 0.01, i, f"{k:.2f}", va="center", fontsize=7)
    fig.tight_layout()
    fig.savefig("estabilidade.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("\nArquivos: estabilidade.csv, estabilidade.png")


def main():
    ap = argparse.ArgumentParser(description="Estabilidade de seleção (EFS).")
    ap.add_argument("--dataset", default="breast_cancer")
    ap.add_argument("--repeats", type=int, default=20)
    ap.add_argument("--k", type=int, default=None, help="nº de features (default 10)")
    ap.add_argument("--completo", action="store_true", help="inclui esparsos/wrappers (lento)")
    args = ap.parse_args()
    resultados, ds, kval = medir(args.dataset, args.repeats, args.completo, k=args.k)
    salvar(resultados, ds, kval)


if __name__ == "__main__":
    main()
