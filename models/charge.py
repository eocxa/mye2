from dataclasses import dataclass

@dataclass
class Charge:
    """
    Representación de una carga eléctrica puntual.
    q: Valor de la carga en Culombios (C)
    x: Posición en el eje X (m)
    y: Posición en el eje Y (m), por defecto 0 para sistemas 1D
    """
    q: float
    x: float
    y: float = 0.0

    def __post_init__(self):
        # Asegurar que los tipos sean correctos
        self.q = float(self.q)
        self.x = float(self.x)
        self.y = float(self.y)
