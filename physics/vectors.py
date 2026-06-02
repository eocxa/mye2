import numpy as np

def calculate_distance(p1, p2):
    return np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def calculate_unit_vector(source_pos, target_pos):
    dx = target_pos[0] - source_pos[0]
    dy = target_pos[1] - source_pos[1]
    dist = np.sqrt(dx ** 2 + dy ** 2)
    if dist == 0:
        raise ValueError('No se puede calcular el vector unitario entre puntos coincidentes (distancia cero).')
    return np.array([dx / dist, dy / dist])