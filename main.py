import sys
import numpy as np
import matplotlib.pyplot as plt
from models.charge import Charge
from physics.net_force import calculate_net_force
from physics.electric_field import calculate_electric_field_at_point
from visualization.plot_1d import plot_system_1d
from visualization.plot_2d import plot_system_2d
from visualization.plot_field import plot_electric_field

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número.")

def main():
    while True:
        print("\n" + "="*40)
        print("   Simulador de Cargas Eléctricas")
        print("="*40)
        print("1. Modo 1D")
        print("2. Modo 2D")
        print("3. Salir")
        mode = input("Seleccione modo (1/2/3): ")
        
        if mode == '3':
            print("¡Gracias por usar el simulador! Adiós.")
            break
            
        if mode not in ['1', '2']:
            print("Opción no válida. Intente de nuevo.")
            continue

        num_charges = int(get_float_input("Ingrese el número de cargas: "))
        charges = []
        
        for i in range(num_charges):
            print(f"\nDatos para la carga {i+1}:")
            q = get_float_input("  Valor de la carga (C): ")
            x = get_float_input("  Posición X (m): ")
            y = 0.0
            if mode == '2':
                y = get_float_input("  Posición Y (m): ")
            
            # Validar posición duplicada
            collision = False
            for existing in charges:
                if existing.x == x and existing.y == y:
                    print("Error: Dos cargas no pueden estar en la misma posición. Reintente.")
                    collision = True
                    break
            if collision:
                # Reiniciar el ingreso de cargas para este intento
                break 

            charges.append(Charge(q, x, y))
        
        if len(charges) < num_charges:
            continue

        print("\nSistema inicial cargado.")
        
        # Seleccionar carga objetivo para fuerza neta
        print("\nSeleccione la carga objetivo para calcular la fuerza neta:")
        for i in range(len(charges)):
            print(f"{i+1}. Carga {i+1} en ({charges[i].x}, {charges[i].y})")
        
        target_idx = int(get_float_input("Índice: ")) - 1
        if 0 <= target_idx < len(charges):
            target_charge = charges[target_idx]
            net_f = calculate_net_force(target_charge, charges)
            
            print(f"\n--- Resultados para la Carga {target_idx+1} ---")
            print(f"Fuerza Neta Fx: {net_f[0]:.4e} N")
            print(f"Fuerza Neta Fy: {net_f[1]:.4e} N")
            print(f"Magnitud: {np.linalg.norm(net_f):.4e} N")
            
            # Visualización de fuerza
            filename = f"assets/screenshots/fuerza_{'1d' if mode == '1' else '2d'}.png"
            if mode == '1':
                fig = plot_system_1d(charges, target_charge, net_f, filename=filename)
            else:
                fig = plot_system_2d(charges, target_charge, net_f, filename=filename)
            
            plt.close(fig) # Liberar memoria
        else:
            print("Índice inválido.")

        # Campo Eléctrico
        print("\n¿Desea calcular el campo eléctrico en un punto específico? (s/n)")
        if input().lower() == 's':
            px = get_float_input("  Posición X del punto (m): ")
            py = 0.0
            if mode == '2':
                py = get_float_input("  Posición Y del punto (m): ")
            
            e_field = calculate_electric_field_at_point((px, py), charges)
            print(f"\n--- Campo Eléctrico en ({px}, {py}) ---")
            print(f"Ex: {e_field[0]:.4e} N/C")
            print(f"Ey: {e_field[1]:.4e} N/C")
            print(f"Magnitud: {np.linalg.norm(e_field):.4e} N/C")

        # Mapa de Campo
        if mode == '2':
            print("\n¿Desea generar el mapa de campo eléctrico? (s/n)")
            if input().lower() == 's':
                filename_field = "assets/screenshots/campo_electrico.png"
                fig_field = plot_electric_field(charges, filename=filename_field)
                plt.close(fig_field)

        print("\n" + "-"*30)
        input("Presione Enter para volver al menú principal...")

if __name__ == "__main__":
    main()
