from typing import Optional


class Nodo:
    """
    Representa un nodo en el árbol sintáctico de derivación.

    Atributos:
        etiqueta  : Nombre del símbolo (terminal o no-terminal).
        hijos     : Lista de nodos hijos (vacía si es hoja).
        es_hoja   : True si el nodo es un símbolo terminal (palabra real).
    """

    def __init__(self, etiqueta: str, es_hoja: bool = False) -> None:
        self.etiqueta: str = etiqueta
        self.hijos: list["Nodo"] = []
        self.es_hoja: bool = es_hoja

    def agregar_hijo(self, hijo: "Nodo") -> None:
        """Agrega un nodo hijo a este nodo."""
        self.hijos.append(hijo)

    def __repr__(self) -> str:
        return f"Nodo({self.etiqueta!r}, hijos={len(self.hijos)})"


# ─────────────────────────────────────────────
# Impresión del árbol en formato textual
# ─────────────────────────────────────────────

def imprimir_arbol(nodo: Nodo, prefijo: str = "", es_raiz: bool = True) -> None:
    """
    Imprime el árbol sintáctico en la consola usando caracteres Unicode
    para representar la jerarquía de ramas (estilo 'tree' de Unix).

    Parámetros:
        nodo     : El nodo actual a imprimir.
        prefijo  : Cadena acumulada de indentación para las líneas anteriores.
        es_raiz  : True si es el nodo raíz (no imprime conector).

    Ejemplo de salida:
        S
        └── SPAM
            ├── IMP
            ├── PROM
            └── BEN
    """
    print(prefijo + nodo.etiqueta)
    _imprimir_hijos(nodo, prefijo, es_raiz)


def _imprimir_hijos(nodo: Nodo, prefijo: str, es_raiz: bool) -> None:
    """Imprime recursivamente los hijos de un nodo con la indentación correcta."""
    for i, hijo in enumerate(nodo.hijos):
        ultimo = (i == len(nodo.hijos) - 1)
        conector = "└── " if ultimo else "├── "
        extension = "    " if ultimo else "│   "
        print(prefijo + conector + hijo.etiqueta)
        _imprimir_hijos(hijo, prefijo + extension, False)


def arbol_a_cadena(nodo: Nodo, prefijo: str = "", es_raiz: bool = True) -> str:
    """
    Igual que imprimir_arbol pero devuelve el resultado como string
    (útil para pruebas y logging).

    Ejemplo:
        S
        └── SPAM
            ├── IMP
            ├── PROM
            └── BEN
    """
    resultado = prefijo + nodo.etiqueta + "\n"
    resultado += _hijos_a_cadena(nodo, prefijo)
    return resultado


def _hijos_a_cadena(nodo: Nodo, prefijo: str) -> str:
    """Genera recursivamente la representación de los hijos."""
    resultado = ""
    for i, hijo in enumerate(nodo.hijos):
        ultimo = (i == len(nodo.hijos) - 1)
        conector = "└── " if ultimo else "├── "
        extension = "    " if ultimo else "│   "
        resultado += prefijo + conector + hijo.etiqueta + "\n"
        resultado += _hijos_a_cadena(hijo, prefijo + extension)
    return resultado


def obtener_clasificacion(arbol: Nodo) -> Optional[str]:
    """
    Recorre el árbol para encontrar el primer hijo de la raíz S,
    que corresponde a la clasificación (SPAM, SOSPECHOSO o NORMAL).

    Retorna None si el árbol está vacío o malformado.
    """
    if arbol.hijos:
        return arbol.hijos[0].etiqueta
    return None