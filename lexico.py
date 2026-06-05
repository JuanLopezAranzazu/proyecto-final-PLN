from typing import Optional

# ─────────────────────────────────────────────
# Léxico: mapeo token → categoría léxica
# ─────────────────────────────────────────────

LEXICO: dict[str, str] = {

    # ══════════════════════════════════════════════════════════════
    # CATEGORÍAS SIN GÉNERO (no forman sintagma nominal con DET)
    # ══════════════════════════════════════════════════════════════

    # ── Imperativos (IMP) ─────────────────────────────────────────
    "gana":       "IMP",
    "obtén":      "IMP",
    "obten":      "IMP",
    "consigue":   "IMP",
    "reclama":    "IMP",
    "aprovecha":  "IMP",
    "descarga":   "IMP",
    "activa":     "IMP",
    "registrate": "IMP",
    "regístrate": "IMP",
    "haz":        "IMP",
    "llama":      "IMP",
    "envía":      "IMP",
    "envia":      "IMP",
    "compra":     "IMP",
    "suscríbete": "IMP",
    "suscribete": "IMP",

    # ── Promesas / Productos (PROM) ───────────────────────────────
    "dinero":     "PROM",
    "premio":     "PROM",
    "premios":    "PROM",
    "oferta":     "PROM",
    "ganancia":   "PROM",
    "ganancias":  "PROM",
    "recompensa": "PROM",
    "bono":       "PROM",
    "bonos":      "PROM",
    "crédito":    "PROM",
    "credito":    "PROM",
    "préstamo":   "PROM",
    "prestamo":   "PROM",
    "millones":   "PROM",
    "fortuna":    "PROM",
    "riqueza":    "PROM",
    "efectivo":   "PROM",
    "regalo":     "PROM",

    # ── Beneficios (BEN) ──────────────────────────────────────────
    "gratis":       "BEN",
    "gratuito":     "BEN",
    "gratuita":     "BEN",
    "rápido":       "BEN",
    "rapido":       "BEN",
    "fácil":        "BEN",
    "facil":        "BEN",
    "exclusivo":    "BEN",
    "exclusiva":    "BEN",
    "garantizado":  "BEN",
    "garantizada":  "BEN",
    "inmediato":    "BEN",
    "inmediata":    "BEN",
    "seguro":       "BEN",
    "limitado":     "BEN",
    "especial":     "BEN",
    "increíble":    "BEN",
    "increible":    "BEN",

    # ── Alertas / Urgencia (ALERT) ────────────────────────────────
    "urgente":    "ALERT",
    "ahora":      "ALERT",
    "hoy":        "ALERT",
    "último":     "ALERT",
    "ultimo":     "ALERT",
    "expira":     "ALERT",
    "vence":      "ALERT",
    "plazo":      "ALERT",
    "tiempo":     "ALERT",
    "límite":     "ALERT",
    "limite":     "ALERT",
    "advertencia":"ALERT",
    "cuidado":    "ALERT",
    "atención":   "ALERT",
    "atencion":   "ALERT",
    "alerta":     "ALERT",

    # ── Verbos neutros (VERB) ─────────────────────────────────────
    "revisa":     "VERB",
    "revisó":     "VERB",
    "reviso":     "VERB",
    "revisaron":  "VERB",
    "consulta":   "VERB",
    "envió":      "VERB",
    "envio":      "VERB",
    "adjuntó":    "VERB",
    "adjunto":    "VERB",
    "preparó":    "VERB",
    "preparo":    "VERB",
    "actualizó":  "VERB",
    "actualizo":  "VERB",
    "completó":   "VERB",
    "completo":   "VERB",
    "generó":     "VERB",
    "genero":     "VERB",
    "publicó":    "VERB",
    "publico":    "VERB",
    "solicitó":   "VERB",
    "solicito":   "VERB",
    "presentó":   "VERB",
    "presenta":   "VERB",
    "confirma":   "VERB",
    "verificó":   "VERB",
    "verifico":   "VERB",
    "reportó":    "VERB",
    "reporto":    "VERB",

    # ══════════════════════════════════════════════════════════════
    # CATEGORÍAS CON RASGO DE GÉNERO
    # ══════════════════════════════════════════════════════════════

    # ── Determinantes masculinos (DET_M) ──────────────────────────
    # Artículos y demostrativos que concuerdan con sustantivos masculinos.
    # Nota: "mi", "tu", "su" son invariables en género pero se duplican
    #       para permitir su uso con ambos géneros en la gramática.
    "el":       "DET_M",   # artículo definido masc. singular
    "un":       "DET_M",   # artículo indefinido masc. singular
    "este":     "DET_M",   # demostrativo proximal masc. singular
    "ese":      "DET_M",   # demostrativo medial masc. singular
    "aquel":    "DET_M",   # demostrativo distal masc. singular
    "nuestro":  "DET_M",   # posesivo masc. singular
    "dicho":    "DET_M",   # determinante referencial masc.

    # ── Determinantes femeninos (DET_F) ───────────────────────────
    "la":       "DET_F",   # artículo definido fem. singular
    "una":      "DET_F",   # artículo indefinido fem. singular
    "esta":     "DET_F",   # demostrativo proximal fem. singular
    "esa":      "DET_F",   # demostrativo medial fem. singular
    "aquella":  "DET_F",   # demostrativo distal fem. singular
    "nuestra":  "DET_F",   # posesivo fem. singular
    "dicha":    "DET_F",   # determinante referencial fem.

    # ── Determinantes plurales (DET_PL) ───────────────────────────
    # El plural en español puede ser masc. o fem., pero para este modelo
    # se unifica en DET_PL y se combina con OBJ_PL / SUJ_PL.
    "los":      "DET_PL",
    "las":      "DET_PL",
    "unos":     "DET_PL",
    "unas":     "DET_PL",
    "estos":    "DET_PL",
    "estas":    "DET_PL",
    "esos":     "DET_PL",
    "esas":     "DET_PL",

    # ── Determinantes invariables de género (DET_I) ───────────────
    # Posesivos y otros determinantes que no marcan género:
    # "mi libro" / "mi factura" → ambos válidos.
    "mi":       "DET_I",
    "tu":       "DET_I",
    "su":       "DET_I",

    # ══════════════════════════════════════════════════════════════
    # SUJETOS CON GÉNERO
    # ══════════════════════════════════════════════════════════════

    # ── Sujetos masculinos (SUJ_M) ────────────────────────────────
    # Sustantivos genéricos masculinos: roles, cargos y entidades.
    # Se eliminaron nombres propios para mayor generalidad.
    "usuario":      "SUJ_M",
    "usuarios":     "SUJ_M",
    "cliente":      "SUJ_M",
    "clientes":     "SUJ_M",
    "empleado":     "SUJ_M",
    "empleados":    "SUJ_M",
    "proveedor":    "SUJ_M",
    "proveedores":  "SUJ_M",
    "director":     "SUJ_M",
    "gerente":      "SUJ_M",
    "equipo":       "SUJ_M",
    "equipos":      "SUJ_M",
    "sistema":      "SUJ_M",
    "sistemas":     "SUJ_M",
    "departamento": "SUJ_M",
    "servidor":     "SUJ_M",
    "administrador":"SUJ_M",
    "él":           "SUJ_M",
    "ellos":        "SUJ_M",
    "nosotros":     "SUJ_M",

    # ── Sujetos femeninos (SUJ_F) ─────────────────────────────────
    # Sustantivos genéricos femeninos: roles, cargos y entidades.
    "usuaria":      "SUJ_F",
    "usuarias":     "SUJ_F",
    "clienta":      "SUJ_F",
    "clientas":     "SUJ_F",
    "empleada":     "SUJ_F",
    "empleadas":    "SUJ_F",
    "empresa":      "SUJ_F",
    "empresas":     "SUJ_F",
    "área":         "SUJ_F",
    "area":         "SUJ_F",
    "dirección":    "SUJ_F",
    "direccion":    "SUJ_F",
    "organización": "SUJ_F",
    "organizacion": "SUJ_F",
    "plataforma":   "SUJ_F",
    "aplicación":   "SUJ_F",
    "aplicacion":   "SUJ_F",
    "ella":         "SUJ_F",
    "ellas":        "SUJ_F",

    # ══════════════════════════════════════════════════════════════
    # OBJETOS CON GÉNERO
    # ══════════════════════════════════════════════════════════════

    # ── Objetos masculinos (OBJ_M) ────────────────────────────────
    # Sustantivos de género masculino usados como complemento directo.
    "informe":    "OBJ_M",
    "documento":  "OBJ_M",
    "reporte":    "OBJ_M",
    "archivo":    "OBJ_M",
    "correo":     "OBJ_M",
    "mensaje":    "OBJ_M",
    "contrato":   "OBJ_M",
    "formulario": "OBJ_M",
    "proyecto":   "OBJ_M",
    "resultado":  "OBJ_M",
    "resumen":    "OBJ_M",
    "análisis":   "OBJ_M",
    "analisis":   "OBJ_M",
    "registro":   "OBJ_M",
    "libro":      "OBJ_M",
    "borrador":   "OBJ_M",
    "presupuesto":"OBJ_M",
    "proceso":    "OBJ_M",

    # ── Objetos femeninos (OBJ_F) ─────────────────────────────────
    # Sustantivos de género femenino usados como complemento directo.
    "factura":      "OBJ_F",
    "propuesta":    "OBJ_F",
    "lista":        "OBJ_F",
    "solicitud":    "OBJ_F",
    "información":  "OBJ_F",
    "informacion":  "OBJ_F",
    "nota":         "OBJ_F",
    "orden":        "OBJ_F",    # "la orden" → fem. en contexto administrativo
    "resolución":   "OBJ_F",
    "resolucion":   "OBJ_F",
    "acta":         "OBJ_F",
    "carta":        "OBJ_F",
    "tabla":        "OBJ_F",
    "base":         "OBJ_F",
    "versión":      "OBJ_F",
    "version":      "OBJ_F",

    # ── Objetos plurales (OBJ_PL) ─────────────────────────────────
    # Formas plurales que combinan con DET_PL.
    "documentos":  "OBJ_PL",
    "archivos":    "OBJ_PL",
    "resultados":  "OBJ_PL",
    "datos":       "OBJ_PL",
    "registros":   "OBJ_PL",
    "informes":    "OBJ_PL",
    "reportes":    "OBJ_PL",
    "contratos":   "OBJ_PL",
    "facturas":    "OBJ_PL",
    "propuestas":  "OBJ_PL",
}


# ─────────────────────────────────────────────
# Función principal de categorización
# ─────────────────────────────────────────────

def categoria(token: str) -> Optional[str]:
    """
    Devuelve la categoría léxica (con rasgo de género si aplica) de un token.

    Parámetros:
        token : Palabra a categorizar (se normaliza a minúsculas).

    Retorna:
        La etiqueta léxica (str) o None si el token es OOV.

    Ejemplos:
        >>> categoria("el")
        'DET_M'
        >>> categoria("la")
        'DET_F'
        >>> categoria("informe")
        'OBJ_M'
        >>> categoria("factura")
        'OBJ_F'
    """
    return LEXICO.get(token.lower())


def tokenizar(texto: str) -> list[str]:
    """
    Divide un texto en tokens normalizando a minúsculas y eliminando
    signos de puntuación.

    Ejemplo:
        >>> tokenizar("El equipo revisó la factura.")
        ['el', 'equipo', 'revisó', 'la', 'factura']
    """
    import re
    texto_limpio = re.sub(r"[^\w\sáéíóúüñÁÉÍÓÚÜÑ]", "", texto)
    return [t.lower() for t in texto_limpio.split() if t]


def categorizar_tokens(tokens: list[str]) -> list[tuple[str, Optional[str]]]:
    """
    Aplica categoria() a cada token y retorna pares (token, categoría).

    Ejemplo:
        >>> categorizar_tokens(["el", "informe", "revisa"])
        [('el', 'DET_M'), ('informe', 'OBJ_M'), ('revisa', 'VERB')]
    """
    return [(token, categoria(token)) for token in tokens]