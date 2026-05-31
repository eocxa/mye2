# Simulador de Cargas Eléctricas

Este proyecto es un simulador educativo para modelar sistemas de cargas eléctricas puntuales en 1D y 2D. Permite calcular fuerzas eléctricas (Ley de Coulomb), fuerza neta (superposición) y campo eléctrico.

## Estructura del Proyecto

- `main.py`: Punto de entrada de la aplicación.
- `models/`: Definición de la clase `Charge`.
- `physics/`: Motores de cálculo (Coulomb, Superposición, Campo Eléctrico).
- `visualization/`: Módulos para generar gráficas con Matplotlib.
- `tests/`: Casos de prueba para validación.

## Requisitos

- Python 3.x
- NumPy
- Matplotlib

Instalación de dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Ejecute el simulador con:
```bash
python main.py
```

Siga las instrucciones en pantalla para seleccionar el modo (1D/2D), ingresar las cargas y visualizar los resultados.

## Pruebas

Para ejecutar las pruebas automáticas:
```bash
python tests/case_1d.py
python tests/case_2d.py
python tests/case_field.py
```
