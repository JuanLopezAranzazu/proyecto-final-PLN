from arbol import Nodo

PCFG: dict[tuple[str, tuple[str, ...]], float] = {

    # ── S ───────────────────────────────────────────────────────────
    ("S", ("SPAM",)):        0.34,
    ("S", ("SOSPECHOSO",)):  0.33,
    ("S", ("NORMAL",)):      0.33,

    # ── SPAM ────────────────────────────────────────────────────────
    ("SPAM", ("IMP", "PROM", "BEN")):               0.30,
    ("SPAM", ("IMP", "PROM", "BEN", "ALERT")):      0.20,
    ("SPAM", ("IMP", "PROM", "ALERT")):             0.15,
    ("SPAM", ("IMP", "BEN", "PROM")):               0.12,
    ("SPAM", ("IMP", "ALERT", "PROM", "BEN")):      0.10,
    ("SPAM", ("ALERT", "IMP", "PROM", "BEN")):      0.07,
    ("SPAM", ("IMP", "PROM", "PROM")):              0.04,
    ("SPAM", ("IMP", "IMP", "PROM", "BEN")):        0.02,

    # ── SOSPECHOSO ──────────────────────────────────────────────────
    ("SOSPECHOSO", ("IMP", "PROM")):                    0.22,
    ("SOSPECHOSO", ("PROM", "BEN")):                    0.17,
    ("SOSPECHOSO", ("IMP", "BEN")):                     0.13,
    ("SOSPECHOSO", ("PROM", "ALERT")):                  0.11,
    ("SOSPECHOSO", ("IMP", "ALERT")):                   0.10,
    ("SOSPECHOSO", ("ALERT", "PROM")):                  0.08,
    ("SOSPECHOSO", ("ALERT", "IMP", "PROM")):           0.07,
    ("SOSPECHOSO", ("IMP", "PROM", "SN_S")):            0.04,
    ("SOSPECHOSO", ("SN_S", "IMP", "PROM")):            0.03,
    ("SOSPECHOSO", ("SN_S", "IMP", "DET_M", "PROM")):   0.01,
    ("SOSPECHOSO", ("SN_S", "IMP", "DET_F", "PROM")):   0.01,
    ("SOSPECHOSO", ("SN_S", "IMP", "DET_I", "PROM")):   0.01,
    ("SOSPECHOSO", ("VERB", "PROM", "BEN")):            0.02,

    # ── NORMAL ──────────────────────────────────────────────────────
    ("NORMAL", ("SN_S", "VERB", "SN_O")):              0.35,
    ("NORMAL", ("SN_S", "VERB", "SN_O", "SN_O")):      0.20,
    ("NORMAL", ("SN_S", "VERB")):                       0.15,
    ("NORMAL", ("VERB", "SN_O")):                       0.13,
    ("NORMAL", ("VERB", "SN_O", "SN_O")):               0.08,
    ("NORMAL", ("SN_S", "SN_S", "VERB", "SN_O")):       0.05,
    ("NORMAL", ("SN_S", "VERB", "SN_S", "SN_O")):       0.04,

    # ── SN_S — Sintagma Nominal Sujeto (abstracto) ──────────────────
    ("SN_S", ("SN_S_M",)):   0.40,
    ("SN_S", ("SN_S_F",)):   0.35,
    ("SN_S", ("SN_S_I",)):   0.15,
    ("SN_S", ("SN_S_PL",)):  0.10,

    # ── SN_O — Sintagma Nominal Objeto (abstracto) ──────────────────
    ("SN_O", ("SN_O_M",)):   0.38,
    ("SN_O", ("SN_O_F",)):   0.32,
    ("SN_O", ("SN_O_I",)):   0.12,
    ("SN_O", ("SN_O_PL",)):  0.18,

    # ── SN_S_M — Sujeto masculino ───────────────────────────────────
    # Con DET más probable en texto formal
    ("SN_S_M", ("DET_M", "SUJ_M")):  0.60,
    ("SN_S_M", ("SUJ_M",)):          0.40,

    # ── SN_S_F — Sujeto femenino ────────────────────────────────────
    ("SN_S_F", ("DET_F", "SUJ_F")):  0.60,
    ("SN_S_F", ("SUJ_F",)):          0.40,

    # ── SN_S_I — Sujeto con DET invariable ─────────────────────────
    ("SN_S_I", ("DET_I", "SUJ_M")):  0.50,
    ("SN_S_I", ("DET_I", "SUJ_F")):  0.50,

    # ── SN_S_PL — Sujeto plural ─────────────────────────────────────
    ("SN_S_PL", ("DET_PL", "SUJ_M")):  0.50,
    ("SN_S_PL", ("DET_PL", "SUJ_F")):  0.50,

    # ── SN_O_M — Objeto masculino ───────────────────────────────────
    ("SN_O_M", ("DET_M", "OBJ_M")):  0.65,
    ("SN_O_M", ("OBJ_M",)):          0.35,

    # ── SN_O_F — Objeto femenino ────────────────────────────────────
    ("SN_O_F", ("DET_F", "OBJ_F")):  0.65,
    ("SN_O_F", ("OBJ_F",)):          0.35,

    # ── SN_O_I — Objeto con DET invariable ─────────────────────────
    ("SN_O_I", ("DET_I", "OBJ_M")):  0.50,
    ("SN_O_I", ("DET_I", "OBJ_F")):  0.50,

    # ── SN_O_PL — Objeto plural ─────────────────────────────────────
    ("SN_O_PL", ("DET_PL", "OBJ_PL")):  0.70,
    ("SN_O_PL", ("OBJ_PL",)):           0.30,
}


def prob_regla(lhs: str, rhs: tuple[str, ...]) -> float:
    """Retorna la probabilidad de la producción A → α."""
    return PCFG.get((lhs, rhs), 0.0)


def prob_arbol(arbol: Nodo) -> float:
    """
    Calcula P(T) = ∏ p(Aᵢ → αᵢ) para todos los nodos internos del árbol.
    Los nodos hoja (terminales) contribuyen con probabilidad 1.0.
    """
    if not arbol.hijos:
        return 1.0

    rhs: tuple[str, ...] = tuple(hijo.etiqueta for hijo in arbol.hijos)
    p = prob_regla(arbol.etiqueta, rhs)
    if p == 0.0:
        return 0.0

    for hijo in arbol.hijos:
        p_hijo = prob_arbol(hijo)
        if p_hijo == 0.0:
            return 0.0
        p *= p_hijo

    return p


def verificar_consistencia() -> dict[str, float]:
    """Verifica que Σ p(A→α) = 1.0 para cada no-terminal A."""
    sumas: dict[str, float] = {}
    for (lhs, _), prob in PCFG.items():
        sumas[lhs] = sumas.get(lhs, 0.0) + prob
    return sumas


def describir_pcfg() -> str:
    """Representación textual de la PCFG."""
    lineas = ["=== Gramática Probabilística Libre de Contexto (PCFG) ===\n"]
    vistos: set[str] = set()
    for (lhs, rhs), prob in sorted(PCFG.items(), key=lambda x: (x[0][0], -x[1])):
        if lhs not in vistos:
            lineas.append(f"\n  {lhs}:")
            vistos.add(lhs)
        lineas.append(f"    → {' '.join(rhs):<40s}  p = {prob:.4f}")

    lineas.append("\n── Verificación de consistencia ──")
    for nt, s in sorted(verificar_consistencia().items()):
        ok = "✓" if abs(s - 1.0) < 1e-6 else "✗ INCONSISTENTE"
        lineas.append(f"  Σ p({nt} → *) = {s:.6f}  {ok}")
    return "\n".join(lineas)