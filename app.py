import numpy as np
import streamlit as st
from models.charge import Charge
from physics.net_force import calculate_net_force
from physics.electric_field import calculate_electric_field_at_point
from visualization.plot_1d import plot_system_1d
from visualization.plot_2d import plot_system_2d
from visualization.plot_field import plot_electric_field
st.set_page_config(page_title='Simulador de Cargas Electricas', layout='wide', initial_sidebar_state='expanded')
if 'charges_data' not in st.session_state:
    st.session_state.charges_data = [{'q': 1e-06, 'x': -2.0, 'y': 0.0}, {'q': -1e-06, 'x': 0.0, 'y': 0.0}, {'q': 1e-06, 'x': 2.0, 'y': 0.0}]
if 'selected_idx' not in st.session_state:
    st.session_state.selected_idx = 0
if 'last_diagram_event_id' not in st.session_state:
    st.session_state.last_diagram_event_id = 0
DIAGRAM_HTML = '\n<div class="diagram-shell">\n  <svg class="diagram-svg" role="img" aria-label="Diagrama interactivo de cargas"></svg>\n</div>\n'
DIAGRAM_CSS = '\n.diagram-shell {\n  width: 100%;\n  height: 100%;\n  min-height: 280px;\n  background: #ffffff;\n  border: 1px solid #e2e8f0;\n  border-radius: 8px;\n  overflow: hidden;\n}\n.diagram-svg {\n  width: 100%;\n  height: 100%;\n  display: block;\n  touch-action: none;\n  user-select: none;\n  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;\n}\n.charge-node {\n  cursor: grab;\n}\n.charge-node:active {\n  cursor: grabbing;\n}\n'
DIAGRAM_JS = '\nexport default function (component) {\n  const { data, parentElement, setStateValue } = component\n  const svg = parentElement.querySelector("svg")\n  if (!svg || !data) return\n\n  const NS = "http://www.w3.org/2000/svg"\n  const width = Math.max(320, Math.floor(parentElement.clientWidth || 800))\n  const height = data.height || 420\n  const pad = { left: 56, right: 28, top: 34, bottom: 48 }\n  const charges = Array.isArray(data.charges) ? data.charges : []\n  const mode = data.mode || "2d"\n  let selectedIdx = Number.isInteger(data.selected_idx) ? data.selected_idx : 0\n  const force = data.force || null\n\n  svg.setAttribute("viewBox", `0 0 ${width} ${height}`)\n  svg.replaceChildren()\n\n  const xs = charges.map(c => Number(c.x) || 0)\n  const ys = charges.map(c => mode === "1d" ? 0 : (Number(c.y) || 0))\n  let minX = Math.min(-5, ...xs)\n  let maxX = Math.max(5, ...xs)\n  let minY = mode === "1d" ? -1 : Math.min(-5, ...ys)\n  let maxY = mode === "1d" ? 1 : Math.max(5, ...ys)\n  const dx = Math.max(2, maxX - minX)\n  const dy = Math.max(2, maxY - minY)\n  minX -= dx * 0.18\n  maxX += dx * 0.18\n  minY -= dy * 0.18\n  maxY += dy * 0.18\n\n  const plotW = width - pad.left - pad.right\n  const plotH = height - pad.top - pad.bottom\n  const xToPx = x => pad.left + ((x - minX) / (maxX - minX)) * plotW\n  const yToPx = y => pad.top + (1 - ((y - minY) / (maxY - minY))) * plotH\n  const pxToX = px => minX + ((px - pad.left) / plotW) * (maxX - minX)\n  const pxToY = py => minY + (1 - ((py - pad.top) / plotH)) * (maxY - minY)\n\n  function el(name, attrs = {}, text = null) {\n    const node = document.createElementNS(NS, name)\n    for (const [key, value] of Object.entries(attrs)) {\n      if (value !== null && value !== undefined) node.setAttribute(key, String(value))\n    }\n    if (text !== null) node.textContent = text\n    svg.appendChild(node)\n    return node\n  }\n\n  function line(x1, y1, x2, y2, attrs = {}) {\n    return el("line", { x1, y1, x2, y2, ...attrs })\n  }\n\n  const gridColor = "#e5e7eb"\n  const axisColor = "#94a3b8"\n  const ticks = 8\n  for (let i = 0; i <= ticks; i++) {\n    const x = pad.left + (plotW * i / ticks)\n    const y = pad.top + (plotH * i / ticks)\n    line(x, pad.top, x, pad.top + plotH, { stroke: gridColor, "stroke-width": 1 })\n    line(pad.left, y, pad.left + plotW, y, { stroke: gridColor, "stroke-width": 1 })\n  }\n\n  if (minX <= 0 && maxX >= 0) {\n    line(xToPx(0), pad.top, xToPx(0), pad.top + plotH, { stroke: axisColor, "stroke-width": 1.5 })\n  }\n  if (minY <= 0 && maxY >= 0) {\n    line(pad.left, yToPx(0), pad.left + plotW, yToPx(0), { stroke: axisColor, "stroke-width": 1.5 })\n  }\n\n  el("text", { x: width / 2, y: 22, "text-anchor": "middle", fill: "#1e293b", "font-size": 16, "font-weight": 650 }, data.title || "Diagrama interactivo")\n  el("text", { x: width / 2, y: height - 12, "text-anchor": "middle", fill: "#475569", "font-size": 12 }, "X (m)")\n  if (mode !== "1d") {\n    el("text", { x: 16, y: height / 2, "text-anchor": "middle", fill: "#475569", "font-size": 12, transform: `rotate(-90 16 ${height / 2})` }, "Y (m)")\n  }\n\n  const defs = document.createElementNS(NS, "defs")\n  defs.innerHTML = `<marker id="arrowhead" markerWidth="9" markerHeight="7" refX="8" refY="3.5" orient="auto"><polygon points="0 0, 9 3.5, 0 7" fill="#16a34a"></polygon></marker>`\n  svg.appendChild(defs)\n\n  if (force && charges[selectedIdx]) {\n    const fx = Number(force.fx) || 0\n    const fy = mode === "1d" ? 0 : (Number(force.fy) || 0)\n    const mag = Math.hypot(fx, fy)\n    if (mag > 1e-15) {\n      const c = charges[selectedIdx]\n      const x0 = xToPx(Number(c.x) || 0)\n      const y0 = yToPx(mode === "1d" ? 0 : (Number(c.y) || 0))\n      const arrowLen = Math.min(86, Math.max(44, plotW * 0.12))\n      const x1 = x0 + (fx / mag) * arrowLen\n      const y1 = y0 - (fy / mag) * arrowLen\n      line(x0, y0, x1, y1, { stroke: "#16a34a", "stroke-width": 3, "marker-end": "url(#arrowhead)" })\n      el("text", { x: x1 + 8, y: y1 - 8, fill: "#15803d", "font-size": 12, "font-weight": 600 }, `F = ${mag.toExponential(3)} N`)\n    }\n  }\n\n  function emit(idx) {\n    const positions = charges.map(c => ({\n      x: Number(c.x) || 0,\n      y: mode === "1d" ? 0 : (Number(c.y) || 0),\n    }))\n    setStateValue("positions", positions)\n    setStateValue("selected", idx)\n    setStateValue("event_id", Date.now())\n  }\n\n  charges.forEach((charge, idx) => {\n    const x = xToPx(Number(charge.x) || 0)\n    const y = yToPx(mode === "1d" ? 0 : (Number(charge.y) || 0))\n    const g = document.createElementNS(NS, "g")\n    g.classList.add("charge-node")\n    svg.appendChild(g)\n\n    const selected = idx === selectedIdx\n    const color = Number(charge.q) >= 0 ? "#ef4444" : "#3b82f6"\n    const ring = document.createElementNS(NS, "circle")\n    ring.setAttribute("cx", x)\n    ring.setAttribute("cy", y)\n    ring.setAttribute("r", selected ? 21 : 18)\n    ring.setAttribute("fill", color)\n    ring.setAttribute("stroke", selected ? "#f59e0b" : "#1e293b")\n    ring.setAttribute("stroke-width", selected ? 5 : 2)\n    g.appendChild(ring)\n\n    const sign = document.createElementNS(NS, "text")\n    sign.setAttribute("x", x)\n    sign.setAttribute("y", y + 6)\n    sign.setAttribute("text-anchor", "middle")\n    sign.setAttribute("fill", "#ffffff")\n    sign.setAttribute("font-size", 19)\n    sign.setAttribute("font-weight", 750)\n    sign.textContent = Number(charge.q) >= 0 ? "+" : "-"\n    g.appendChild(sign)\n\n    const label = document.createElementNS(NS, "text")\n    label.setAttribute("x", x)\n    label.setAttribute("y", y - 28)\n    label.setAttribute("text-anchor", "middle")\n    label.setAttribute("fill", "#334155")\n    label.setAttribute("font-size", 12)\n    label.setAttribute("font-weight", 650)\n    label.textContent = `q${idx + 1}`\n    g.appendChild(label)\n\n    function moveTo(clientX, clientY) {\n      const rect = svg.getBoundingClientRect()\n      const px = Math.min(pad.left + plotW, Math.max(pad.left, clientX - rect.left))\n      const py = Math.min(pad.top + plotH, Math.max(pad.top, clientY - rect.top))\n      charge.x = Number(pxToX(px).toFixed(3))\n      charge.y = mode === "1d" ? 0 : Number(pxToY(py).toFixed(3))\n      const nx = xToPx(charge.x)\n      const ny = yToPx(charge.y)\n      ring.setAttribute("cx", nx)\n      ring.setAttribute("cy", ny)\n      sign.setAttribute("x", nx)\n      sign.setAttribute("y", ny + 6)\n      label.setAttribute("x", nx)\n      label.setAttribute("y", ny - 28)\n    }\n\n    g.addEventListener("pointerdown", e => {\n      e.preventDefault()\n      selectedIdx = idx\n      g.setPointerCapture(e.pointerId)\n      let moved = false\n      const onMove = ev => { moved = true; moveTo(ev.clientX, ev.clientY) }\n      const onUp = ev => {\n        if (moved) { moveTo(ev.clientX, ev.clientY) }\n        emit(idx)\n        g.releasePointerCapture(ev.pointerId)\n        g.removeEventListener("pointermove", onMove)\n        g.removeEventListener("pointerup", onUp)\n        g.removeEventListener("pointercancel", onUp)\n      }\n      g.addEventListener("pointermove", onMove)\n      g.addEventListener("pointerup", onUp)\n      g.addEventListener("pointercancel", onUp)\n    })\n  })\n}\n'
_CHARGE_DIAGRAM = st.components.v2.component('charge_drag_diagram', html=DIAGRAM_HTML, css=DIAGRAM_CSS, js=DIAGRAM_JS)

def sync_position_widgets():
    for i, charge in enumerate(st.session_state.charges_data):
        x_key = f'sidebar_x{i}'
        y_key = f'sidebar_y{i}'
        if x_key in st.session_state:
            st.session_state[x_key] = float(charge['x'])
        if y_key in st.session_state:
            st.session_state[y_key] = float(charge['y'])

def consume_diagram_events():
    latest_event = None
    for key in ('force_diagram', 'field_diagram'):
        state = st.session_state.get(key, {})
        if not isinstance(state, dict):
            continue
        event_id = state.get('event_id')
        if not isinstance(event_id, (int, float)):
            continue
        if event_id <= st.session_state.last_diagram_event_id:
            continue
        if latest_event is None or event_id > latest_event.get('event_id', 0):
            latest_event = state
    if latest_event is None:
        return
    positions = latest_event.get('positions', [])
    for i, pos in enumerate(positions):
        if i >= len(st.session_state.charges_data) or not isinstance(pos, dict):
            continue
        st.session_state.charges_data[i]['x'] = float(pos.get('x', 0.0))
        st.session_state.charges_data[i]['y'] = float(pos.get('y', 0.0))
    selected = latest_event.get('selected')
    if isinstance(selected, int) and 0 <= selected < len(st.session_state.charges_data):
        st.session_state.selected_idx = selected
    st.session_state.last_diagram_event_id = latest_event.get('event_id', 0)
    sync_position_widgets()

def render_charge_diagram(key, title, charges, mode, selected_idx, net_force=None, height=430):
    payload = {'title': title, 'mode': '1d' if '1D' in mode else '2d', 'selected_idx': int(selected_idx), 'height': height, 'charges': [{'q': float(c.q), 'x': float(c.x), 'y': float(c.y)} for c in charges], 'force': None if net_force is None else {'fx': float(net_force[0]), 'fy': float(net_force[1])}}
    return _CHARGE_DIAGRAM(key=key, data=payload, width='stretch', height=height, on_positions_change=lambda: None, on_selected_change=lambda: None, on_event_id_change=lambda: None)

def format_scientific(value, unit=''):
    mantissa, exponent = f'{float(value):.2e}'.split('e')
    suffix = f' {unit}' if unit else ''
    return f'{mantissa} x10^{int(exponent)}{suffix}'

def split_scientific(value):
    value = float(value)
    if value == 0:
        return (0.0, 0)
    exponent = int(np.floor(np.log10(abs(value))))
    coefficient = value / 10 ** exponent
    return (coefficient, exponent)
consume_diagram_events()
st.markdown('\n    <style>\n    @import url(\'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap\');\n\n    html, body, [class*="css"] {\n        font-family: \'Inter\', sans-serif;\n    }\n\n    .block-container {\n        padding-top: 2rem;\n        padding-bottom: 2rem;\n        max-width: 1400px;\n    }\n\n    [data-testid="stSidebar"] {\n        background-color: #0f172a;\n        border-right: none;\n    }\n\n    [data-testid="stSidebar"] .block-container {\n        padding-top: 2rem;\n        padding-bottom: 2rem;\n    }\n\n    [data-testid="stSidebar"] h1,\n    [data-testid="stSidebar"] h2,\n    [data-testid="stSidebar"] h3,\n    [data-testid="stSidebar"] .stMarkdown {\n        color: white;\n    }\n\n    [data-testid="stSidebar"] .stSlider label,\n    [data-testid="stSidebar"] .stRadio label {\n        color: #cbd5e1;\n        font-weight: 600;\n    }\n\n    [data-testid="stSidebar"] .stExpander {\n        background-color: rgba(255,255,255,0.05);\n        border: 1px solid rgba(255,255,255,0.1);\n        border-radius: 8px;\n    }\n\n    [data-testid="stSidebar"] .stExpander:hover {\n        background-color: rgba(255,255,255,0.08);\n    }\n\n    [data-testid="stSidebar"] .st-expanderContent {\n        color: #e2e8f0;\n    }\n\n    [data-testid="stSidebar"] input {\n        background-color: rgba(255,255,255,0.1);\n        border: 1px solid rgba(255,255,255,0.2);\n        color: white;\n        border-radius: 8px;\n    }\n\n    [data-testid="stSidebar"] input:focus {\n        border-color: #60a5fa;\n        box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.2);\n    }\n\n    [data-testid="stSidebar"] .stRadio > div {\n        background-color: rgba(255,255,255,0.05);\n        border-radius: 8px;\n        padding: 0.5rem;\n    }\n\n    [data-testid="stSidebar"] .stRadio [role="radiogroup"] label {\n        color: #e2e8f0;\n    }\n\n    .stTabs [data-baseweb="tab-list"] {\n        gap: 4px;\n    }\n\n    .stTabs [data-baseweb="tab"] {\n        height: 44px;\n        background-color: white;\n        border-radius: 10px;\n        border: 1px solid #e2e8f0;\n        padding: 0 1.5rem;\n        font-weight: 600;\n        color: #000000 !important;\n    }\n\n    .stTabs [data-baseweb="tab"]:hover {\n        background-color: #f8fafc;\n        border-color: #cbd5e1;\n        color: #000000 !important;\n    }\n\n    .stTabs [aria-selected="true"] {\n        background-color: #2563eb;\n        color: #000000 !important;\n        border-color: #2563eb;\n    }\n\n    .stTabs [data-baseweb="tab"] p,\n    .stTabs [data-baseweb="tab"] span {\n        color: #000000 !important;\n    }\n\n    .stMetric {\n        background-color: white;\n        border-radius: 8px;\n        padding: 1rem;\n        border: 1px solid #e2e8f0;\n        color: #000000;\n    }\n\n    .stMetric [data-testid="stMetricLabel"],\n    .stMetric [data-testid="stMetricValue"],\n    .stMetric [data-testid="stMetricDelta"],\n    .stMetric label,\n    .stMetric div,\n    .stMetric p {\n        color: #000000 !important;\n    }\n\n    .stMetric [data-testid="stMetricValue"] {\n        font-size: 1.05rem;\n        line-height: 1.2;\n        white-space: normal;\n        overflow-wrap: anywhere;\n        word-break: normal;\n    }\n\n    .stMetric [data-testid="stMetricLabel"] {\n        font-size: 0.82rem;\n        line-height: 1.15;\n        white-space: normal;\n    }\n\n    .stInfo, .stSuccess, .stWarning {\n        border-radius: 8px;\n    }\n\n    .drag-hint {\n        color: #64748b;\n        font-size: 0.8rem;\n        margin-top: 0.3rem;\n    }\n    </style>\n    ', unsafe_allow_html=True)
st.title('Simulador de Cargas Electricas')
st.caption('Arrastre las esferas rojas y azules en los graficos para modificar las posiciones')
with st.sidebar:
    st.header('Configuracion')
    mode = st.radio('Dimensiones', ['1D (Eje X)', '2D (Plano XY)'], key='mode', help='1D: solo eje X. 2D: plano completo XY.')
    st.divider()
    st.subheader('Control de Cargas')
    col_add, col_del = st.columns(2)
    if col_add.button('+ Añadir'):
        new_q = 1e-06 if len(st.session_state.charges_data) % 2 == 0 else -1e-06
        st.session_state.charges_data.append({'q': new_q, 'x': 0.0, 'y': 1.0})
        st.session_state.selected_idx = len(st.session_state.charges_data) - 1
        st.rerun()
    if col_del.button('- Eliminar') and len(st.session_state.charges_data) > 1:
        st.session_state.charges_data.pop(st.session_state.selected_idx)
        st.session_state.selected_idx = max(0, st.session_state.selected_idx - 1)
        st.rerun()
    st.divider()
    st.subheader('Lista de Cargas')
    charges = []
    for i, c_data in enumerate(st.session_state.charges_data):
        is_selected = i == st.session_state.selected_idx
        label = f'Carga q{i + 1}' + (' *' if is_selected else '')
        with st.expander(label, expanded=is_selected):
            q_coef, q_exp = split_scientific(c_data['q'])
            st.caption('Valor de carga (C)')
            q_col1, q_col2, q_col3 = st.columns([1.15, 0.55, 1])
            q_coef_val = q_col1.number_input('Coeficiente', value=float(q_coef), step=0.1, format='%.2f', key=f'sidebar_q_coef{i}')
            q_col2.markdown("<div style='padding-top: 1.9rem; text-align: center; font-weight: 700;'>x10</div>", unsafe_allow_html=True)
            q_exp_val = q_col3.number_input('Exponente', value=int(q_exp), step=1, key=f'sidebar_q_exp{i}')
            q_val = float(q_coef_val) * 10 ** int(q_exp_val)
            x_val = st.number_input('X (m)', value=float(c_data['x']), step=1.0, key=f'sidebar_x{i}')
            y_val = 0.0
            if '2D' in mode:
                y_val = st.number_input('Y (m)', value=float(c_data['y']), step=1.0, key=f'sidebar_y{i}')
            st.session_state.charges_data[i]['q'] = q_val
            st.session_state.charges_data[i]['x'] = x_val
            st.session_state.charges_data[i]['y'] = y_val
            if st.button(f'Seleccionar q{i + 1}', key=f'sel_{i}'):
                st.session_state.selected_idx = i
                st.rerun()
        charges.append(Charge(st.session_state.charges_data[i]['q'], st.session_state.charges_data[i]['x'], st.session_state.charges_data[i]['y']))
    num_charges = len(charges)
    st.divider()
    st.caption('Simulador v3.0 - Manipulacion Mejorada')
PLOTLY_CONFIG = {'displayModeBar': True, 'scrollZoom': True}
tab1, tab2, tab3 = st.tabs(['Fuerza Neta', 'Campo Electrico', 'Fundamentos'])
with tab1:
    st.header('Vector de Fuerza Resultante')
    st.info('Haga clic en una carga en el grafico para seleccionarla o use el panel de abajo. Puede arrastrar cualquier carga para cambiar su posicion.')
    with st.container(border=True):
        idx = st.session_state.selected_idx
        if idx >= len(st.session_state.charges_data):
            st.session_state.selected_idx = 0
            idx = 0
        c_edit = st.session_state.charges_data[idx]
        col1, col2, col3, col4 = st.columns([1.8, 1.25, 1, 1])
        col1.subheader(f'Carga seleccionada q{idx + 1}')
        col2.metric('Carga', format_scientific(c_edit['q'], 'C'))
        col3.metric('X', f'{float(c_edit['x']):.2f} m')
        col4.metric('Y', f'{float(c_edit['y']):.2f} m')
    target_idx = st.session_state.selected_idx
    target_charge = charges[target_idx]
    force_error = None
    try:
        net_f = calculate_net_force(target_charge, charges)
    except ValueError as exc:
        net_f = np.array([0.0, 0.0])
        force_error = str(exc)
    force_mag = np.linalg.norm(net_f)
    st.subheader('Resultados')
    if force_error:
        st.warning('No se puede calcular la fuerza porque hay cargas exactamente en la misma posicion. Separe las cargas en el diagrama o en los controles.')
    m1, m2, m3 = st.columns(3)
    m1.metric('Componente Fx', format_scientific(net_f[0], 'N'))
    m2.metric('Componente Fy', format_scientific(net_f[1], 'N'))
    m3.metric('Magnitud |F|', format_scientific(force_mag, 'N'))
    st.subheader('Grafico Interactivo')
    render_charge_diagram(key='force_diagram', title='Arrastre una carga para recalcular la fuerza', charges=charges, mode=mode, selected_idx=target_idx, net_force=net_f, height=360 if '1D' in mode else 560)
    with st.expander('Ver grafico Plotly'):
        if '1D' in mode:
            fig = plot_system_1d(charges=charges, target_charge=target_charge, net_force=net_f, selected_idx=target_idx)
        else:
            fig = plot_system_2d(charges=charges, target_charge=target_charge, net_force=net_f, selected_idx=target_idx)
        st.plotly_chart(fig, width='stretch', config=PLOTLY_CONFIG)
with tab2:
    st.header('Campo Electrico')
    st.info('Arrastre las esferas rojas/azules para mover las cargas. El campo se recalcula despues de soltar la carga.')
    col_plot, col_ctrl = st.columns([3, 1])
    with col_ctrl:
        st.markdown('**Parametros**')
        grid_res = st.select_slider('Densidad de lineas', options=[10, 15, 20, 25, 30, 40], value=20)
        st.divider()
        st.markdown('**Sonda puntual**')
        st.caption('Mida el campo en un punto arbitrario:')
        px = st.number_input('X (m)', value=0.0, step=1.0)
        py = 0.0
        if '2D' in mode:
            py = st.number_input('Y (m)', value=1.0, step=1.0)
        try:
            e_field = calculate_electric_field_at_point((px, py), charges)
        except ValueError as exc:
            st.warning(exc)
        else:
            st.metric('Intensidad en sonda', format_scientific(np.linalg.norm(e_field), 'N/C'))
            with st.expander('Componentes'):
                st.write(f'Ex = {format_scientific(e_field[0], 'N/C')}')
                st.write(f'Ey = {format_scientific(e_field[1], 'N/C')}')
    with col_plot:
        render_charge_diagram(key='field_diagram', title='Diagrama editable de cargas', charges=charges, mode=mode, selected_idx=st.session_state.selected_idx, height=300 if '1D' in mode else 360)
        if '2D' in mode:
            with st.spinner('Calculando campo electrico...'):
                fig_field = plot_electric_field(charges, grid_size=grid_res, selected_idx=st.session_state.selected_idx)
                st.plotly_chart(fig_field, width='stretch', config=PLOTLY_CONFIG)
        else:
            st.warning('El mapa de campo esta optimizado para 2D. Cambie a modo 2D en la barra lateral.')
with tab3:
    st.header('Fundamentos de Electrostatica')
    st.markdown('Las ecuaciones que gobiernan este simulador:')
    col_eq1, col_eq2 = st.columns(2)
    with col_eq1:
        with st.container(border=True):
            st.subheader('1. Ley de Coulomb')
            st.latex('F = k \\frac{|q_1 q_2|}{r^2}')
            st.caption('La fuerza entre dos cargas es proporcional al producto de sus magnitudes e inversamente proporcional al cuadrado de la distancia. k = 8.99e9 N m2/C2.')
    with col_eq2:
        with st.container(border=True):
            st.subheader('2. Principio de Superposicion')
            st.latex('\\vec{F}_{neta} = \\sum_{i} \\vec{F}_i')
            st.caption('La fuerza neta sobre una carga es la suma vectorial de todas las fuerzas individuales ejercidas por las demas cargas.')
    with st.container(border=True):
        st.subheader('3. Campo Electrico')
        st.latex('\\vec{E} = \\frac{\\vec{F}}{q_0} = k \\sum \\frac{q_i}{r_i^2} \\hat{r}_i')
        st.caption('El campo electrico es la fuerza por unidad de carga de prueba. Define el espacio que rodea a las cargas.')