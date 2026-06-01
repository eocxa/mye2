import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt

def plot_system_1d(charges, target_charge=None, net_force=None, selected_idx=None):
    """Grafico 1D interactivo (Plotly)."""
    fig = go.Figure()

    x_positions = [c.x for c in charges]
    q_values = [c.q for c in charges]

    colors = ['#ef4444' if q > 0 else '#3b82f6' for q in q_values]

    # Estilos de línea para los marcadores (resaltado si está seleccionado)
    line_colors = []
    line_widths = []
    for i in range(len(charges)):
        if selected_idx is not None and i == selected_idx:
            line_colors.append('#fbbf24')  # Dorado
            line_widths.append(5)
        else:
            line_colors.append('#1e293b')  # Slate
            line_widths.append(2)

    fig.add_trace(go.Scatter(
        x=x_positions,
        y=[0] * len(x_positions),
        mode='markers+text',
        marker=dict(
            size=35,
            color=colors,
            line=dict(color=line_colors, width=line_widths),
        ),
        text=[f'q{i+1}: {q:.2e} C' for i, q in enumerate(q_values)],
        textposition='top center',
        textfont=dict(size=11, color='#334155'),
        hovertemplate=(
            '<b>%{text}</b><br>'
            'X = %{x:.2f} m'
            '<extra></extra>'
        ),
        name='Cargas'
    ))

    if target_charge and net_force is not None:
        force_mag = float(np.linalg.norm(net_force))
        if force_mag > 1e-15:
            fx, fy = float(net_force[0]), float(net_force[1])
            scale = 0.6
            x0, y0 = float(target_charge.x), 0.0
            x1 = x0 + (fx / force_mag) * scale
            fig.add_annotation(
                x=x1, y=0,
                ax=x0, ay=0,
                xref='x', yref='y',
                axref='x', ayref='y',
                showarrow=True,
                arrowhead=3,
                arrowsize=1.8,
                arrowwidth=3,
                arrowcolor='#16a34a',
                font=dict(color='#16a34a', size=12, family='Inter'),
            )
            fig.add_annotation(
                x=x1 + 0.05, y=0.02,
                text=f'F = {force_mag:.3e} N',
                showarrow=False,
                font=dict(color='#16a34a', size=11),
            )

    fig.update_layout(
        title=dict(
            text='Visualizacion 1D',
            font=dict(size=16, color='#1e293b'),
        ),
        xaxis=dict(
            title='X (m)',
            showgrid=True,
            gridcolor='#e5e7eb',
            zeroline=True,
            zerolinecolor='#94a3b8',
            zerolinewidth=1.5,
        ),
        yaxis=dict(
            visible=False,
            range=[-0.6, 0.8],
        ),
        showlegend=False,
        hovermode='closest',
        plot_bgcolor='white',
        margin=dict(l=40, r=40, t=50, b=50),
        height=300,
    )

    return fig

def plot_system_1d_mpl(charges, target_charge=None, net_force=None, filename=None):
    """Visualizacion 1D de las cargas en el eje X (matplotlib)."""
    fig, ax = plt.subplots(figsize=(10, 2))

    x_positions = [c.x for c in charges]
    q_values = [c.q for c in charges]

    colors = ['red' if q > 0 else 'blue' for q in q_values]

    ax.scatter(x_positions, np.zeros_like(x_positions), s=100, c=colors, zorder=5)

    for i, c in enumerate(charges):
        ax.annotate(f'q{i+1}: {c.q:.2e} C', (c.x, 0.05), ha='center')

    if target_charge and net_force is not None:
        force_mag = np.linalg.norm(net_force)
        if force_mag > 0:
            direction = net_force[0] / force_mag
            ax.arrow(target_charge.x, 0, direction * 0.5, 0,
                     head_width=0.05, head_length=0.1, fc='green', ec='green',
                     label='Fuerza Neta')
            ax.legend()

    ax.axhline(0, color='black', lw=1, zorder=1)
    ax.set_yticks([])
    ax.set_xlabel('Posicion X (m)')
    ax.set_title('Simulacion 1D - Distribucion de Cargas')
    plt.grid(True, axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()

    if filename:
        plt.savefig(filename)

    return fig
