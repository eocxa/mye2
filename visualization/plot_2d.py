import matplotlib.pyplot as plt
import numpy as np

def plot_system_2d(charges, target_charge=None, net_force=None, filename=None):
    """
    Visualización 2D de las cargas y vectores de fuerza.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    x_pos = [c.x for c in charges]
    y_pos = [c.y for c in charges]
    q_val = [c.q for c in charges]
    
    colors = ['red' if q > 0 else 'blue' for q in q_val]
    
    ax.scatter(x_pos, y_pos, s=200, c=colors, edgecolors='black', zorder=5)
    
    for i, c in enumerate(charges):
        ax.annotate(f'q{i+1}\n({c.q:.1e} C)', (c.x, c.y), 
                    textcoords="offset points", xytext=(0,10), ha='center')
        
    if target_charge and net_force is not None:
        # Dibujar vector de fuerza neta
        ax.quiver(target_charge.x, target_charge.y, net_force[0], net_force[1], 
                  color='green', scale_units='xy', scale=None, label='Fuerza Neta')
        ax.legend()
        
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_title('Simulación 2D - Cargas y Fuerzas')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_aspect('equal')
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename)
        print(f"Imagen guardada en: {filename}")
        
    return fig
