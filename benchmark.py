"""Benchmark do itmofs-lab: roda VÁRIOS métodos em VÁRIAS bases.

Para cada (dataset, método):
  - separa treino/teste (o teste NUNCA entra no fit);
  - aplica o pré-processamento recomendado pela spec do método (só no treino);
  - ajusta o seletor no treino, transforma treino e teste;
  - treina um LogisticRegression e mede balanced_accuracy no teste;
  - compara com o baseline (todas as features).

Gera:
  - uma tabela por dataset no terminal;
  - `benchmark_resultados.csv` (método x dataset = balanced_accuracy com FS);
  - `benchmark_resumo.csv` (melhor método por dataset).

Uso:
    python benchmark.py                      # todos os métodos executáveis, bases padrão
    python benchmark.py --datasets breast_cancer wine
    python benchmark.py --rapido             # pula métodos esparsos (mais lentos)

Observação: em numpy>=2 / scikit-learn>=1.4 alguns métodos da ITMO_FS 0.3.3 dão
erro de runtime (o script marca como ERRO e continua). Para cobertura total:
    pip install "numpy<2" "pandas<2" "scikit-learn<1.4" itmofs-lab
"""

from __future__ import annotations

import argparse
import csv
import time
import warnings
from collections import defaultdict

warnings.filterwarnings("ignore")

import numpy as np
from sklearn.datasets import (load_breast_cancer, load_wine, load_iris,
                              load_digits, make_classification)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, KBinsDiscretizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score

import itmofs_lab as fs

K = 10  # nº de features a selecionar


# ----------------------------------------------------------------- datasets
def carregar(nome):
    if nome == "breast_cancer":
        d = load_breast_cancer()
    elif nome == "wine":
        d = load_wine()
    elif nome == "iris":
        d = load_iris()
    elif nome == "digits":
        d = load_digits()
    elif nome == "sintetico_bal":
        X, y = make_classification(n_samples=600, n_features=30, n_informative=8,
                                   n_redundant=6, weights=[0.5, 0.5], random_state=42)
        return X, y
    elif nome == "sintetico_desbal":
        X, y = make_classification(n_samples=600, n_features=30, n_informative=8,
                                   n_redundant=6, weights=[0.9, 0.1], random_state=42)
        return X, y
    else:
        raise SystemExit(f"dataset desconhecido: {nome}")
    return d.data, d.target


DATASETS_PADRAO = ["breast_cancer", "wine", "iris", "digits",
                   "sintetico_bal", "sintetico_desbal"]


# ------------------------------------------------------- pré-processamento
def preprocessa(spec, Xtr, Xte):
    """Ajusta a representação recomendada pela spec SOMENTE no treino."""
    if spec.requires_nonnegative or spec.recommends_scaling == "minmax":
        sc = MinMaxScaler().fit(Xtr)
        return sc.transform(Xtr), sc.transform(Xte), "nonneg"
    if spec.requires_discrete or spec.recommends_scaling == "discretize":
        dc = KBinsDiscretizer(n_bins=5, encode="ordinal", strategy="uniform").fit(Xtr)
        return dc.transform(Xtr).astype(int), dc.transform(Xte).astype(int), "discretizado"
    if spec.recommends_scaling == "standard":
        sc = StandardScaler().fit(Xtr)
        return sc.transform(Xtr), sc.transform(Xte), "escalado"
    return Xtr, Xte, "raw"


# ------------------------------------------------------- métodos a testar
def metodos_executaveis(rapido=False, completo=False):
    """Nomes de métodos executáveis.

    Padrão: filtros (univariados/multivariados), esparsos e ensembles.
    Wrappers e embedded (busca guiada por classificador — LENTOS, ex.: MOS ~80s)
    só entram com --completo. --rapido também remove os esparsos.
    """
    out = []
    for nome in fs.list_methods():
        s = fs.spec(nome)
        if s.status not in ("OK", "OK_WITH_ADAPTER"):
            continue
        if s.component_type == "support_metric":
            continue
        if not completo and s.family in ("wrappers", "embedded"):
            continue
        if rapido and s.family in ("filters.sparse", "filters.unsupervised"):
            continue
        out.append(nome)
    return out


def kwargs_de(nome, kval):
    s = fs.spec(nome)
    if "k" in s.params:
        return {"k": kval}
    if "n_features" in s.params:
        return {"n_features": kval}
    return {}


# ----------------------------------------------------------------- execução
def rodar(datasets, rapido=False, completo=False):
    metodos = metodos_executaveis(rapido, completo)
    print("=" * 68)
    print(f" itmofs-lab {fs.__version__} | ITMO_FS {fs.itmo_version()}")
    print(f" {len(metodos)} métodos executáveis x {len(datasets)} datasets  (k={K})")
    print("=" * 68)

    # resultados[metodo][dataset] = bal_acc (ou None)
    resultados = defaultdict(dict)
    baselines = {}
    n_features_ds = {}

    for ds in datasets:
        X, y = carregar(ds)
        X, y = np.asarray(X, float), np.asarray(y)
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
        n_features_ds[ds] = X.shape[1]
        kval = min(K, X.shape[1] - 1)   # não pedir mais features do que existem
        base = LogisticRegression(max_iter=1000).fit(Xtr, ytr)
        b0 = balanced_accuracy_score(yte, base.predict(Xte))
        baselines[ds] = b0

        print(f"\n### {ds}  ({X.shape[0]} amostras, {X.shape[1]} features) "
              f"| baseline bal_acc = {b0:.4f}")
        print(f"{'método':22s} {'repr':12s} {'n':>3s} {'bal_acc':>8s} {'Δ':>7s}  {'t(s)':>6s}")
        print("-" * 62)
        for nome in metodos:
            s = fs.spec(nome)
            try:
                Xa, Xb, rep = preprocessa(s, Xtr, Xte)
                t0 = time.perf_counter()
                m = fs.get(nome, **kwargs_de(nome, kval)).fit(Xa, ytr)
                Xa_s, Xb_s = m.transform(Xa), m.transform(Xb)
                clf = LogisticRegression(max_iter=1000).fit(Xa_s, ytr)
                bacc = balanced_accuracy_score(yte, clf.predict(Xb_s))
                dt = time.perf_counter() - t0
                resultados[nome][ds] = bacc
                print(f"{nome:22s} {rep:12s} {len(m.selected_):3d} "
                      f"{bacc:8.4f} {bacc-b0:+7.4f}  {dt:6.2f}")
            except Exception as e:
                resultados[nome][ds] = None
                print(f"{nome:22s} {'-':12s}   -  {'ERRO':>8s}  ({type(e).__name__})")

    # --------- CSV wide (método x dataset) ---------
    with open("benchmark_resultados.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["metodo", "tipo", "status"] + datasets)
        w.writerow(["__baseline__", "-", "-"] + [f"{baselines[d]:.4f}" for d in datasets])
        for nome in metodos:
            s = fs.spec(nome)
            linha = [nome, s.component_type, s.status]
            for d in datasets:
                v = resultados[nome].get(d)
                linha.append(f"{v:.4f}" if v is not None else "ERRO")
            w.writerow(linha)

    # --------- resumo: melhor método por dataset ---------
    print("\n" + "=" * 68)
    print(" RESUMO — melhor método por dataset (vs baseline)")
    print("=" * 68)
    with open("benchmark_resumo.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["dataset", "n_features", "baseline", "melhor_metodo", "melhor_bal_acc", "ganho"])
        for ds in datasets:
            validos = [(n, resultados[n][ds]) for n in metodos if resultados[n].get(ds) is not None]
            if not validos:
                continue
            best_n, best_v = max(validos, key=lambda x: x[1])
            print(f"  {ds:18s} baseline={baselines[ds]:.4f}  ->  {best_n} = {best_v:.4f} "
                  f"({best_v-baselines[ds]:+.4f})")
            w.writerow([ds, n_features_ds[ds], f"{baselines[ds]:.4f}",
                        best_n, f"{best_v:.4f}", f"{best_v-baselines[ds]:+.4f}"])

    # --------- contagem de erros ---------
    total = len(metodos) * len(datasets)
    erros = sum(1 for n in metodos for d in datasets if resultados[n].get(d) is None)
    print(f"\nExecuções: {total-erros} OK, {erros} com erro (de {total}).")
    print("Arquivos: benchmark_resultados.csv, benchmark_resumo.csv")


def main():
    ap = argparse.ArgumentParser(description="Benchmark do itmofs-lab (vários métodos x várias bases).")
    ap.add_argument("--datasets", nargs="*", default=DATASETS_PADRAO)
    ap.add_argument("--rapido", action="store_true", help="pula métodos esparsos (mais lentos)")
    ap.add_argument("--completo", action="store_true",
                    help="inclui wrappers e embedded (LENTOS: MOS ~80s, wrappers ~5s cada)")
    args = ap.parse_args()
    rodar(args.datasets, rapido=args.rapido, completo=args.completo)


if __name__ == "__main__":
    main()
