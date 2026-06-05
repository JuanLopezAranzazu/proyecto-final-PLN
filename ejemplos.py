from typing import NamedTuple


class Ejemplo(NamedTuple):
    texto: str
    clase_esperada: str
    descripcion: str


EJEMPLOS: list[Ejemplo] = [

    # ── SPAM ────────────────────────────────────────────────────────
    Ejemplo("gana dinero gratis",            "SPAM", "IMP+PROM+BEN canónico"),
    Ejemplo("obtén premio gratis",           "SPAM", "IMP+PROM+BEN"),
    Ejemplo("consigue bono exclusivo",       "SPAM", "IMP+PROM+BEN"),
    Ejemplo("reclama regalo gratuito",       "SPAM", "IMP+PROM+BEN"),
    Ejemplo("consigue premio gratis ahora",  "SPAM", "IMP+PROM+BEN+ALERT"),
    Ejemplo("obtén dinero urgente",          "SPAM", "IMP+PROM+ALERT"),
    Ejemplo("activa ahora premio gratis",    "SPAM", "IMP+ALERT+PROM+BEN"),
    Ejemplo("urgente gana dinero gratis",    "SPAM", "ALERT+IMP+PROM+BEN"),

    # ── SOSPECHOSO ──────────────────────────────────────────────────
    Ejemplo("obtén dinero",                      "SOSPECHOSO", "IMP+PROM"),
    Ejemplo("premio gratis",                     "SOSPECHOSO", "PROM+BEN"),
    Ejemplo("consigue gratis",                   "SOSPECHOSO", "IMP+BEN"),
    Ejemplo("oferta urgente",                    "SOSPECHOSO", "PROM+ALERT"),
    Ejemplo("activa ahora",                      "SOSPECHOSO", "IMP+ALERT"),
    Ejemplo("urgente oferta",                    "SOSPECHOSO", "ALERT+PROM"),
    Ejemplo("ahora consigue dinero",             "SOSPECHOSO", "ALERT+IMP+PROM"),
    Ejemplo("el cliente gana un premio",         "SOSPECHOSO", "DET_M+SUJ_M+IMP+DET_M+PROM"),
    Ejemplo("la empresa gana una recompensa",    "SOSPECHOSO", "DET_F+SUJ_F+IMP+DET_F+PROM"),

    # ── NORMAL sin artículo ─────────────────────────────────────────
    Ejemplo("usuario revisa informe",              "NORMAL", "SUJ_M+VERB+OBJ_M"),
    Ejemplo("empleada consulta documento",         "NORMAL", "SUJ_F+VERB+OBJ_M"),
    Ejemplo("gerente confirma solicitud",          "NORMAL", "SUJ_M+VERB+OBJ_F"),
    Ejemplo("ella adjunto archivo documento",      "NORMAL", "SUJ_F+VERB+OBJ_M+OBJ_M"),
    Ejemplo("revisa documento",                    "NORMAL", "VERB+OBJ_M sin sujeto"),
    Ejemplo("director presentó propuesta proyecto","NORMAL", "SUJ_M+VERB+OBJ_F+OBJ_M"),

    # ── NORMAL con DET — concordancia CORRECTA ──────────────────────
    Ejemplo("el usuario revisa el informe",          "NORMAL", "DET_M+SUJ_M ✓  DET_M+OBJ_M ✓"),
    Ejemplo("la empresa consulta la factura",        "NORMAL", "DET_F+SUJ_F ✓  DET_F+OBJ_F ✓"),
    Ejemplo("un cliente presentó un reporte",        "NORMAL", "DET_M+SUJ_M ✓  DET_M+OBJ_M ✓"),
    Ejemplo("una empleada generó una propuesta",     "NORMAL", "DET_F+SUJ_F ✓  DET_F+OBJ_F ✓"),
    Ejemplo("revisa el documento",                   "NORMAL", "VERB + DET_M+OBJ_M ✓"),
    Ejemplo("consulta la solicitud",                 "NORMAL", "VERB + DET_F+OBJ_F ✓"),
    Ejemplo("mi equipo revisó mi informe",           "NORMAL", "DET_I+SUJ_M ✓  DET_I+OBJ_M ✓"),
    Ejemplo("su empresa presentó su propuesta",      "NORMAL", "DET_I+SUJ_F ✓  DET_I+OBJ_F ✓"),
    Ejemplo("los equipos revisaron los archivos",    "NORMAL", "DET_PL+SUJ_M ✓  DET_PL+OBJ_PL ✓"),
    Ejemplo("el sistema generó un reporte",          "NORMAL", "DET_M+SUJ_M ✓  DET_M+OBJ_M ✓"),
    Ejemplo("el proveedor envió el contrato",        "NORMAL", "DET_M+SUJ_M ✓  DET_M+OBJ_M ✓"),
    Ejemplo("la plataforma generó la versión",       "NORMAL", "DET_F+SUJ_F ✓  DET_F+OBJ_F ✓"),
    Ejemplo("el administrador verificó el proceso",  "NORMAL", "DET_M+SUJ_M ✓  DET_M+OBJ_M — 'proceso' es OBJ_M"),

    # ── CONCORDANCIA INCORRECTA → DESCONOCIDO ───────────────────────
    Ejemplo("un factura",    "DESCONOCIDO", "DET_M + OBJ_F ✗"),
    Ejemplo("una informe",   "DESCONOCIDO", "DET_F + OBJ_M ✗"),
    Ejemplo("el propuesta",  "DESCONOCIDO", "DET_M + OBJ_F ✗"),
    Ejemplo("la proyecto",   "DESCONOCIDO", "DET_F + OBJ_M ✗"),
    Ejemplo("un solicitud",  "DESCONOCIDO", "DET_M + OBJ_F ✗"),
    Ejemplo("una documento", "DESCONOCIDO", "DET_F + OBJ_M ✗"),

    # ── DESCONOCIDO (OOV) ────────────────────────────────────────────
    Ejemplo("hola mundo",   "DESCONOCIDO", "tokens fuera del léxico"),
    Ejemplo("",             "DESCONOCIDO", "texto vacío"),
]


def ejecutar_pruebas(verbose: bool = True) -> dict[str, int]:
    from clasificador import clasificar

    correctos = incorrectos = 0
    total = len(EJEMPLOS)

    print("=" * 65)
    print("  SUITE DE PRUEBAS DEL CLASIFICADOR")
    print("=" * 65)

    for i, ej in enumerate(EJEMPLOS, 1):
        r = clasificar(ej.texto)
        acierto = r.clasificacion == ej.clase_esperada
        correctos += acierto
        incorrectos += not acierto

        if verbose:
            simbolo = "✓" if acierto else "✗"
            display = f'"{ej.texto}"' if ej.texto else "(vacío)"
            print(f"\n  [{i:02d}] {simbolo} {display}")
            print(f"       Esperado:  {ej.clase_esperada}")
            print(f"       Obtenido:  {r.clasificacion}")
            if r.parsing_exitoso:
                print(f"       P(árbol):  {r.probabilidad:.6f}")
            if not acierto:
                print(f"       ⚠ FALLO — {ej.descripcion}")

    print("\n" + "=" * 65)
    print("  RESUMEN")
    print(f"  Total:      {total}")
    print(f"  Correctos:  {correctos}  ({100*correctos/total:.1f}%)")
    print(f"  Fallidos:   {incorrectos}  ({100*incorrectos/total:.1f}%)")
    print("=" * 65)
    return {"correctos": correctos, "incorrectos": incorrectos, "total": total}


def ejemplos_por_clase(clase: str) -> list[Ejemplo]:
    return [e for e in EJEMPLOS if e.clase_esperada == clase]