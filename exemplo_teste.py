"""Teste rápido do itmofs-lab: roda vários métodos e mostra um resumo.

Uso:
    python exemplo_teste.py

Observação de ambiente: a ITMO_FS 0.3.3 é de ~2021. Em numpy>=2 / sklearn>=1.4
alguns métodos podem dar erro de runtime — o script trata isso por método e
segue em frente. Para rodar todos sem erro, use:
    pip install "numpy<2" "pandas<2" "scikit-learn<1.4" itmofs-lab
"""

import warnings
warnings.filterwarnings("ignore")

import itmofs_lab as fs
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, KBinsDiscretizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score

print("=" * 60)
print(f" itmofs-lab {fs.__version__}  |  ITMO_FS {fs.itmo_version()}")
print(f" métodos catalogados: {len(fs.list_methods())}")
print("=" * 60)

# 1) dados + split (o teste NUNCA entra no fit)
X, y = load_breast_cancer(return_X_y=True)
names = list(load_breast_cancer().feature_names)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

# representações ajustadas só no treino
scaled_tr = StandardScaler().fit(X_tr)
Xtr_s, Xte_s = scaled_tr.transform(X_tr), scaled_tr.transform(X_te)
mm = MinMaxScaler().fit(X_tr)
Xtr_nn, Xte_nn = mm.transform(X_tr), mm.transform(X_te)
disc = KBinsDiscretizer(n_bins=5, encode="ordinal", strategy="uniform").fit(X_tr)
Xtr_d, Xte_d = disc.transform(X_tr).astype(int), disc.transform(X_te).astype(int)

# baseline (todas as features)
base = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
bacc0 = balanced_accuracy_score(y_te, base.predict(X_te))
print(f"\nBaseline (30 features): balanced_accuracy = {bacc0:.4f}\n")

# 2) métodos a testar: (nome, kwargs, treino, teste)
casos = [
    ("gini_index",         dict(k=10), X_tr, X_te),
    ("f_ratio_measure",    dict(k=10), X_tr, X_te),
    ("chi2_measure",       dict(k=10), Xtr_nn, Xte_nn),     # exige X>=0
    ("information_gain",   dict(k=10), Xtr_d, Xte_d),       # discretizado
    ("reliefF_measure",    dict(k=10), Xtr_s, Xte_s),
    ("MRMR",               dict(n_features=10), Xtr_d, Xte_d),
    ("CMIM",               dict(n_features=10), Xtr_d, Xte_d),
    ("MCFS",               dict(n_features=10), Xtr_s, Xte_s),
    ("WeightBased",        dict(k=10), X_tr, X_te),
    ("Mixed",              dict(k=10), X_tr, X_te),
    ("BestSum",            dict(k=10), Xtr_s, Xte_s),
]

print(f"{'método':20s} {'status':10s} {'n_sel':>5s}  {'bal_acc (FS)':>12s}")
print("-" * 55)
ok = fail = 0
for nome, kw, Xa, Xb in casos:
    try:
        m = fs.get(nome, **kw).fit(Xa, y_tr, feature_names=names)
        Xa_s, Xb_s = m.transform(Xa), m.transform(Xb)
        clf = LogisticRegression(max_iter=1000).fit(Xa_s, y_tr)
        bacc = balanced_accuracy_score(y_te, clf.predict(Xb_s))
        print(f"{nome:20s} {'OK':10s} {len(m.selected_):5d}  {bacc:12.4f}")
        ok += 1
    except fs.NotSupportedError as e:
        print(f"{nome:20s} {'INDISPON.':10s}     -  ({str(e).splitlines()[0][:30]})")
        fail += 1
    except Exception as e:
        print(f"{nome:20s} {'ERRO':10s}     -  {type(e).__name__}: {str(e)[:30]}")
        fail += 1

print("-" * 55)
print(f"\nResumo: {ok} OK, {fail} com erro/indisponível.")
print("Ajuda de qualquer método:  itmofs-lab info <nome>   ou   fs.info('<nome>')")
