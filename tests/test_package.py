"""Testes do itmofs-lab."""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pytest
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

import itmofs_lab as fs


@pytest.fixture(scope="module")
def data():
    d = load_breast_cancer()
    Xtr, Xte, ytr, yte = train_test_split(d.data, d.target, test_size=0.3,
                                          stratify=d.target, random_state=42)
    return Xtr, Xte, ytr, yte, list(d.feature_names)


def test_catalog_nonempty():
    assert len(fs.list_methods()) >= 45
    assert "gini_index" in fs.list_methods()


def test_info_all_methods():
    for name in fs.list_methods():
        txt = fs.info(name)
        assert "ENTRA" in txt and "SAI" in txt


def test_families_cover_all():
    fams = fs.families()
    assert "filters.univariate" in fams
    assert "ensembles.measure_based" in fams
    assert "wrappers" in fams


@pytest.mark.parametrize("name,pre", [
    ("gini_index", "raw"), ("f_ratio_measure", "raw"), ("MRMR", "disc"),
    ("chi2_measure", "minmax"), ("WeightBased", "raw"), ("Mixed", "raw"),
])
def test_working_methods_fit_transform(data, name, pre):
    Xtr, Xte, ytr, yte, names = data
    if pre == "disc":
        from sklearn.preprocessing import KBinsDiscretizer
        d = KBinsDiscretizer(n_bins=5, encode="ordinal", strategy="uniform").fit(Xtr)
        Xtr = d.transform(Xtr).astype(int); Xte = d.transform(Xte).astype(int)
    elif pre == "minmax":
        from sklearn.preprocessing import MinMaxScaler
        s = MinMaxScaler().fit(Xtr); Xtr, Xte = s.transform(Xtr), s.transform(Xte)
    m = fs.get(name, **({"n_features": 8} if name == "MRMR" else {"k": 8})).fit(Xtr, ytr, feature_names=names)
    Xtr_s, Xte_s = m.transform(Xtr), m.transform(Xte)
    # contrato de dimensão
    assert Xtr_s.shape[1] == Xte_s.shape[1] == len(m.selected_)
    # índices válidos e únicos
    assert len(set(m.selected_)) == len(m.selected_)
    assert all(0 <= i < Xtr.shape[1] for i in m.selected_)
    assert len(m.selected_names_) == len(m.selected_)


def test_broken_raises_clear_error(data):
    Xtr, Xte, ytr, yte, names = data
    for name in ("fit_criterion_measure", "RecursiveElimination", "TPhMGWO"):
        with pytest.raises(fs.NotSupportedError):
            fs.get(name).fit(Xtr, ytr)


def test_per_method_file_import():
    from itmofs_lab.filters.univariate.gini_index import GiniIndex
    from itmofs_lab.ensembles.WeightBased import WeightBased
    assert "ENTRA" in GiniIndex.info()
    assert WeightBased.name == "WeightBased"


def test_cli_smoke(capsys):
    from itmofs_lab.cli import main
    main(["list", "--family", "filters.univariate"])
    out = capsys.readouterr().out
    assert "gini_index" in out
    main(["info", "gini_index"])
    assert "ENTRA" in capsys.readouterr().out
