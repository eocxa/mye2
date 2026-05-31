import matplotlib.pyplot as plt
import numpy as np
from physics.electric_field import calculate_electric_field_at_point

def plot_electric_field(charges, grid_size=20, filename=None):
    """
    Visualización del campo eléctrico mediante líneas de campo o vectores.
    """
    # Determinar límites
    x_coords = [c.x for c in charges]
    y_coords = [c.y for c in charges]
    
    margin = 1.0
    x_min, x_max = min(x_coords) - margin, max(x_coords) + margin
    y_min, y_max = min(y_coords) - margin, max(y_coords) + margin
    
    # Crear malla
    nx, ny = grid_size, grid_size
    x = np.linspace(x_min, x_max, nx)
    y = np.linspace(y_min, y_max, ny)
    X, Y = np.meshgrid(x, y)
    
    Ex = np.zeros(X.shape)
    Ey = np.zeros(Y.shape)
    
    for i in range(nx):
        for j in range(ny):
            field = calculate_electric_field_at_point((X[i,j], Y[i,j]), charges)
            Ex[i,j] = field[0]
            Ey[i,j] = field[1]
            
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Dibujar campo con streamplot (líneas de flujo)
    # Evitar log10(0)
    mag = np.sqrt(Ex**2 + Ey**2)
    color = np.log10(mag, out=np.zeros_like(mag), where=(mag!=0)) 
    
    strm = ax.streamplot(X, Y, Ex, Ey, color=color, linewidth=1, cmap='inferno',
                         density=1.5, arrowstyle='->', arrowsize=1.5)
    
    # Dibujar cargas
    x_pos = [c.x for c in charges]
    y_pos = [c.y for c in charges]
    q_val = [c.q for c in charges]
    colors = ['red' if q > 0 else 'blue' for q in q_val]
    ax.scatter(x_pos, y_pos, s=150, c=colors, edgecolors='white', zorder=10)
    
    fig.colorbar(strm.lines, label='Log10(Intensidad del Campo E)')
    ax.set_title('Mapa de Campo Eléctrico')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_aspect('equal')
    
    plt.tight_layout()
    
    if filename:
        plt.savefig(filename)
        print(f"Imagen guardada en: {filename}")
        
    return fig
