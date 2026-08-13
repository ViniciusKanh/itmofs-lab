"""Interface de linha de comando do itmofs-lab.

Comandos:
    itmofs-lab list [--family filters.univariate] [--status OK]
    itmofs-lab families
    itmofs-lab info <metodo>          # o que entra e o que sai
    itmofs-lab run <metodo> --dataset breast_cancer [-k 10] [--n-features 10]
    itmofs-lab version
"""

from __future__ import annotations

import argparse
import sys
import warnings

warnings.filterwarnings("ignore")

from . import (list_methods, families, info, get, itmo_version, __version__)
from .core.registry import spec


def _cmd_list(args):
    names = list_methods(family=args.family, status=args.status)
    for n in names:
        s = spec(n)
        print(f"{n:26s} {s.status:18s} {s.family:26s} {s.summary}")
    print(f"\n{len(names)} método(s).")


def _cmd_families(args):
    for fam, ms in families().items():
        print(f"{fam}  ({len(ms)})")
        for m in ms:
            print(f"    - {m}")


def _cmd_info(args):
    try:
        print(info(args.method))
    except KeyError as e:
        print(e, file=sys.stderr)
        sys.exit(2)


def _load_dataset(name):
    from sklearn.datasets import load_breast_cancer, load_wine, make_classification
    if name == "breast_cancer":
        d = load_breast_cancer(); return d.data, d.target, list(d.feature_names)
    if name == "wine":
        d = load_wine(); return d.data, d.target, list(d.feature_names)
    if name == "synthetic":
        X, y = make_classification(n_samples=400, n_features=25, n_informative=8,
                                   n_redundant=5, random_state=42)
        return X, y, [f"f{i:02d}" for i in range(X.shape[1])]
    raise SystemExit(f"dataset desconhecido: {name} (use breast_cancer|wine|synthetic)")


def _cmd_run(args):
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, MinMaxScaler, KBinsDiscretizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import balanced_accuracy_score

    X, y, names = _load_dataset(args.dataset)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

    s = spec(args.method)
    # aplica pré-processamento recomendado (ajustado SÓ no treino)
    rep = s.recommends_scaling
    if s.requires_nonnegative or rep == "minmax":
        sc = MinMaxScaler().fit(Xtr); Xtr, Xte = sc.transform(Xtr), sc.transform(Xte)
    elif s.requires_discrete or rep == "discretize":
        dc = KBinsDiscretizer(n_bins=5, encode="ordinal", strategy="uniform").fit(Xtr)
        Xtr = dc.transform(Xtr).astype(int); Xte = dc.transform(Xte).astype(int)
    elif rep == "standard":
        sc = StandardScaler().fit(Xtr); Xtr, Xte = sc.transform(Xtr), sc.transform(Xte)

    over = {}
    if args.k is not None:
        over["k"] = args.k
    if args.n_features is not None:
        over["n_features"] = args.n_features
    try:
        m = get(args.method, **over)
        m.fit(Xtr, ytr, feature_names=names)
    except Exception as e:
        print(f"[{args.method}] não executável: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)

    Xtr_s, Xte_s = m.transform(Xtr), m.transform(Xte)
    clf = LogisticRegression(max_iter=1000).fit(Xtr_s, ytr)
    bacc = balanced_accuracy_score(yte, clf.predict(Xte_s))
    base = LogisticRegression(max_iter=1000).fit(Xtr, ytr)
    bacc0 = balanced_accuracy_score(yte, base.predict(Xte))

    print(f"Método: {args.method}  ({s.family})")
    print(f"Dataset: {args.dataset}  |  {Xtr.shape[1]} -> {len(m.selected_)} features")
    print(f"Selecionadas: {m.selected_names_}")
    if m.scores_ is not None:
        import numpy as np
        top = np.argsort(np.nan_to_num(m.scores_, nan=-np.inf))[::-1][:5]
        print("Top-5 por score:", [names[i] for i in top])
    print(f"Balanced accuracy: baseline={bacc0:.4f}  com FS={bacc:.4f}")


def build_parser():
    p = argparse.ArgumentParser(
        prog="itmofs-lab",
        description="Wrapper simples e uniforme sobre a ITMO_FS (filtros, ensembles, wrappers).")
    sub = p.add_subparsers(dest="cmd")

    pl = sub.add_parser("list", help="lista métodos")
    pl.add_argument("--family", default=None, help="filtra por família (prefixo)")
    pl.add_argument("--status", default=None, help="filtra por status (ex.: OK)")
    pl.set_defaults(func=_cmd_list)

    pf = sub.add_parser("families", help="lista famílias e seus métodos")
    pf.set_defaults(func=_cmd_families)

    pi = sub.add_parser("info", help="o que entra e o que sai de um método")
    pi.add_argument("method")
    pi.set_defaults(func=_cmd_info)

    pr = sub.add_parser("run", help="executa um método num dataset didático")
    pr.add_argument("method")
    pr.add_argument("--dataset", default="breast_cancer",
                    help="breast_cancer|wine|synthetic")
    pr.add_argument("-k", type=int, default=None, help="nº de features (cutting rule)")
    pr.add_argument("--n-features", type=int, default=None, dest="n_features")
    pr.set_defaults(func=_cmd_run)

    pv = sub.add_parser("version", help="versões")
    pv.set_defaults(func=lambda a: print(f"itmofs-lab {__version__} | ITMO_FS {itmo_version()}"))
    return p


def main(argv=None):
    p = build_parser()
    args = p.parse_args(argv)
    if not getattr(args, "func", None):
        p.print_help(); return
    args.func(args)


if __name__ == "__main__":
    main()
