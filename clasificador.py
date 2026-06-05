from dataclasses import dataclass, field
from typing import Optional

from lexico import tokenizar, categorizar_tokens, categoria
from parser import analizar
from pcfg import prob_arbol
from arbol import Nodo, obtener_clasificacion, arbol_a_cadena


# ─────────────────────────────────────────────
# Estructura de resultado
# ─────────────────────────────────────────────

@dataclass
class ResultadoClasificacion:
    """
    Encapsula el resultado completo del proceso de clasificación.

    Atributos:
        texto_original   : El mensaje original sin modificar.
        tokens           : Lista de tokens extraídos.
        categorias       : Lista de categorías léxicas asignadas.
        pares            : Lista de tuplas (token, categoría).
        tokens_validos   : True si todos los tokens están en el léxico.
        tokens_invalidos : Lista de tokens que no están en el léxico.
        parsing_exitoso  : True si el parser encontró una derivación válida.
        arbol            : El árbol sintáctico generado (None si falló).
        clasificacion    : La etiqueta asignada (SPAM/SOSPECHOSO/NORMAL/DESCONOCIDO).
        probabilidad     : La probabilidad del árbol según la PCFG.
        representacion_arbol : Árbol en formato de texto.
    """
    texto_original: str = ""
    tokens: list[str] = field(default_factory=list)
    categorias: list[str] = field(default_factory=list)
    pares: list[tuple[str, Optional[str]]] = field(default_factory=list)
    tokens_validos: bool = False
    tokens_invalidos: list[str] = field(default_factory=list)
    parsing_exitoso: bool = False
    arbol: Optional[Nodo] = None
    clasificacion: str = "DESCONOCIDO"
    probabilidad: float = 0.0
    representacion_arbol: str = ""


# ─────────────────────────────────────────────
# Función principal de clasificación
# ─────────────────────────────────────────────

def clasificar(texto: str) -> ResultadoClasificacion:
    """
    Clasifica un mensaje de texto ejecutando el pipeline completo.

    Etapas:
        1. Tokenización del texto
        2. Análisis léxico (asignación de categorías)
        3. Verificación de tokens fuera de vocabulario (OOV)
        4. Parsing CFG con backtracking
        5. Extracción de la clasificación del árbol
        6. Cálculo de probabilidad PCFG
        7. Empaquetado del resultado

    Parámetros:
        texto : Cadena de texto en español a clasificar.

    Retorna:
        ResultadoClasificacion con toda la información del análisis.
    """
    resultado = ResultadoClasificacion(texto_original=texto)

    # ── Etapa 1: Tokenización ─────────────────────────────────────
    resultado.tokens = tokenizar(texto)

    if not resultado.tokens:
        resultado.clasificacion = "DESCONOCIDO"
        return resultado

    # ── Etapa 2: Análisis léxico ──────────────────────────────────
    resultado.pares = categorizar_tokens(resultado.tokens)

    # Separar tokens válidos e inválidos (OOV)
    resultado.tokens_invalidos = [
        token for token, cat in resultado.pares if cat is None
    ]
    resultado.tokens_validos = len(resultado.tokens_invalidos) == 0

    # Obtener sólo las categorías de los tokens válidos
    resultado.categorias = [
        cat for _, cat in resultado.pares if cat is not None
    ]

    # Si hay tokens fuera de vocabulario, el análisis no puede continuar
    if not resultado.tokens_validos:
        resultado.clasificacion = "DESCONOCIDO"
        return resultado

    # ── Etapa 3: Parsing CFG ──────────────────────────────────────
    exito, arbol = analizar(resultado.categorias)
    resultado.parsing_exitoso = exito
    resultado.arbol = arbol

    if not exito or arbol is None:
        resultado.clasificacion = "DESCONOCIDO"
        return resultado

    # ── Etapa 4: Extracción de clasificación ──────────────────────
    clasificacion = obtener_clasificacion(arbol)
    if clasificacion:
        resultado.clasificacion = clasificacion
    else:
        resultado.clasificacion = "DESCONOCIDO"

    # ── Etapa 5: Probabilidad PCFG ────────────────────────────────
    resultado.probabilidad = prob_arbol(arbol)

    # ── Etapa 6: Representación del árbol ─────────────────────────
    resultado.representacion_arbol = arbol_a_cadena(arbol)

    return resultado


# ─────────────────────────────────────────────
# Funciones de presentación
# ─────────────────────────────────────────────

def formatear_resultado(r: ResultadoClasificacion) -> str:
    """
    Genera la representación completa del resultado de clasificación
    para mostrar en la interfaz de línea de comandos (CLI).

    Parámetros:
        r : El resultado de clasificación a formatear.

    Retorna:
        Cadena multi-línea con toda la información del análisis.
    """
    lineas: list[str] = []
    lineas.append("=" * 50)
    lineas.append(f"  Mensaje: \"{r.texto_original}\"")
    lineas.append("=" * 50)

    # ── Tokens y categorías ───────────────────────────────────────
    lineas.append("\nTokens:")
    for token, cat in r.pares:
        if cat is not None:
            lineas.append(f"  {token:<15s} →  {cat}")
        else:
            lineas.append(f"  {token:<15s} →  [DESCONOCIDO — fuera de léxico]")

    # ── Tokens fuera de vocabulario ───────────────────────────────
    if r.tokens_invalidos:
        lineas.append(f"\n⚠  Tokens no reconocidos: {', '.join(r.tokens_invalidos)}")
        lineas.append("   El mensaje no puede analizarse con el léxico actual.")

    # ── Árbol sintáctico ──────────────────────────────────────────
    if r.parsing_exitoso and r.arbol:
        lineas.append("\nÁrbol Sintáctico:")
        for linea in r.representacion_arbol.strip().split("\n"):
            lineas.append("  " + linea)
    elif r.tokens_validos:
        lineas.append("\nÁrbol Sintáctico:")
        lineas.append("  [No se pudo construir — la secuencia de categorías no")
        lineas.append("   coincide con ninguna regla de la gramática]")

    # ── Probabilidad ──────────────────────────────────────────────
    if r.parsing_exitoso:
        lineas.append("\nProbabilidad (PCFG):")
        lineas.append(f"  P(árbol) = {r.probabilidad:.6f}")

    # ── Clasificación final ───────────────────────────────────────
    lineas.append("\nClasificación:")
    etiqueta_visual = _etiqueta_con_icono(r.clasificacion)
    lineas.append(f"  {etiqueta_visual}")
    lineas.append("=" * 50)

    return "\n".join(lineas)


def _etiqueta_con_icono(clasificacion: str) -> str:
    """
    Devuelve la etiqueta de clasificación acompañada de un símbolo visual
    para facilitar la lectura en la consola.
    """
    iconos = {
        "SPAM":        "🔴  SPAM",
        "SOSPECHOSO":  "🟡  SOSPECHOSO",
        "NORMAL":      "🟢  NORMAL",
        "DESCONOCIDO": "⚪  DESCONOCIDO",
    }
    return iconos.get(clasificacion, f"?  {clasificacion}")


def clasificar_varios(textos: list[str]) -> list[ResultadoClasificacion]:
    """
    Clasifica una lista de mensajes y retorna los resultados.

    Parámetros:
        textos : Lista de cadenas de texto a clasificar.

    Retorna:
        Lista de ResultadoClasificacion en el mismo orden.
    """
    return [clasificar(texto) for texto in textos]