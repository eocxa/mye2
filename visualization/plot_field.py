import plotly.graph_objects as go
import numpy as np
from physics.electric_field import calculate_electric_field_at_point

def plot_electric_field(charges, grid_size=20, selected_idx=None):
    x_coords = [c.x for c in charges]
    y_coords = [c.y for c in charges]
    margin = 1.5
    x_min, x_max = (min(x_coords) - margin, max(x_coords) + margin)
    y_min, y_max = (min(y_coords) - margin, max(y_coords) + margin)
    nx = ny = grid_size
    X = np.linspace(x_min, x_max, nx)
    Y = np.linspace(y_min, y_max, ny)
    X_mesh, Y_mesh = np.meshgrid(X, Y)
    Ex = np.zeros((nx, ny))
    Ey = np.zeros((nx, ny))
    for i in range(nx):
        for j in range(ny):
            field = calculate_electric_field_at_point((float(X_mesh[i, j]), float(Y_mesh[i, j])), charges)
            Ex[i, j] = field[0]
            Ey[i, j] = field[1]
    mag = np.sqrt(Ex ** 2 + Ey ** 2)
    cell_dx = (x_max - x_min) / nx
    cell_dy = (y_max - y_min) / ny
    arrow_scale = 0.4 * min(cell_dx, cell_dy)
    line_x = []
    line_y = []
    for i in range(nx):
        for j in range(ny):
            m = mag[i, j]
            if m > 1e-15:
                ex_n = Ex[i, j] / m
                ey_n = Ey[i, j] / m
                x0 = float(X_mesh[i, j]) - ex_n * arrow_scale
                y0 = float(Y_mesh[i, j]) - ey_n * arrow_scale
                x1 = float(X_mesh[i, j]) + ex_n * arrow_scale
                y1 = float(Y_mesh[i, j]) + ey_n * arrow_scale
                line_x.extend([x0, x1, None])
                line_y.extend([y0, y1, None])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=line_x, y=line_y, mode='lines', line=dict(color='#64748b', width=1.0), showlegend=False, hoverinfo='skip', name='Campo E'))
    x_pos = [c.x for c in charges]
    y_pos = [c.y for c in charges]
    q_val = [c.q for c in charges]
    colors = ['#ef4444' if q > 0 else '#3b82f6' for q in q_val]
    line_colors = []
    line_widths = []
    for i in range(len(charges)):
        if selected_idx is not None and i == selected_idx:
            line_colors.append('#fbbf24')
            line_widths.append(5)
        else:
            line_colors.append('white')
            line_widths.append(2)
    fig.add_trace(go.Scatter(x=x_pos, y=y_pos, mode='markers+text', marker=dict(size=30, color=colors, line=dict(color=line_colors, width=line_widths)), text=[f'q{i + 1}' for i in range(len(x_pos))], textposition='top center', textfont=dict(size=13, color='#1e293b'), hovertemplate='<b>q%{text}</b><br>Carga: %{customdata[0]:.2e} C<br>X = %{x:.2f} m<br>Y = %{y:.2f} m<extra></extra>', customdata=[[q] for q in q_val], name='Cargas'))
    fig.update_layout(title=dict(text='Mapa de Campo Electrico', font=dict(size=16, color='#1e293b')), xaxis=dict(title='X (m)', range=[x_min, x_max], showgrid=True, gridcolor='#e5e7eb', zeroline=True, zerolinecolor='#94a3b8', zerolinewidth=1.5, scaleanchor='y', scaleratio=1), yaxis=dict(title='Y (m)', range=[y_min, y_max], showgrid=True, gridcolor='#e5e7eb', zeroline=True, zerolinecolor='#94a3b8', zerolinewidth=1.5), showlegend=False, hovermode='closest', plot_bgcolor='white', margin=dict(l=60, r=20, t=50, b=60), height=600)
    return fig
import matplotlib.pyplot as plt

def plot_electric_field_mpl(charges, grid_size=20, filename=None):
    x_coords = [c.x for c in charges]
    y_coords = [c.y for c in charges]
    margin = 1.0
    x_min, x_max = (min(x_coords) - margin, max(x_coords) + margin)
    y_min, y_max = (min(y_coords) - margin, max(y_coords) + margin)
    nx, ny = (grid_size, grid_size)
    x = np.linspace(x_min, x_max, nx)
    y = np.linspace(y_min, y_max, ny)
    X, Y = np.meshgrid(x, y)
    Ex = np.zeros(X.shape)
    Ey = np.zeros(Y.shape)
    for i in range(nx):
        for j in range(ny):
            field = calculate_electric_field_at_point((X[i, j], Y[i, j]), charges)
            Ex[i, j] = field[0]
            Ey[i, j] = field[1]
    fig, ax = plt.subplots(figsize=(10, 8))
    mag = np.sqrt(Ex ** 2 + Ey ** 2)
    color = np.log10(mag, out=np.zeros_like(mag), where=mag != 0)
    strm = ax.streamplot(X, Y, Ex, Ey, color=color, linewidth=1, cmap='inferno', density=1.5, arrowstyle='->', arrowsize=1.5)
    x_pos = [c.x for c in charges]
    y_pos = [c.y for c in charges]
    q_val = [c.q for c in charges]
    colors = ['red' if q > 0 else 'blue' for q in q_val]
    ax.scatter(x_pos, y_pos, s=150, c=colors, edgecolors='white', zorder=10)
    fig.colorbar(strm.lines, label='Log10(Intensidad del Campo E)')
    ax.set_title('Mapa de Campo Electrico')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_aspect('equal')
    plt.tight_layout()
    if filename:
        plt.savefig(filename)
        print(f'Imagen guardada en: {filename}')
    return fig