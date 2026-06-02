import numpy as np
import matplotlib.pyplot as plt
from models.charge import Charge
from physics.net_force import calculate_net_force
from physics.electric_field import calculate_electric_field_at_point
from visualization.plot_1d import plot_system_1d_mpl as plot_system_1d
from visualization.plot_2d import plot_system_2d_mpl as plot_system_2d
from visualization.plot_field import plot_electric_field_mpl as plot_electric_field
SCREENSHOT_DIR = 'assets/screenshots'
FORCE_1D_FILENAME = f'{SCREENSHOT_DIR}/fuerza_1d.png'
FORCE_2D_FILENAME = f'{SCREENSHOT_DIR}/fuerza_2d.png'
FIELD_MAP_FILENAME = f'{SCREENSHOT_DIR}/campo_electrico.png'

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print('Entrada inválida. Por favor, ingrese un número.')

def get_positive_int_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print('Debe ser un número entero positivo.')
        except ValueError:
            print('Entrada inválida. Por favor, ingrese un número entero.')

def display_menu():
    print('\n' + '=' * 40)
    print('   Simulador de Cargas Eléctricas')
    print('=' * 40)
    print('1. Modo 1D')
    print('2. Modo 2D')
    print('3. Salir')
    return input('Seleccione modo (1/2/3): ')

def is_duplicate_position(charges, x, y):
    return any((c.x == x and c.y == y for c in charges))

def collect_charges(mode):
    num_charges = get_positive_int_input('Ingrese el número de cargas: ')
    charges = []
    for i in range(num_charges):
        while True:
            print(f'\nDatos para la carga {i + 1}:')
            q = get_float_input('  Valor de la carga (C): ')
            x = get_float_input('  Posición X (m): ')
            y = get_float_input('  Posición Y (m): ') if mode == '2' else 0.0
            if is_duplicate_position(charges, x, y):
                print('Error: Dos cargas no pueden estar en la misma posición. Reintente.')
                continue
            charges.append(Charge(q, x, y))
            break
    return charges

def select_target_charge(charges):
    print('\nSeleccione la carga objetivo para calcular la fuerza neta:')
    for i, charge in enumerate(charges):
        print(f'{i + 1}. Carga {i + 1} en ({charge.x}, {charge.y})')
    while True:
        try:
            idx = int(input('Índice: ')) - 1
            if 0 <= idx < len(charges):
                return (charges[idx], idx)
            print('Índice fuera de rango. Intente de nuevo.')
        except ValueError:
            print('Entrada inválida. Por favor, ingrese un número entero.')

def display_force_results(mode, target_idx, net_force, charges):
    print(f'\n--- Resultados Detallados para la Carga {target_idx + 1} ---')
    target = charges[target_idx]
    from physics.coulomb import calculate_coulomb_force
    from physics.vectors import calculate_distance
    print('\nInteracciones Individuales:')
    for i, other in enumerate(charges):
        if i == target_idx:
            continue
        dist = calculate_distance((target.x, target.y), (other.x, other.y))
        f_vec = calculate_coulomb_force(other, target)
        print(f'  Desde Carga {i + 1}: Distancia = {dist:.4f} m, Fuerza Fx = {f_vec[0]:.4e} N, Fy = {f_vec[1]:.4e} N')
    print(f'\nFUERZA NETA TOTAL:')
    print(f'  Fx: {net_force[0]:.4e} N')
    if mode == '2':
        print(f'  Fy: {net_force[1]:.4e} N')
    magnitude = np.linalg.norm(net_force)
    print(f'  Magnitud: {magnitude:.4e} N')
    if mode == '1':
        direction = 'DERECHA (+)' if net_force[0] > 0 else 'IZQUIERDA (-)' if net_force[0] < 0 else 'NULA'
        print(f'  Dirección: {direction}')
    else:
        angle = np.degrees(np.arctan2(net_force[1], net_force[0]))
        print(f'  Dirección (ángulo): {angle:.2f}°')

def save_force_plot(mode, charges, target_charge, net_force):
    filename = FORCE_1D_FILENAME if mode == '1' else FORCE_2D_FILENAME
    if mode == '1':
        fig = plot_system_1d(charges, target_charge, net_force, filename=filename)
    else:
        fig = plot_system_2d(charges, target_charge, net_force, filename=filename)
    plt.close(fig)

def ask_yes_no(question):
    return input(f'\n{question} (s/n): ').strip().lower() == 's'

def calculate_and_display_field_at_point(mode, charges):
    try:
        px = get_float_input('  Posición X del punto (m): ')
        py = get_float_input('  Posición Y del punto (m): ') if mode == '2' else 0.0
        e_field = calculate_electric_field_at_point((px, py), charges)
        print(f'\n--- Campo Eléctrico en ({px}, {py}) ---')
        print(f'Ex: {e_field[0]:.4e} N/C')
        if mode == '2':
            print(f'Ey: {e_field[1]:.4e} N/C')
        print(f'Magnitud: {np.linalg.norm(e_field):.4e} N/C')
    except ValueError as e:
        print(f'Error: {e}')

def run_simulation(mode):
    charges = collect_charges(mode)
    if not charges:
        return
    if mode == '1' and len(charges) < 2:
        print('Aviso: El requerimiento mínimo para 1D son 2 cargas.')
    elif mode == '2' and len(charges) < 3:
        print('Aviso: El requerimiento mínimo para 2D son 3 cargas.')
    print('\nSistema inicial cargado.')
    target_charge, target_idx = select_target_charge(charges)
    net_force = calculate_net_force(target_charge, charges)
    display_force_results(mode, target_idx, net_force, charges)
    save_force_plot(mode, charges, target_charge, net_force)
    print('\n--- Cálculo de Campo Eléctrico ---')
    print('(Se recomienda calcular al menos en 3 puntos para cumplir con los requisitos)')
    while True:
        calculate_and_display_field_at_point(mode, charges)
        if not ask_yes_no('¿Desea calcular el campo en otro punto?'):
            break
    if mode == '2':
        generate_field_map(charges)
    print('\n' + '-' * 30)
    input('Presione Enter para volver al menú principal...')

def main():
    while True:
        mode = display_menu()
        if mode == '3':
            print('¡Gracias por usar el simulador! Adiós.')
            break
        elif mode in ('1', '2'):
            run_simulation(mode)
        else:
            print('Opción no válida. Intente de nuevo.')
if __name__ == '__main__':
    main()