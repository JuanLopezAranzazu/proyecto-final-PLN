import sys

from clasificador import clasificar, formatear_resultado
from gramatica import describir_gramatica
from pcfg import describir_pcfg, verificar_consistencia
from lexico import LEXICO
from ejemplos import ejecutar_pruebas


# ─────────────────────────────────────────────
# Banner
# ─────────────────────────────────────────────

BANNER = """
╔══════════════════════════════════════════════════════╗
║     Clasificador de Mensajes — Modelos Formales      ║
║     CFG + Parser Recursivo + PCFG                    ║
║     PLN Universitario — Sin ML ni librerías externas ║
╚══════════════════════════════════════════════════════╝
"""


def mostrar_ayuda() -> None:
    """Imprime las instrucciones de uso del programa."""
    print("""
Uso:
  python main.py                    Modo interactivo
  python main.py "mensaje"          Clasificar un mensaje
  python main.py --pruebas          Ejecutar suite de pruebas
  python main.py --gramatica        Mostrar CFG y PCFG
  python main.py --lexico           Mostrar léxico completo
  python main.py --ayuda            Mostrar esta ayuda

Categorías de clasificación:
  SPAM         Mensaje publicitario no deseado
  SOSPECHOSO   Mensaje con rasgos parciales de spam
  NORMAL       Mensaje informativo legítimo
  DESCONOCIDO  No reconocido por la gramática
""")


# ─────────────────────────────────────────────
# Modo interactivo
# ─────────────────────────────────────────────

def modo_interactivo() -> None:
    """
    Ejecuta el clasificador en modo interactivo.
    El usuario ingresa mensajes y recibe la clasificación en tiempo real.
    Escribe 'salir', 'exit' o presiona Ctrl+C para terminar.
    """
    print(BANNER)
    print("Modo interactivo. Escribe un mensaje para clasificarlo.")
    print("Comandos especiales: 'salir', 'pruebas', 'gramatica', 'lexico'\n")

    while True:
        try:
            entrada = input(">>> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nSesión terminada.")
            break

        if not entrada:
            continue

        entrada_lower = entrada.lower()

        if entrada_lower in ("salir", "exit", "quit"):
            print("Hasta luego.")
            break
        elif entrada_lower == "pruebas":
            ejecutar_pruebas()
        elif entrada_lower == "gramatica":
            print(describir_gramatica())
            print()
            print(describir_pcfg())
        elif entrada_lower == "lexico":
            mostrar_lexico()
        elif entrada_lower in ("ayuda", "help"):
            mostrar_ayuda()
        else:
            # Clasificar el mensaje ingresado
            resultado = clasificar(entrada)
            print(formatear_resultado(resultado))
            print()


# ─────────────────────────────────────────────
# Modo de mensaje único (argumento CLI)
# ─────────────────────────────────────────────

def modo_mensaje(texto: str) -> None:
    """
    Clasifica un único mensaje pasado como argumento de línea de comandos.

    Parámetros:
        texto : El mensaje a clasificar.
    """
    resultado = clasificar(texto)
    print(formatear_resultado(resultado))


# ─────────────────────────────────────────────
# Modo gramática
# ─────────────────────────────────────────────

def modo_gramatica() -> None:
    """Muestra la CFG y la PCFG en formato legible."""
    print(BANNER)
    print(describir_gramatica())
    print()
    print(describir_pcfg())
    print()
    # Verificar consistencia
    sumas = verificar_consistencia()
    inconsistentes = [nt for nt, s in sumas.items() if abs(s - 1.0) > 1e-6]
    if inconsistentes:
        print(f"\n⚠  No-terminales con probabilidades inconsistentes: {inconsistentes}")
    else:
        print("\n✓  Todas las probabilidades de la PCFG son consistentes (suma = 1.0)")


# ─────────────────────────────────────────────
# Modo léxico
# ─────────────────────────────────────────────

def mostrar_lexico() -> None:
    """Muestra el léxico completo agrupado por categoría."""
    print("\n=== Léxico del Sistema ===\n")
    grupos: dict[str, list[str]] = {}
    for token, cat in sorted(LEXICO.items()):
        grupos.setdefault(cat, []).append(token)

    for cat in sorted(grupos.keys()):
        tokens = sorted(grupos[cat])
        print(f"  {cat}  ({len(tokens)} tokens):")
        # Imprimir en columnas de 4
        for i in range(0, len(tokens), 4):
            fila = tokens[i:i+4]
            print("    " + "  ".join(f"{t:<15}" for t in fila))
        print()


# ─────────────────────────────────────────────
# Demo de ejemplos predefinidos
# ─────────────────────────────────────────────

def demo_ejemplos_seleccionados() -> None:
    """
    Ejecuta una demostración rápida con ejemplos representativos
    de cada clase para mostrar el funcionamiento del sistema.
    """
    print(BANNER)
    print("  DEMOSTRACIÓN — Ejemplos representativos por clase\n")

    demo_textos = [
        "gana dinero gratis",           # SPAM canónico
        "consigue premio gratis ahora", # SPAM con ALERT
        "obtén dinero",                 # SOSPECHOSO
        "oferta urgente",               # SOSPECHOSO
        "juan revisa informe",          # NORMAL
        "revisa documento",             # NORMAL sin sujeto
        "hola mundo",                   # DESCONOCIDO
    ]

    for texto in demo_textos:
        resultado = clasificar(texto)
        print(formatear_resultado(resultado))
        print()


# ─────────────────────────────────────────────
# Punto de entrada principal
# ─────────────────────────────────────────────

def main() -> None:
    """
    Función principal. Determina el modo de ejecución según los argumentos
    de línea de comandos y delega al manejador correspondiente.
    """
    args = sys.argv[1:]

    if not args:
        # Sin argumentos: modo interactivo
        modo_interactivo()

    elif len(args) == 1:
        arg = args[0].lower()

        if arg in ("--pruebas", "-p", "pruebas"):
            print(BANNER)
            ejecutar_pruebas(verbose=True)

        elif arg in ("--gramatica", "-g", "gramatica"):
            modo_gramatica()

        elif arg in ("--lexico", "-l", "lexico"):
            print(BANNER)
            mostrar_lexico()

        elif arg in ("--demo", "-d", "demo"):
            demo_ejemplos_seleccionados()

        elif arg in ("--ayuda", "-h", "--help", "ayuda"):
            print(BANNER)
            mostrar_ayuda()

        elif arg.startswith("-"):
            print(f"Argumento desconocido: {args[0]}")
            mostrar_ayuda()
            sys.exit(1)

        else:
            # El argumento es el mensaje a clasificar
            modo_mensaje(args[0])

    else:
        # Múltiples argumentos: unirlos como un solo mensaje
        texto = " ".join(args)
        modo_mensaje(texto)


if __name__ == "__main__":
    main()