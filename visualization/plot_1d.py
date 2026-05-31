import matplotlib.pyplot as plt
import numpy as np

def plot_system_1d(charges, target_charge=None, net_force=None, filename=None):
    """
    Visualización 1D de las cargas en el eje X.
    """
    fig, ax = plt.subplots(figsize=(10, 2))
    
    x_positions = [c.x for c in charges]
    q_values = [c.q for c in charges]
    
    # Colores: rojo para positivo, azul para negativo
    colors = ['red' if q > 0 else 'blue' for q in q_values]
    
    ax.scatter(x_positions, np.zeros_like(x_positions), s=100, c=colors, zorder=5)
    
    for i, c in enumerate(charges):
        ax.annotate(f'q{i+1}: {c.q:.2e} C', (c.x, 0.05), ha='center')
    
    if target_charge and net_force is not None:
        # Dibujar vector de fuerza neta sobre la carga objetivo
        force_mag = np.linalg.norm(net_force)
        if force_mag > 0:
            direction = net_force[0] / force_mag
            ax.arrow(target_charge.x, 0, direction * 0.5, 0, 
                     head_width=0.05, head_length=0.1, fc='green', ec='green', label='Fuerza Neta')
            ax.legend()

    ax.axhline(0, color='black', lw=1, zorder=1)
    ax.set_yticks([])
    ax.set_xlabel('Posición X (m)')
    ax.set_title('Simulación 1D - Distribución de Cargas')
    plt.grid(True, axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename)
        print(f"Imagen guardada en: {filename}")
        
    return fig
