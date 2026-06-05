# Proyecto final PLN

## Integrantes

| Nombre completo                  | Código   |
|----------------------------------|----------|
| Juan Esteban López Aránzazu      | 2313026  |
| Victor Manuel Álzate Morales     | 2313022  |

---

## Descripción

Este proyecto implementa un sistema de detección de mensajes spam en español utilizando técnicas clásicas de Procesamiento de Lenguaje Natural (PLN) basadas en modelos formales.

A diferencia de los sistemas modernos que emplean aprendizaje automático o redes neuronales, esta propuesta utiliza una combinación de:

* Léxico estructurado
* Gramáticas Libres de Contexto (CFG)
* Parser descendente recursivo
* Árboles de derivación
* Gramáticas Probabilísticas Libres de Contexto (PCFG)

El objetivo es identificar si un mensaje pertenece a una de las siguientes categorías:

* **SPAM**
* **SOSPECHOSO**
* **NORMAL**

La clasificación se realiza a partir de la estructura sintáctica reconocida por la gramática y de la probabilidad asociada a la derivación obtenida.

---

## Objetivos

### Objetivo General

Desarrollar un sistema de detección de spam en español basado en gramáticas formales y análisis sintáctico probabilístico.

### Objetivos Específicos

* Implementar un léxico categorizado para el dominio de mensajes spam.
* Definir una Gramática Libre de Contexto (CFG) para modelar patrones lingüísticos.
* Construir un parser descendente recursivo capaz de validar mensajes.
* Generar árboles sintácticos para representar las derivaciones.
* Implementar una Gramática Probabilística Libre de Contexto (PCFG).
* Calcular la probabilidad de cada árbol sintáctico.
* Clasificar mensajes según la estructura reconocida.

---

## Requisitos

* Python 3.10 o superior

No se utilizan librerías externas de PLN.

---

## Ejecución

Clonar el repositorio:

```bash
git clone https://github.com/JuanLopezAranzazu/proyecto-final-PLN.git
```

Ejecutar la aplicación:

```bash
python main.py
```

---

## Restricciones

Este proyecto tiene fines académicos y busca demostrar el uso de modelos formales para el procesamiento de lenguaje natural.

No pretende competir con sistemas modernos basados en aprendizaje profundo ni cubrir todas las variaciones del español.

---

## Tecnologías Utilizadas

* Python
* Gramáticas Libres de Contexto (CFG)
* Gramáticas Probabilísticas Libres de Contexto (PCFG)
* Parsers Descendentes Recursivos
* Árboles de Derivación

---

## Documentación

- [Enunciado del proyecto](docs/enunciado.pdf)
- [Informe del proyecto](docs/informe_proyecto.pdf)