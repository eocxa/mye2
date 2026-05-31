# Plan de Desarrollo del Proyecto

## Simulador de Cargas Eléctricas, Fuerza Eléctrica y Campo Eléctrico

---

# 1. Objetivo General

Desarrollar una aplicación capaz de modelar sistemas de cargas eléctricas puntuales en 1D y 2D, calcular fuerzas eléctricas mediante la Ley de Coulomb, determinar la fuerza neta sobre una carga seleccionada y calcular el campo eléctrico en puntos definidos por el usuario.

El sistema deberá incluir representaciones gráficas que permitan visualizar tanto las cargas como los vectores de fuerza y campo eléctrico.

---

# 2. Tecnologías Propuestas

## Lenguaje Principal

Python 3.x

### Justificación

* Fácil implementación matemática.
* Excelente soporte para gráficos científicos.
* Gran cantidad de librerías para simulación.
* Desarrollo rápido.

---

## Librerías

### NumPy

Responsabilidades:

* Operaciones vectoriales.
* Distancias.
* Magnitudes.
* Componentes.

### Matplotlib

Responsabilidades:

* Visualización 1D.
* Visualización 2D.
* Vectores de fuerza.
* Campo eléctrico.
* Mapas de intensidad.

### Dataclasses

Responsabilidades:

* Representación de cargas eléctricas.

---

# 3. Arquitectura del Proyecto

```text
electrostatic-simulator/

├── main.py
│
├── models/
│   └── charge.py
│
├── physics/
│   ├── coulomb.py
│   ├── net_force.py
│   ├── electric_field.py
│   └── vectors.py
│
├── visualization/
│   ├── plot_1d.py
│   ├── plot_2d.py
│   └── plot_field.py
│
├── tests/
│   ├── case_1d.py
│   ├── case_2d.py
│   └── case_field.py
│
├── assets/
│   ├── screenshots/
│   └── videos/
│
├── report/
│   └── reporte.pdf
│
├── requirements.txt
└── README.md
```

---

# 4. Flujo General del Sistema

```text
Inicio

↓

Seleccionar modo:
(1D o 2D)

↓

Ingresar número de cargas

↓

Ingresar datos de cada carga:
- valor
- signo
- posición

↓

Validar entradas

↓

Mostrar sistema inicial

↓

Seleccionar carga objetivo

↓

Calcular fuerzas individuales

↓

Calcular fuerza neta

↓

Mostrar resultados

↓

Definir puntos de análisis

↓

Calcular campo eléctrico

↓

Generar visualizaciones

↓

Fin
```

---

# 5. Etapas de Desarrollo

## ETAPA 1

### Modelo de datos

Objetivo:

Representar una carga eléctrica.

Resultado esperado:

Clase Charge.

Ejemplo conceptual:

```python
Charge(
    q=5e-6,
    x=2,
    y=3
)
```

---

## ETAPA 2

### Distancias

Objetivo:

Calcular separación entre cargas.

Resultado esperado:

Funciones para:

* distancia 1D
* distancia 2D

---

## ETAPA 3

### Fuerza entre dos cargas

Objetivo:

Implementar Ley de Coulomb.

Entradas:

* carga 1
* carga 2

Salida:

* magnitud
* dirección

Resultado esperado:

Calcular correctamente:

* atracción
* repulsión

---

## ETAPA 4

### Componentes Vectoriales

Objetivo:

Descomponer la fuerza en:

* Fx
* Fy

Resultado esperado:

Obtención de componentes para sistemas 2D.

---

## ETAPA 5

### Fuerza Neta

Objetivo:

Aplicar principio de superposición.

Resultado esperado:

Sumar todas las fuerzas que actúan sobre una carga.

Salida:

* Fx total
* Fy total
* Magnitud
* Dirección

---

## ETAPA 6

### Campo Eléctrico

Objetivo:

Calcular campo eléctrico producido por todas las cargas.

Resultado esperado:

Para cada punto:

* Ex
* Ey
* Magnitud del campo

---

## ETAPA 7

### Visualización 1D

Objetivo:

Representar:

* eje x
* cargas
* dirección de fuerza

Resultado esperado:

Gráfica simple y clara.

---

## ETAPA 8

### Visualización 2D

Objetivo:

Representar:

* plano cartesiano
* cargas
* vectores de fuerza
* fuerza neta

Resultado esperado:

Gráfica vectorial completa.

---

## ETAPA 9

### Campo Eléctrico

Objetivo:

Representar:

* vectores de campo
* dirección
* intensidad

Resultado esperado:

Mapa visual del campo eléctrico.

---

# 6. Validaciones Requeridas

El sistema deberá impedir:

## División entre cero

Caso:

Dos cargas en la misma posición.

---

## Campo sobre una carga

Caso:

Calcular campo exactamente donde existe una carga.

---

## Entradas inválidas

Caso:

Texto donde se espera un número.

---

## Auto interacción

Caso:

Calcular fuerza de una carga sobre sí misma.

---

# 7. Casos de Prueba

## Caso 1

### Sistema 1D

Configuración:

* 2 cargas
* eje x

Resultado esperado:

* fuerza eléctrica
* dirección

---

## Caso 2

### Sistema 2D

Configuración:

* 3 cargas

Resultado esperado:

* componentes Fx
* componentes Fy
* fuerza neta

---

## Caso 3

### Campo Eléctrico

Configuración:

* múltiples cargas
* tres puntos de análisis

Resultado esperado:

* Ex
* Ey
* magnitud
* representación gráfica

---

# 8. Resultados Esperados

Al finalizar el proyecto deberá existir:

## Software funcional

Capaz de:

* representar cargas
* calcular fuerzas
* calcular fuerza neta
* calcular campo eléctrico

---

## Visualizaciones

1. Sistema 1D
2. Sistema 2D
3. Campo eléctrico

---

## Evidencias

* Capturas de pantalla.
* Video de funcionamiento.

---

## Documentación

* README.
* Reporte PDF.

---

## Interpretación Física

Responder preguntas como:

* ¿Las cargas se atraen o repelen?
* ¿Cómo afecta la distancia?
* ¿Cómo afecta el signo de la carga?
* ¿Por qué se suman vectores?
* ¿Qué representa el campo eléctrico?

---

# 9. Meta Final

Construir una herramienta educativa que permita visualizar y analizar interacciones electrostáticas mediante la Ley de Coulomb, el principio de superposición y el concepto de campo eléctrico, integrando cálculo numérico y representación gráfica.
