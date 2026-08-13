"""Adaptadores do projeto (não alteram a ITMO_FS)."""

from __future__ import annotations

import ITMO_FS as I


class UnivariateModelAdapter:
    """Modelo compatível com BestSum: expõe selected_features e best_score.

    O BestSum da ITMO_FS espera modelos com esses atributos após fit; o
    best_score vem de validação cruzada SOMENTE no treino.
    """

    def __init__(self, measure_string: str, k: int = 8, cv: int = 3):
        self.measure_string = measure_string
        self.k = k
        self.cv = cv
        self.selected_features = []
        self.best_score = 0.0

    def fit(self, X, y):
        from sklearn.linear_model import LogisticRegression
        from sklearn.model_selection import cross_val_score
        uf = I.UnivariateFilter(self.measure_string, ("K best", self.k))
        uf.fit(X, y)
        self.selected_features = [int(i) for i in uf.selected_features]
        self.best_score = float(cross_val_score(
            LogisticRegression(max_iter=500), X[:, self.selected_features], y, cv=self.cv).mean())
        return self

    def predict(self, X):
        raise NotImplementedError("use fit()+cut()")
