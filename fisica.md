# Interpretación Física de los Resultados

Este documento proporciona una base teórica y respuestas a las preguntas guía del proyecto, basadas en los resultados numéricos obtenidos con el simulador.

## Tabla de Resultados

### Caso 1D — 2 cargas positivas (1e-06 C en x=0 m y x=1 m)
| Parámetro | Valor |
|-----------|-------|
| q1 | 1.00e-06 C en x=0.0 m |
| q2 | 1.00e-06 C en x=1.0 m |
| Distancia r | 1.0000 m |
| Fuerza sobre q2 (Fx) | 8.99e-03 N (derecha) |
| Fuerza neta sobre q2 | 8.99e-03 N, dirección: DERECHA (+) |

### Caso 2D — 3 cargas positivas (triángulo equilátero)
| Parámetro | Valor |
|-----------|-------|
| q1 | 1.00e-06 C en (0.0, 0.0) m |
| q2 | 1.00e-06 C en (1.0, 0.0) m |
| q3 | 1.00e-06 C en (0.5, 0.866) m |
| Fuerza q3-q1 (Fx, Fy) | (4.50e-03, 7.79e-03) N |
| Fuerza q3-q2 (Fx, Fy) | (-4.50e-03, 7.79e-03) N |
| Fuerza neta (Fx, Fy) | (0.00e+00, 1.56e-02) N |
| Magnitud | 1.56e-02 N |
| Dirección | 90.00° (vertical hacia arriba) |

### Caso Campo Eléctrico — 1 carga positiva (1e-06 C en origen)
| Punto | Ex (N/C) | Ey (N/C) | \|E\| (N/C) |
|-------|----------|----------|-------------|
| (1.0, 0.0) | 8.99e+03 | 0.00e+00 | 8.99e+03 |
| (0.0, 1.0) | 0.00e+00 | 8.99e+03 | 8.99e+03 |
| (1.0, 1.0) | 3.18e+03 | 3.18e+03 | 4.50e+03 |

---

## 1. ¿Las cargas se atraen o se repelen?
Depende del producto de sus signos (ley de los signos de las cargas):
- **Cargas del mismo signo (+/+ o -/-):** Se repelen. La fuerza neta apunta alejándose de la otra carga.
- **Cargas de signo opuesto (+/-):** Se atraen. La fuerza neta apunta hacia la otra carga.

En nuestros resultados: las 3 cargas del caso 2D son positivas y se repelen entre sí, por eso q3 experimenta una fuerza neta hacia arriba (90°), alejándose de q1 y q2.

## 2. ¿Cómo influye el signo de la carga?
El signo determina la dirección del vector de fuerza y de campo eléctrico:
- Una carga **positiva** genera un campo eléctrico que "sale" de ella (radialmente hacia afuera).
- Una carga **negativa** genera un campo eléctrico que "entra" en ella (radialmente hacia adentro).
- El signo de la **carga objetivo** también invierte la dirección de la fuerza recibida respecto al campo eléctrico local ($\vec{F} = q\vec{E}$).

En el caso de campo eléctrico: la carga positiva en el origen produce un campo que apunta radialmente hacia afuera. En (1, 0) el campo es Ex=8.99e+03 N/C (hacia +X), y en (0, 1) es Ey=8.99e+03 N/C (hacia +Y), confirmando que el campo "sale" de la carga positiva.

## 3. ¿Cómo cambia la fuerza cuando cambia la distancia?
Sigue la **Ley del Inverso del Cuadrado** ($F \propto 1/r^2$):
- Si la distancia se reduce a la mitad ($r/2$), la fuerza aumenta **cuatro veces**.
- Si la distancia se duplica ($2r$), la fuerza se reduce a **una cuarta parte**.

En el caso 1D con r=1 m, F=8.99e-03 N. Si r=0.5 m, F=3.60e-02 N (4x mayor). Si r=2 m, F=2.25e-03 N (1/4 de la original). Esto explica por qué las interacciones son muy intensas a distancias cortas y decaen rápidamente al alejarse.

## 4. ¿Por qué las fuerzas se suman como vectores?
Debido al **Principio de Superposición**. Las fuerzas eléctricas son magnitudes vectoriales porque tienen tanto magnitud como dirección. Cuando múltiples cargas actúan sobre una sola, la interacción de cada par es independiente de las demás, y el efecto total es la suma geométrica (vectorial) de todas las contribuciones individuales.

En el caso 2D: q3 recibe dos fuerzas — de q1 con Fx=+4.50e-03, Fy=+7.79e-03 y de q2 con Fx=-4.50e-03, Fy=+7.79e-03. Las componentes x se cancelan exactamente por simetría (suman 0), mientras las componentes y se suman constructivamente (1.56e-02 N). Esto demuestra la superposición vectorial en acción.

## 5. ¿Qué representa el campo eléctrico en un punto?
Representa la perturbación que las cargas generan en el espacio que las rodea. Físicamente, es la **fuerza por unidad de carga** que experimentaría una "carga de prueba" positiva colocada en ese punto ($E = F/q_{prueba}$). No requiere que haya una carga físicamente presente en el punto para existir.

En el punto (1, 1), el campo es |E|=4.50e+03 N/C con componentes Ex=Ey=3.18e+03 N/C, apuntando en dirección 45° alejándose de la carga fuente en el origen.

## 6. ¿Cuál es la diferencia entre fuerza eléctrica y campo eléctrico?
- **Fuerza eléctrica:** Es una interacción entre **dos o más** cargas. Requiere al menos dos cargas para manifestarse. Ej: la fuerza neta de 1.56e-02 N sobre q3 en el caso 2D.
- **Campo eléctrico:** Es una propiedad del **espacio** generada por una o más cargas. Existe independientemente de si hay otra carga presente para sentirlo. Ej: el campo de 8.99e+03 N/C en (1, 0) generado por la carga en el origen.
- Relación: $\vec{F} = q\vec{E}$. Si colocáramos q=1e-06 C en (1,0), la fuerza sería F = (1e-06)(8.99e+03) = 8.99e-03 N.

## 7. ¿Qué limitaciones tiene el modelo de cargas puntuales?
- Asume que la carga no tiene dimensiones (volumen cero), lo cual es una idealización matemática.
- En la realidad, las cargas están distribuidas en objetos con geometría finita.
- A distancias extremadamente pequeñas ($r \to 0$), el modelo predice fuerzas infinitas (singularidad en r=0), requiriendo mecánica cuántica para una descripción correcta.
- No considera efectos relativistas si las cargas se mueven a altas velocidades.
- No modela efectos de apantallamiento en medios dieléctricos.
