import plotly.graph_objects as go
import numpy as np


def plot_system_2d(charges, target_charge=None, net_force=None, selected_idx=None):
    """Grafico 2D interactivo (Plotly)."""
    fig = go.Figure()

    x_pos = [c.x for c in charges]
    y_pos = [c.y for c in charges]
    q_val = [c.q for c in charges]

    colors = ['#ef4444' if q > 0 else '#3b82f6' for q in q_val]
    
    # Estilos de línea para los marcadores (resaltado si está seleccionado)
    line_colors = []
    line_widths = []
    for i in range(len(charges)):
        if selected_idx is not None and i == selected_idx:
            line_colors.append('#fbbf24')  # Dorado (Amber 400)
            line_widths.append(5)
        else:
            line_colors.append('#1e293b')  # Slate 800
            line_widths.append(2)

    fig.add_trace(go.Scatter(
        x=x_pos,
        y=y_pos,
        mode='markers+text',
        marker=dict(
            size=30,
            color=colors,
            line=dict(color=line_colors, width=line_widths),
        ),
        text=[f'q{i+1}' for i in range(len(x_pos))],
        textposition='top center',
        textfont=dict(size=12, color='#334155'),
        hovertemplate=(
            '<b>q%{text}</b><br>'
            'Carga: %{customdata[0]:.2e} C<br>'
            'X = %{x:.2f} m<br>'
            'Y = %{y:.2f} m'
            '<extra></extra>'
        ),
        customdata=[[q] for q in q_val],
        name='Cargas'
    ))

    if target_charge and net_force is not None:
        force_mag = float(np.linalg.norm(net_force))
        if force_mag > 1e-15:
            fx, fy = float(net_force[0]), float(net_force[1])
            x0, y0 = float(target_charge.x), float(target_charge.y)
            scale = 0.6
            nx, ny = fx / force_mag * scale, fy / force_mag * scale
            x1, y1 = x0 + nx, y0 + ny
            fig.add_annotation(
                x=x1, y=y1,
                ax=x0, ay=y0,
                xref='x', yref='y',
                axref='x', ayref='y',
                showarrow=True,
                arrowhead=3,
                arrowsize=1.8,
                arrowwidth=3,
                arrowcolor='#16a34a',
                font=dict(color='#16a34a', size=12),
            )
            fig.add_annotation(
                x=x1 + 0.08, y=y1 + 0.08,
                text=f'F = {force_mag:.3e} N',
                showarrow=False,
                font=dict(color='#16a34a', size=11),
            )

    # Limites con margen
    if x_pos and y_pos:
        margin_x = max(2.0, (max(x_pos) - min(x_pos)) * 0.3)
        margin_y = max(2.0, (max(y_pos) - min(y_pos)) * 0.3)
        x_range = [min(x_pos) - margin_x, max(x_pos) + margin_x]
        y_range = [min(y_pos) - margin_y, max(y_pos) + margin_y]
    else:
        x_range = [-5, 5]
        y_range = [-5, 5]

    fig.update_xaxes(range=x_range)
    fig.update_yaxes(range=y_range)

    fig.update_layout(
        title=dict(
            text='Visualizacion 2D',
            font=dict(size=16, color='#1e293b'),
        ),
        xaxis=dict(
            title='X (m)',
            showgrid=True,
            gridcolor='#e5e7eb',
            zeroline=True,
            zerolinecolor='#94a3b8',
            zerolinewidth=1.5,
            scaleanchor='y',
            scaleratio=1,
        ),
        yaxis=dict(
            title='Y (m)',
            showgrid=True,
            gridcolor='#e5e7eb',
            zeroline=True,
            zerolinecolor='#94a3b8',
            zerolinewidth=1.5,
        ),
        showlegend=False,
        hovermode='closest',
        plot_bgcolor='white',
        margin=dict(l=60, r=20, t=50, b=60),
        height=600,
    )

    return fig


# ---------------------------------------------------------------------------
# Version matplotlib para CLI (main.py)
# ---------------------------------------------------------------------------
import matplotlib.pyplot as plt


def plot_system_2d_mpl(charges, target_charge=None, net_force=None, filename=None):
    """Visualizacion 2D de las cargas y vectores de fuerza (matplotlib)."""
    fig, ax = plt.subplots(figsize=(8, 8))

    x_pos = [c.x for c in charges]
    y_pos = [c.y for c in charges]
    q_val = [c.q for c in charges]

    colors = ['red' if q > 0 else 'blue' for q in q_val]

    ax.scatter(x_pos, y_pos, s=200, c=colors, edgecolors='black', zorder=5)

    for i, c in enumerate(charges):
        ax.annotate(f'q{i+1}\n({c.q:.1e} C)', (c.x, c.y),
                    textcoords="offset points", xytext=(0, 10), ha='center')

    if target_charge and net_force is not None:
        ax.quiver(target_charge.x, target_charge.y, net_force[0], net_force[1],
                  color='green', scale_units='xy', scale=None, label='Fuerza Neta')
        ax.legend()

    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_title('Simulacion 2D - Cargas y Fuerzas')
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_aspect('equal')
    plt.tight_layout()

    if filename:
        plt.savefig(filename)
        print(f"Imagen guardada en: {filename}")

    return fig
