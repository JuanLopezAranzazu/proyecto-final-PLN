from typing import Optional
from arbol import Nodo
from gramatica import GRAMATICA, SIMBOLO_INICIAL


class Parser:
    """
    Parser descendente recursivo con backtracking para la gramática CFG.

    El parser mantiene un puntero (cursor) sobre la lista de tokens.
    Cuando intenta una producción, avanza el cursor; si falla, lo restaura
    al valor anterior (backtracking).

    Atributos:
        tokens  : Lista de categorías léxicas de la oración a analizar.
        cursor  : Posición actual en la lista de tokens.
        exito   : True si el parsing fue exitoso.
    """

    def __init__(self, tokens: list[str]) -> None:
        self.tokens: list[str] = tokens
        self.cursor: int = 0
        self.exito: bool = False

    # ─────────────────────────────────────────────
    # Punto de entrada del análisis
    # ─────────────────────────────────────────────

    def parsear(self) -> Optional[Nodo]:
        """
        Ejecuta el parsing completo desde el símbolo inicial S.

        Retorna el árbol sintáctico si el parsing es exitoso, None si falla.
        """
        self.cursor = 0
        self.exito = False

        raiz = Nodo(SIMBOLO_INICIAL)
        if self._expandir_nt(SIMBOLO_INICIAL, raiz) and self.cursor == len(self.tokens):
            self.exito = True
            return raiz
        return None

    # ─────────────────────────────────────────────
    # Expansión de un no-terminal
    # ─────────────────────────────────────────────

    def _expandir_nt(self, nt: str, nodo: Nodo) -> bool:
        """
        Intenta cada producción de 'nt' con backtracking completo.

        Para cada producción A → B1 B2 ... Bk:
          - Crea un nodo hijo por cada Bi
          - Si Bi es terminal: verifica contra el token actual
          - Si Bi es no-terminal: recursiona
          - Si algún Bi falla: deshace todos los cambios (backtracking)

        El resultado final añade directamente a 'nodo' los hijos
        correspondientes a la producción exitosa (B1, B2, ..., Bk),
        NO un nodo envolvente adicional. Esto garantiza:

            S → SPAM → IMP PROM BEN
            se convierte en:
            S.hijos = [SPAM]
            SPAM.hijos = [IMP, PROM, BEN]
        """
        producciones = GRAMATICA.get(nt, [])

        for produccion in producciones:
            cursor_inicial = self.cursor
            hijos_nuevos: list[Nodo] = []
            exito = True

            for simbolo in produccion:
                if simbolo in GRAMATICA:
                    # Símbolo no-terminal: crear nodo y expandir recursivamente
                    hijo = Nodo(simbolo)
                    if self._expandir_nt(simbolo, hijo):
                        hijos_nuevos.append(hijo)
                    else:
                        exito = False
                        break
                else:
                    # Símbolo terminal: comparar con token actual
                    if self.cursor < len(self.tokens) and self.tokens[self.cursor] == simbolo:
                        hoja = Nodo(simbolo, es_hoja=True)
                        hijos_nuevos.append(hoja)
                        self.cursor += 1
                    else:
                        exito = False
                        break

            if exito:
                # Producción exitosa: agregar los hijos al nodo padre
                for hijo in hijos_nuevos:
                    nodo.agregar_hijo(hijo)
                return True
            else:
                # Backtracking: restaurar cursor (hijos_nuevos se descarta)
                self.cursor = cursor_inicial

        return False


# ─────────────────────────────────────────────
# Función de alto nivel
# ─────────────────────────────────────────────

def analizar(categorias: list[str]) -> tuple[bool, Optional[Nodo]]:
    """
    Función de alto nivel que instancia el parser y ejecuta el análisis.

    Parámetros:
        categorias : Lista de categorías léxicas (salida del léxico).

    Retorna:
        Una tupla (éxito, árbol) donde:
          - éxito : True si la cadena pertenece al lenguaje.
          - árbol : El árbol sintáctico, o None si el parsing falló.

    Ejemplo:
        >>> analizar(['IMP', 'PROM', 'BEN'])
        (True, Nodo('S', hijos=1))
    """
    parser = Parser(categorias)
    arbol = parser.parsear()
    return parser.exito, arbol