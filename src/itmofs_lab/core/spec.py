"""MethodSpec: descrição padronizada de "o que entra e o que sai" de cada método.

É a base do comando de ajuda (``.info()`` no Python e ``itmofs-lab info <nome>``
na linha de comando).
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Optional


# Status possíveis de execução na ITMO_FS 0.3.3 (fonte: auditoria empírica).
STATUS = {
    "OK": "Executa normalmente.",
    "OK_WITH_ADAPTER": "Executa via adaptador do itmofs-lab (API run/feature_ranking ou modelo).",
    "BROKEN_IN_0_3_3": "Quebrado na ITMO_FS 0.3.3 (bug da biblioteca ou incompatibilidade).",
    "DEPENDENCY_MISSING": "Requer dependência externa ausente (ex.: solver de QP).",
    "LEAKAGE_BY_DESIGN": "A API exige dados de teste no fit — viola anti-leakage; não recomendado.",
    "SUPPORT_ONLY": "Componente de apoio; não seleciona features.",
}


@dataclass
class MethodSpec:
    """Metadados de um método. `inputs`/`outputs` respondem 'o que entra/sai'."""
    name: str                       # nome curto canônico (ex.: "gini_index")
    display: str                    # nome de exibição (ex.: "Gini Index")
    family: str                     # ex.: "filters.univariate", "ensembles", "wrappers"
    component_type: str             # score_function, criterion_function, standalone_selector, ...
    summary: str                    # uma linha: o que faz
    itmo_symbol: str                # símbolo real na ITMO_FS
    itmo_signature: str             # assinatura real observada
    status: str = "OK"              # chave de STATUS

    # ----- ENTRADAS (o que entra) -----
    needs_X: bool = True
    y: str = "required"             # required | optional | not_used
    requires_discrete: bool = False
    requires_nonnegative: bool = False
    recommends_scaling: str = "optional"   # optional | standard | minmax | discretize | none
    params: dict = field(default_factory=dict)   # hiperparâmetros -> descrição

    # ----- SAÍDAS (o que sai) -----
    outputs_scores: bool = False
    outputs_ranking: bool = True
    outputs_subset: bool = True
    selected_attr: str = "selected_"       # atributo padronizado do itmofs-lab
    transforms_test: bool = True

    # ----- extras -----
    cutting_rule: str = "n/a"
    quirks: str = ""
    example: str = ""
    references: str = ""

    def as_dict(self) -> dict:
        return asdict(self)

    def io_text(self) -> str:
        """Texto amigável de 'o que entra / o que sai' (usado pelo help)."""
        y_map = {"required": "obrigatório", "optional": "opcional", "not_used": "não usado"}
        pre = []
        if self.requires_discrete:
            pre.append("dados discretizados")
        if self.requires_nonnegative:
            pre.append("dados não negativos (X>=0)")
        if self.recommends_scaling not in ("optional", "none"):
            pre.append(f"escala recomendada: {self.recommends_scaling}")
        pre_txt = "; ".join(pre) if pre else "nenhum pré-processamento obrigatório"

        outs = []
        outs.append("scores por feature" if self.outputs_scores else "sem score global")
        outs.append("ranking" if self.outputs_ranking else "sem ranking")
        outs.append("subconjunto selecionado" if self.outputs_subset else "não seleciona subconjunto")
        if self.transforms_test:
            outs.append("transforma treino e teste")

        params_txt = "\n".join(f"    - {k}: {v}" for k, v in self.params.items()) or "    (nenhum)"

        return (
            f"Método: {self.display}  [{self.name}]\n"
            f"Família: {self.family}  |  tipo: {self.component_type}\n"
            f"Status na ITMO_FS 0.3.3: {self.status} — {STATUS.get(self.status,'')}\n"
            f"Resumo: {self.summary}\n\n"
            f"ENTRA:\n"
            f"  X: {'sim' if self.needs_X else 'não'}\n"
            f"  y: {y_map.get(self.y, self.y)}\n"
            f"  pré-processamento: {pre_txt}\n"
            f"  parâmetros:\n{params_txt}\n\n"
            f"SAI:\n  " + "; ".join(outs) + "\n"
            f"  atributos após fit: {self.selected_attr}, selected_names_"
            + (", scores_" if self.outputs_scores else "") + "\n\n"
            f"Assinatura ITMO_FS: {self.itmo_signature}\n"
            + (f"Atenções: {self.quirks}\n" if self.quirks else "")
            + (f"Exemplo:\n{self.example}\n" if self.example else "")
        )
