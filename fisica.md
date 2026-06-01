# Interpretación Física de los Resultados

Este documento proporciona una base teórica y respuestas a las preguntas guía del proyecto, basadas en el modelo implementado en el simulador.

## 1. ¿Las cargas se atraen o se repelen?
Depende del producto de sus signos (ley de los signos de las cargas):
- **Cargas del mismo signo (+/+ o -/-):** Se repelen. La fuerza neta apunta alejándose de la otra carga.
- **Cargas de signo opuesto (+/-):** Se atraen. La fuerza neta apunta hacia la otra carga.

## 2. ¿Cómo influye el signo de la carga?
El signo determina la dirección del vector de fuerza y de campo eléctrico:
- Una carga **positiva** genera un campo eléctrico que "sale" de ella (radialmente hacia afuera).
- Una carga **negativa** genera un campo eléctrico que "entra" en ella (radialmente hacia adentro).
- El signo de la **carga objetivo** también invierte la dirección de la fuerza recibida respecto al campo eléctrico local ($\vec{F} = q\vec{E}$).

## 3. ¿Cómo cambia la fuerza cuando cambia la distancia?
Sigue la **Ley del Inverso del Cuadrado** ($F \propto 1/r^2$):
- Si la distancia se reduce a la mitad ($r/2$), la fuerza aumenta **cuatro veces**.
- Si la distancia se duplica ($2r$), la fuerza se reduce a **una cuarta parte**.
- Esto explica por qué las interacciones son muy intensas a distancias cortas y decaen rápidamente al alejarse.

## 4. ¿Por qué las fuerzas se suman como vectores?
Debido al **Principio de Superposición**. Las fuerzas eléctricas son magnitudes vectoriales porque tienen tanto magnitud como dirección. Cuando múltiples cargas actúan sobre una sola, la interacción de cada par es independiente de las demás, y el efecto total es la suma geométrica (vectorial) de todas las contribuciones individuales.

## 5. ¿Qué representa el campo eléctrico en un punto?
Representa la perturbación que las cargas generan en el espacio que las rodea. Físicamente, es la **fuerza por unidad de carga** que experimentaría una "carga de prueba" positiva colocada en ese punto ($E = F/q_{prueba}$). No requiere que haya una carga físicamente presente en el punto para existir.

## 6. ¿Cuál es la diferencia entre fuerza eléctrica y campo eléctrico?
- **Fuerza eléctrica:** Es una interacción entre **dos o más** cargas. Requiere al menos dos cargas para manifestarse.
- **Campo eléctrico:** Es una propiedad del **espacio** generada por una o más cargas. Existe independientemente de si hay otra carga presente para sentirlo.
- Relación: $\vec{F} = q\vec{E}$.

## 7. ¿Qué limitaciones tiene el modelo de cargas puntuales?
- Asume que la carga no tiene dimensiones (volumen cero), lo cual es una idealización matemática.
- En la realidad, las cargas están distribuidas en objetos con geometría.
- A distancias extremadamente pequeñas ($r \to 0$), el modelo predice fuerzas infinitas, lo cual requiere de mecánica cuántica y electrodinámica cuántica para ser explicado correctamente.
- No considera efectos relativistas si las cargas se mueven a altas velocidades.
