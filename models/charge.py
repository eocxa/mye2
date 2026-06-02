from dataclasses import dataclass

@dataclass
class Charge:
    q: float
    x: float
    y: float = 0.0

    def __post_init__(self):
        self.q = float(self.q)
        self.x = float(self.x)
        self.y = float(self.y)