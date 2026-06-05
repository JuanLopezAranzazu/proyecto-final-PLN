Regla = tuple[str, ...]
CFG = dict[str, list[Regla]]

GRAMATICA: CFG = {

    # ── Símbolo inicial ─────────────────────────────────────────────
    "S": [
        ("SPAM",),
        ("SOSPECHOSO",),
        ("NORMAL",),
    ],

    # ── SPAM ────────────────────────────────────────────────────────
    # Los tokens de spam (IMP, PROM, BEN, ALERT) no tienen género,
    # por lo que las reglas SPAM no cambian.
    "SPAM": [
        ("IMP", "IMP", "PROM", "BEN"),
        ("IMP", "PROM", "BEN", "ALERT"),
        ("IMP", "ALERT", "PROM", "BEN"),
        ("ALERT", "IMP", "PROM", "BEN"),
        ("IMP", "PROM", "ALERT"),
        ("IMP", "BEN", "PROM"),
        ("IMP", "PROM", "PROM"),
        ("IMP", "PROM", "BEN"),
    ],

    # ── SOSPECHOSO ──────────────────────────────────────────────────
    # SN_S agrupa todas las variantes de género del sujeto.
    "SOSPECHOSO": [
        ("ALERT", "IMP", "PROM"),
        ("SN_S", "IMP", "PROM"),
        ("VERB", "PROM", "BEN"),
        ("IMP", "PROM", "SN_S"),
        ("SN_S", "IMP", "DET_M", "PROM"),
        ("SN_S", "IMP", "DET_F", "PROM"),
        ("SN_S", "IMP", "DET_I", "PROM"),
        ("IMP", "PROM"),
        ("PROM", "BEN"),
        ("IMP", "BEN"),
        ("PROM", "ALERT"),
        ("IMP", "ALERT"),
        ("ALERT", "PROM"),
    ],

    # ── NORMAL ──────────────────────────────────────────────────────
    # Todas las posiciones de sujeto/objeto usan SN_S / SN_O
    # para que la concordancia de género se resuelva en los sub-no-terminales.
    "NORMAL": [
        ("SN_S", "SN_S", "VERB", "SN_O"),
        ("SN_S", "VERB", "SN_S", "SN_O"),
        ("SN_S", "VERB", "SN_O", "SN_O"),
        ("VERB", "SN_O", "SN_O"),
        ("SN_S", "VERB", "SN_O"),
        ("SN_S", "VERB"),
        ("VERB", "SN_O"),
    ],

    # ══════════════════════════════════════════════════════════════
    # SINTAGMAS NOMINALES — NIVEL ABSTRACTO
    # SN_S y SN_O son "sumideros" que delegan a variantes con género.
    # ══════════════════════════════════════════════════════════════

    # ── SN_S — Sintagma Nominal Sujeto (abstracto) ─────────────────
    # Delega a la variante de género correcta.
    "SN_S": [
        ("SN_S_M",),   # sujeto masculino
        ("SN_S_F",),   # sujeto femenino
        ("SN_S_I",),   # sujeto con DET invariable
        ("SN_S_PL",),  # sujeto plural
    ],

    # ── SN_O — Sintagma Nominal Objeto (abstracto) ─────────────────
    "SN_O": [
        ("SN_O_M",),   # objeto masculino
        ("SN_O_F",),   # objeto femenino
        ("SN_O_I",),   # objeto con DET invariable
        ("SN_O_PL",),  # objeto plural
    ],

    # ══════════════════════════════════════════════════════════════
    # SINTAGMAS NOMINALES — VARIANTES CON GÉNERO
    # La concordancia se garantiza porque DET_M sólo aparece con SUJ_M/OBJ_M,
    # DET_F sólo con SUJ_F/OBJ_F, etc.
    # ══════════════════════════════════════════════════════════════

    # ── SN_S_M — Sujeto masculino ──────────────────────────────────
    #   "el equipo", "equipo"
    "SN_S_M": [
        ("DET_M", "SUJ_M"),   # artículo definido/indefinido masc. + nombre masc.
        ("SUJ_M",),           # nombre masculino sin artículo
    ],

    # ── SN_S_F — Sujeto femenino ───────────────────────────────────
    #   "la empresa", "empresa"
    "SN_S_F": [
        ("DET_F", "SUJ_F"),
        ("SUJ_F",),
    ],

    # ── SN_S_I — Sujeto con determinante invariable ────────────────
    #   "mi equipo", "su empresa", "tu sistema"
    "SN_S_I": [
        ("DET_I", "SUJ_M"),
        ("DET_I", "SUJ_F"),
    ],

    # ── SN_S_PL — Sujeto plural ────────────────────────────────────
    #   "los equipos" — por simplicidad se omite SUJ_PL del léxico;
    #   se incluye la regla para extensibilidad futura.
    "SN_S_PL": [
        ("DET_PL", "SUJ_M"),   # plural con base masc. (los equipos)
        ("DET_PL", "SUJ_F"),   # plural con base fem. (las empresas)
    ],

    # ── SN_O_M — Objeto masculino ──────────────────────────────────
    #   "el informe", "un documento", "informe", "documento"
    "SN_O_M": [
        ("DET_M", "OBJ_M"),
        ("OBJ_M",),
    ],

    # ── SN_O_F — Objeto femenino ───────────────────────────────────
    #   "la factura", "una propuesta", "factura", "solicitud"
    "SN_O_F": [
        ("DET_F", "OBJ_F"),
        ("OBJ_F",),
    ],

    # ── SN_O_I — Objeto con determinante invariable ────────────────
    #   "mi informe", "su factura", "tu proyecto"
    "SN_O_I": [
        ("DET_I", "OBJ_M"),
        ("DET_I", "OBJ_F"),
    ],

    # ── SN_O_PL — Objeto plural ────────────────────────────────────
    #   "los documentos", "las facturas", "unos datos"
    "SN_O_PL": [
        ("DET_PL", "OBJ_PL"),
        ("OBJ_PL",),
    ],
}

SIMBOLO_INICIAL: str = "S"


# ─────────────────────────────────────────────
# Funciones auxiliares
# ─────────────────────────────────────────────

def obtener_producciones(no_terminal: str) -> list[Regla]:
    """Retorna las producciones de un no-terminal."""
    return GRAMATICA.get(no_terminal, [])


def es_no_terminal(simbolo: str) -> bool:
    return simbolo in GRAMATICA


def es_terminal(simbolo: str) -> bool:
    return simbolo not in GRAMATICA


def listar_terminales() -> set[str]:
    terminales: set[str] = set()
    for producciones in GRAMATICA.values():
        for prod in producciones:
            for s in prod:
                if es_terminal(s):
                    terminales.add(s)
    return terminales


def listar_no_terminales() -> set[str]:
    return set(GRAMATICA.keys())


def describir_gramatica() -> str:
    """Representación textual de la CFG en notación BNF."""
    lineas = ["=== Gramática Libre de Contexto (CFG) con Concordancia de Género ===\n"]
    for lhs, producciones in GRAMATICA.items():
        for i, rhs in enumerate(producciones):
            flecha = "→" if i == 0 else " |"
            lineas.append(f"  {lhs:<12s} {flecha} {' '.join(rhs)}")
    return "\n".join(lineas)