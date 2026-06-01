import numpy as np
import streamlit as st

from models.charge import Charge
from physics.net_force import calculate_net_force
from physics.electric_field import calculate_electric_field_at_point
from visualization.plot_1d import plot_system_1d
from visualization.plot_2d import plot_system_2d
from visualization.plot_field import plot_electric_field

# =============================================================================
# CONFIGURACION DE PAGINA
# =============================================================================
st.set_page_config(
    page_title="Simulador de Cargas Electricas",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# INICIALIZACION DE ESTADO
# =============================================================================
if "charges_data" not in st.session_state:
    st.session_state.charges_data = [
        {"q": 1e-6, "x": -2.0, "y": 0.0},
        {"q": -1e-6, "x": 0.0, "y": 0.0},
        {"q": 1e-6, "x": 2.0, "y": 0.0},
    ]

if "selected_idx" not in st.session_state:
    st.session_state.selected_idx = 0

if "last_diagram_event_id" not in st.session_state:
    st.session_state.last_diagram_event_id = 0


DIAGRAM_HTML = """
<div class="diagram-shell">
  <svg class="diagram-svg" role="img" aria-label="Diagrama interactivo de cargas"></svg>
</div>
"""

DIAGRAM_CSS = """
.diagram-shell {
  width: 100%;
  height: 100%;
  min-height: 280px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}
.diagram-svg {
  width: 100%;
  height: 100%;
  display: block;
  touch-action: none;
  user-select: none;
  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.charge-node {
  cursor: grab;
}
.charge-node:active {
  cursor: grabbing;
}
"""

DIAGRAM_JS = """
export default function (component) {
  const { data, parentElement, setStateValue } = component
  const svg = parentElement.querySelector("svg")
  if (!svg || !data) return

  const NS = "http://www.w3.org/2000/svg"
  const width = Math.max(320, Math.floor(parentElement.clientWidth || 800))
  const height = data.height || 420
  const pad = { left: 56, right: 28, top: 34, bottom: 48 }
  const charges = Array.isArray(data.charges) ? data.charges : []
  const mode = data.mode || "2d"
  let selectedIdx = Number.isInteger(data.selected_idx) ? data.selected_idx : 0
  const force = data.force || null

  svg.setAttribute("viewBox", `0 0 ${width} ${height}`)
  svg.replaceChildren()

  const xs = charges.map(c => Number(c.x) || 0)
  const ys = charges.map(c => mode === "1d" ? 0 : (Number(c.y) || 0))
  let minX = Math.min(-5, ...xs)
  let maxX = Math.max(5, ...xs)
  let minY = mode === "1d" ? -1 : Math.min(-5, ...ys)
  let maxY = mode === "1d" ? 1 : Math.max(5, ...ys)
  const dx = Math.max(2, maxX - minX)
  const dy = Math.max(2, maxY - minY)
  minX -= dx * 0.18
  maxX += dx * 0.18
  minY -= dy * 0.18
  maxY += dy * 0.18

  const plotW = width - pad.left - pad.right
  const plotH = height - pad.top - pad.bottom
  const xToPx = x => pad.left + ((x - minX) / (maxX - minX)) * plotW
  const yToPx = y => pad.top + (1 - ((y - minY) / (maxY - minY))) * plotH
  const pxToX = px => minX + ((px - pad.left) / plotW) * (maxX - minX)
  const pxToY = py => minY + (1 - ((py - pad.top) / plotH)) * (maxY - minY)

  function el(name, attrs = {}, text = null) {
    const node = document.createElementNS(NS, name)
    for (const [key, value] of Object.entries(attrs)) {
      if (value !== null && value !== undefined) node.setAttribute(key, String(value))
    }
    if (text !== null) node.textContent = text
    svg.appendChild(node)
    return node
  }

  function line(x1, y1, x2, y2, attrs = {}) {
    return el("line", { x1, y1, x2, y2, ...attrs })
  }

  const gridColor = "#e5e7eb"
  const axisColor = "#94a3b8"
  const ticks = 8
  for (let i = 0; i <= ticks; i++) {
    const x = pad.left + (plotW * i / ticks)
    const y = pad.top + (plotH * i / ticks)
    line(x, pad.top, x, pad.top + plotH, { stroke: gridColor, "stroke-width": 1 })
    line(pad.left, y, pad.left + plotW, y, { stroke: gridColor, "stroke-width": 1 })
  }

  if (minX <= 0 && maxX >= 0) {
    line(xToPx(0), pad.top, xToPx(0), pad.top + plotH, { stroke: axisColor, "stroke-width": 1.5 })
  }
  if (minY <= 0 && maxY >= 0) {
    line(pad.left, yToPx(0), pad.left + plotW, yToPx(0), { stroke: axisColor, "stroke-width": 1.5 })
  }

  el("text", { x: width / 2, y: 22, "text-anchor": "middle", fill: "#1e293b", "font-size": 16, "font-weight": 650 }, data.title || "Diagrama interactivo")
  el("text", { x: width / 2, y: height - 12, "text-anchor": "middle", fill: "#475569", "font-size": 12 }, "X (m)")
  if (mode !== "1d") {
    el("text", { x: 16, y: height / 2, "text-anchor": "middle", fill: "#475569", "font-size": 12, transform: `rotate(-90 16 ${height / 2})` }, "Y (m)")
  }

  const defs = document.createElementNS(NS, "defs")
  defs.innerHTML = `<marker id="arrowhead" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" fill="#16a34a"></polygon></marker>`
  svg.appendChild(defs)

  if (force && charges[selectedIdx]) {
    const fx = Number(force.fx) || 0
    const fy = mode === "1d" ? 0 : (Number(force.fy) || 0)
    const mag = Math.hypot(fx, fy)
    if (mag > 1e-15) {
      const c = charges[selectedIdx]
      const x0 = xToPx(Number(c.x) || 0)
      const y0 = yToPx(mode === "1d" ? 0 : (Number(c.y) || 0))
      const arrowLen = Math.min(86, Math.max(44, plotW * 0.12))
      const x1 = x0 + (fx / mag) * arrowLen
      const y1 = y0 - (fy / mag) * arrowLen
      line(x0, y0, x1, y1, { stroke: "#16a34a", "stroke-width": 3, "marker-end": "url(#arrowhead)" })
      el("text", { x: x1 + 8, y: y1 - 8, fill: "#15803d", "font-size": 12, "font-weight": 600 }, `F = ${mag.toExponential(3)} N`)
    }
  }

  function emit(idx) {
    const positions = charges.map(c => ({
      x: Number(c.x) || 0,
      y: mode === "1d" ? 0 : (Number(c.y) || 0),
    }))
    setStateValue("positions", positions)
    setStateValue("selected", idx)
    setStateValue("event_id", Date.now())
  }

  charges.forEach((charge, idx) => {
    const x = xToPx(Number(charge.x) || 0)
    const y = yToPx(mode === "1d" ? 0 : (Number(charge.y) || 0))
    const g = document.createElementNS(NS, "g")
    g.classList.add("charge-node")
    svg.appendChild(g)

    const selected = idx === selectedIdx
    const color = Number(charge.q) >= 0 ? "#ef4444" : "#3b82f6"
    const ring = document.createElementNS(NS, "circle")
    ring.setAttribute("cx", x)
    ring.setAttribute("cy", y)
    ring.setAttribute("r", selected ? 21 : 18)
    ring.setAttribute("fill", color)
    ring.setAttribute("stroke", selected ? "#f59e0b" : "#1e293b")
    ring.setAttribute("stroke-width", selected ? 5 : 2)
    g.appendChild(ring)

    const sign = document.createElementNS(NS, "text")
    sign.setAttribute("x", x)
    sign.setAttribute("y", y + 6)
    sign.setAttribute("text-anchor", "middle")
    sign.setAttribute("fill", "#ffffff")
    sign.setAttribute("font-size", 19)
    sign.setAttribute("font-weight", 750)
    sign.textContent = Number(charge.q) >= 0 ? "+" : "-"
    g.appendChild(sign)

    const label = document.createElementNS(NS, "text")
    label.setAttribute("x", x)
    label.setAttribute("y", y - 28)
    label.setAttribute("text-anchor", "middle")
    label.setAttribute("fill", "#334155")
    label.setAttribute("font-size", 12)
    label.setAttribute("font-weight", 650)
    label.textContent = `q${idx + 1}`
    g.appendChild(label)

    function moveTo(clientX, clientY) {
      const rect = svg.getBoundingClientRect()
      const px = Math.min(pad.left + plotW, Math.max(pad.left, clientX - rect.left))
      const py = Math.min(pad.top + plotH, Math.max(pad.top, clientY - rect.top))
      charge.x = Number(pxToX(px).toFixed(3))
      charge.y = mode === "1d" ? 0 : Number(pxToY(py).toFixed(3))
      const nx = xToPx(charge.x)
      const ny = yToPx(charge.y)
      ring.setAttribute("cx", nx)
      ring.setAttribute("cy", ny)
      sign.setAttribute("x", nx)
      sign.setAttribute("y", ny + 6)
      label.setAttribute("x", nx)
      label.setAttribute("y", ny - 28)
    }

    g.addEventListener("pointerdown", e => {
      e.preventDefault()
      selectedIdx = idx
      g.setPointerCapture(e.pointerId)
      const onMove = ev => moveTo(ev.clientX, ev.clientY)
      const onUp = ev => {
        moveTo(ev.clientX, ev.clientY)
        emit(idx)
        g.releasePointerCapture(ev.pointerId)
        g.removeEventListener("pointermove", onMove)
        g.removeEventListener("pointerup", onUp)
        g.removeEventListener("pointercancel", onUp)
      }
      g.addEventListener("pointermove", onMove)
      g.addEventListener("pointerup", onUp)
      g.addEventListener("pointercancel", onUp)
    })
  })
}
"""


_CHARGE_DIAGRAM = st.components.v2.component(
    "charge_drag_diagram",
    html=DIAGRAM_HTML,
    css=DIAGRAM_CSS,
    js=DIAGRAM_JS,
)


def sync_position_widgets():
    for i, charge in enumerate(st.session_state.charges_data):
        x_key = f"sidebar_x{i}"
        y_key = f"sidebar_y{i}"
        if x_key in st.session_state:
            st.session_state[x_key] = float(charge["x"])
        if y_key in st.session_state:
            st.session_state[y_key] = float(charge["y"])

def consume_diagram_events():
    latest_event = None
    for key in ("force_diagram", "field_diagram"):
        state = st.session_state.get(key, {})
        if not isinstance(state, dict):
            continue
        event_id = state.get("event_id")
        if not isinstance(event_id, (int, float)):
            continue
        if event_id <= st.session_state.last_diagram_event_id:
            continue
        if latest_event is None or event_id > latest_event.get("event_id", 0):
            latest_event = state

    if latest_event is None:
        return

    positions = latest_event.get("positions", [])
    for i, pos in enumerate(positions):
        if i >= len(st.session_state.charges_data) or not isinstance(pos, dict):
            continue
        st.session_state.charges_data[i]["x"] = float(pos.get("x", 0.0))
        st.session_state.charges_data[i]["y"] = float(pos.get("y", 0.0))

    selected = latest_event.get("selected")
    if isinstance(selected, int) and 0 <= selected < len(st.session_state.charges_data):
        st.session_state.selected_idx = selected

    st.session_state.last_diagram_event_id = latest_event.get("event_id", 0)
    sync_position_widgets()


def render_charge_diagram(key, title, charges, mode, selected_idx, net_force=None, height=430):
    payload = {
        "title": title,
        "mode": "1d" if "1D" in mode else "2d",
        "selected_idx": int(selected_idx),
        "height": height,
        "charges": [
            {"q": float(c.q), "x": float(c.x), "y": float(c.y)}
            for c in charges
        ],
        "force": None
        if net_force is None
        else {"fx": float(net_force[0]), "fy": float(net_force[1])},
    }
    return _CHARGE_DIAGRAM(
        key=key,
        data=payload,
        width="stretch",
        height=height,
        on_positions_change=lambda: None,
        on_selected_change=lambda: None,
        on_event_id_change=lambda: None,
    )


def format_scientific(value, unit=""):
    mantissa, exponent = f"{float(value):.2e}".split("e")
    suffix = f" {unit}" if unit else ""
    return f"{mantissa} x10^{int(exponent)}{suffix}"


def split_scientific(value):
    value = float(value)
    if value == 0:
        return 0.0, 0

    exponent = int(np.floor(np.log10(abs(value))))
    coefficient = value / (10 ** exponent)
    return coefficient, exponent


consume_diagram_events()

# =============================================================================
# ESTILOS
# =============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    [data-testid="stSidebar"] {
        background-color: #0f172a;
        border-right: none;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }

    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stRadio label {
        color: #cbd5e1;
        font-weight: 600;
    }

    [data-testid="stSidebar"] .stExpander {
        background-color: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 8px;
    }

    [data-testid="stSidebar"] .stExpander:hover {
        background-color: rgba(255,255,255,0.08);
    }

    [data-testid="stSidebar"] .st-expanderContent {
        color: #e2e8f0;
    }

    [data-testid="stSidebar"] input {
        background-color: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        border-radius: 8px;
    }

    [data-testid="stSidebar"] input:focus {
        border-color: #60a5fa;
        box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.2);
    }

    [data-testid="stSidebar"] .stRadio > div {
        background-color: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 0.5rem;
    }

    [data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
        color: #e2e8f0;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 44px;
        background-color: white;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        padding: 0 1.5rem;
        font-weight: 600;
        color: #000000 !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f8fafc;
        border-color: #cbd5e1;
        color: #000000 !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #2563eb;
        color: #000000 !important;
        border-color: #2563eb;
    }

    .stTabs [data-baseweb="tab"] p,
    .stTabs [data-baseweb="tab"] span {
        color: #000000 !important;
    }

    .stMetric {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        border: 1px solid #e2e8f0;
        color: #000000;
    }

    .stMetric [data-testid="stMetricLabel"],
    .stMetric [data-testid="stMetricValue"],
    .stMetric [data-testid="stMetricDelta"],
    .stMetric label,
    .stMetric div,
    .stMetric p {
        color: #000000 !important;
    }

    .stMetric [data-testid="stMetricValue"] {
        font-size: 1.05rem;
        line-height: 1.2;
        white-space: normal;
        overflow-wrap: anywhere;
        word-break: normal;
    }

    .stMetric [data-testid="stMetricLabel"] {
        font-size: 0.82rem;
        line-height: 1.15;
        white-space: normal;
    }

    .stInfo, .stSuccess, .stWarning {
        border-radius: 8px;
    }

    .drag-hint {
        color: #64748b;
        font-size: 0.8rem;
        margin-top: 0.3rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =============================================================================
# HEADER
# =============================================================================
st.title("Simulador de Cargas Electricas")
st.caption("Arrastre las esferas rojas y azules en los graficos para modificar las posiciones")

# =============================================================================
# BARRA LATERAL
# =============================================================================
with st.sidebar:
    st.header("Configuracion")

    mode = st.radio(
        "Dimensiones",
        ["1D (Eje X)", "2D (Plano XY)"],
        key="mode",
        help="1D: solo eje X. 2D: plano completo XY.",
    )

    st.divider()
    st.subheader("Control de Cargas")

    col_add, col_del = st.columns(2)
    if col_add.button("+ Añadir"):
        new_q = 1e-6 if len(st.session_state.charges_data) % 2 == 0 else -1e-6
        st.session_state.charges_data.append({"q": new_q, "x": 0.0, "y": 1.0})
        st.session_state.selected_idx = len(st.session_state.charges_data) - 1
        st.rerun()

    if col_del.button("- Eliminar") and len(st.session_state.charges_data) > 1:
        st.session_state.charges_data.pop(st.session_state.selected_idx)
        st.session_state.selected_idx = max(0, st.session_state.selected_idx - 1)
        st.rerun()

    st.divider()
    st.subheader("Lista de Cargas")

    charges = []
    for i, c_data in enumerate(st.session_state.charges_data):
        is_selected = (i == st.session_state.selected_idx)
        label = f"Carga q{i+1}" + (" *" if is_selected else "")

        with st.expander(label, expanded=is_selected):
            q_coef, q_exp = split_scientific(c_data["q"])
            st.caption("Valor de carga (C)")
            q_col1, q_col2, q_col3 = st.columns([1.15, 0.55, 1])
            q_coef_val = q_col1.number_input(
                "Coeficiente",
                value=float(q_coef),
                step=0.1,
                format="%.2f",
                key=f"sidebar_q_coef{i}",
            )
            q_col2.markdown(
                "<div style='padding-top: 1.9rem; text-align: center; font-weight: 700;'>x10</div>",
                unsafe_allow_html=True,
            )
            q_exp_val = q_col3.number_input(
                "Exponente",
                value=int(q_exp),
                step=1,
                key=f"sidebar_q_exp{i}",
            )
            q_val = float(q_coef_val) * (10 ** int(q_exp_val))
            x_val = st.number_input(
                "X (m)",
                value=float(c_data["x"]),
                step=1.0,
                key=f"sidebar_x{i}",
            )
            y_val = 0.0
            if "2D" in mode:
                y_val = st.number_input(
                    "Y (m)",
                    value=float(c_data["y"]),
                    step=1.0,
                    key=f"sidebar_y{i}"
                )

            # Sincronizar cambios de vuelta a charges_data
            st.session_state.charges_data[i]["q"] = q_val
            st.session_state.charges_data[i]["x"] = x_val
            st.session_state.charges_data[i]["y"] = y_val

            if st.button(f"Seleccionar q{i+1}", key=f"sel_{i}"):
                st.session_state.selected_idx = i
                st.rerun()

        charges.append(Charge(
            st.session_state.charges_data[i]["q"],
            st.session_state.charges_data[i]["x"],
            st.session_state.charges_data[i]["y"]
        ))

    num_charges = len(charges)
    st.divider()
    st.caption("Simulador v3.0 - Manipulacion Mejorada")

PLOTLY_CONFIG = {"displayModeBar": True, "scrollZoom": True}
tab1, tab2, tab3 = st.tabs(
    [
        "Fuerza Neta",
        "Campo Electrico",
        "Fundamentos",
    ]
)

# --- TAB 1: FUERZA NETA ---
with tab1:
    st.header("Vector de Fuerza Resultante")
    st.info(
        "Haga clic en una carga en el grafico para seleccionarla o use el panel de abajo. "
        "Puede arrastrar cualquier carga para cambiar su posicion."
    )

    # PANEL DE CARGA SELECCIONADA
    with st.container(border=True):
        idx = st.session_state.selected_idx
        if idx >= len(st.session_state.charges_data):
            st.session_state.selected_idx = 0
            idx = 0

        c_edit = st.session_state.charges_data[idx]

        col1, col2, col3, col4 = st.columns([1.8, 1.25, 1, 1])
        col1.subheader(f"Carga seleccionada q{idx+1}")
        col2.metric("Carga", format_scientific(c_edit["q"], "C"))
        col3.metric("X", f"{float(c_edit['x']):.2f} m")
        col4.metric("Y", f"{float(c_edit['y']):.2f} m")

    target_idx = st.session_state.selected_idx
    target_charge = charges[target_idx]
    force_error = None
    try:
        net_f = calculate_net_force(target_charge, charges)
    except ValueError as exc:
        net_f = np.array([0.0, 0.0])
        force_error = str(exc)
    force_mag = np.linalg.norm(net_f)

    st.subheader("Resultados")
    if force_error:
        st.warning(
            "No se puede calcular la fuerza porque hay cargas exactamente en la misma posicion. "
            "Separe las cargas en el diagrama o en los controles."
        )
    m1, m2, m3 = st.columns(3)
    m1.metric("Componente Fx", format_scientific(net_f[0], "N"))
    m2.metric("Componente Fy", format_scientific(net_f[1], "N"))
    m3.metric("Magnitud |F|", format_scientific(force_mag, "N"))

    st.subheader("Grafico Interactivo")
    render_charge_diagram(
        key="force_diagram",
        title="Arrastre una carga para recalcular la fuerza",
        charges=charges,
        mode=mode,
        selected_idx=target_idx,
        net_force=net_f,
        height=360 if "1D" in mode else 560,
    )

    with st.expander("Ver grafico Plotly"):
        if "1D" in mode:
            fig = plot_system_1d(
                charges=charges,
                target_charge=target_charge,
                net_force=net_f,
                selected_idx=target_idx,
            )
        else:
            fig = plot_system_2d(
                charges=charges,
                target_charge=target_charge,
                net_force=net_f,
                selected_idx=target_idx,
            )
        st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG)

# --- TAB 2: CAMPO ELECTRICO ---
with tab2:
    st.header("Campo Electrico")
    st.info("Arrastre las esferas rojas/azules para mover las cargas. El campo se recalcula despues de soltar la carga.")

    col_plot, col_ctrl = st.columns([3, 1])

    with col_ctrl:
        st.markdown("**Parametros**")
        grid_res = st.select_slider(
            "Densidad de lineas",
            options=[10, 15, 20, 25, 30, 40],
            value=20,
        )

        st.divider()
        st.markdown("**Sonda puntual**")
        st.caption("Mida el campo en un punto arbitrario:")

        px = st.number_input("X (m)", value=0.0, step=1.0)
        py = 0.0
        if "2D" in mode:
            py = st.number_input("Y (m)", value=1.0, step=1.0)

        e_field = calculate_electric_field_at_point((px, py), charges)
        st.metric("Intensidad en sonda", format_scientific(np.linalg.norm(e_field), "N/C"))

        with st.expander("Componentes"):
            st.write(f"Ex = {format_scientific(e_field[0], 'N/C')}")
            st.write(f"Ey = {format_scientific(e_field[1], 'N/C')}")

    with col_plot:
        render_charge_diagram(
            key="field_diagram",
            title="Diagrama editable de cargas",
            charges=charges,
            mode=mode,
            selected_idx=st.session_state.selected_idx,
            height=300 if "1D" in mode else 360,
        )

        if "2D" in mode:
            with st.spinner("Calculando campo electrico..."):
                fig_field = plot_electric_field(
                    charges,
                    grid_size=grid_res,
                    selected_idx=st.session_state.selected_idx
                )
                st.plotly_chart(
                    fig_field, width="stretch", config=PLOTLY_CONFIG
                )
        else:
            st.warning(
                "El mapa de campo esta optimizado para 2D. "
                "Cambie a modo 2D en la barra lateral."
            )

# --- TAB 3: FUNDAMENTOS ---
with tab3:
    st.header("Fundamentos de Electrostatica")

    st.markdown("Las ecuaciones que gobiernan este simulador:")

    col_eq1, col_eq2 = st.columns(2)

    with col_eq1:
        with st.container(border=True):
            st.subheader("1. Ley de Coulomb")
            st.latex(r"F = k \frac{|q_1 q_2|}{r^2}")
            st.caption(
                "La fuerza entre dos cargas es proporcional al producto de sus magnitudes "
                "e inversamente proporcional al cuadrado de la distancia. "
                "k = 8.99e9 N m2/C2."
            )

    with col_eq2:
        with st.container(border=True):
            st.subheader("2. Principio de Superposicion")
            st.latex(r"\vec{F}_{neta} = \sum_{i} \vec{F}_i")
            st.caption(
                "La fuerza neta sobre una carga es la suma vectorial de todas "
                "las fuerzas individuales ejercidas por las demas cargas."
            )

    with st.container(border=True):
        st.subheader("3. Campo Electrico")
        st.latex(r"\vec{E} = \frac{\vec{F}}{q_0} = k \sum \frac{q_i}{r_i^2} \hat{r}_i")
        st.caption(
            "El campo electrico es la fuerza por unidad de carga de prueba. "
            "Define el espacio que rodea a las cargas."
        )
