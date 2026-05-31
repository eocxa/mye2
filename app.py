import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from models.charge import Charge
from physics.net_force import calculate_net_force
from physics.electric_field import calculate_electric_field_at_point
from visualization.plot_1d import plot_system_1d
from visualization.plot_2d import plot_system_2d
from visualization.plot_field import plot_electric_field

st.set_page_config(page_title="Simulador de Electrostática", layout="wide")

st.title("⚡ Simulador de Cargas Eléctricas")
st.markdown("""
Esta aplicación permite modelar sistemas de cargas puntuales, calcular fuerzas resultantes 
y visualizar el campo eléctrico.
""")

# Configuración en la barra lateral
st.sidebar.header("Configuración del Sistema")
mode = st.sidebar.selectbox("Seleccione Modo", ["1D (Eje X)", "2D (Plano XY)"])
num_charges = st.sidebar.number_input("Número de Cargas", min_value=1, max_value=10, value=2)

charges = []
for i in range(num_charges):
    st.sidebar.subheader(f"Carga {i+1}")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        q = st.number_input(f"Carga {i+1} (C)", value=1e-6, format="%.2e", key=f"q{i}")
        x = st.number_input(f"Posición X {i+1} (m)", value=float(i*2), key=f"x{i}")
    with col2:
        y = 0.0
        if mode == "2D (Plano XY)":
            y = st.number_input(f"Posición Y {i+1} (m)", value=0.0, key=f"y{i}")
    
    charges.append(Charge(q, x, y))

# Pestañas para organizar la visualización
tab1, tab2 = st.tabs(["🚀 Fuerza Neta", "🌐 Campo Eléctrico"])

with tab1:
    st.header("Análisis de Fuerza Neta")
    target_idx = st.selectbox("Seleccione carga objetivo", range(1, num_charges + 1)) - 1
    
    target_charge = charges[target_idx]
    net_f = calculate_net_force(target_charge, charges)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Fuerza Fx", f"{net_f[0]:.4e} N")
    col2.metric("Fuerza Fy", f"{net_f[1]:.4e} N")
    col3.metric("Magnitud Total", f"{np.linalg.norm(net_f):.4e} N")

    # Generar gráfica
    if "1D" in mode:
        fig = plot_system_1d(charges, target_charge, net_f)
    else:
        fig = plot_system_2d(charges, target_charge, net_f)
    
    st.pyplot(fig)

with tab2:
    st.header("Análisis de Campo Eléctrico")
    
    if "2D" in mode:
        st.subheader("Mapa de Campo Eléctrico")
        grid_res = st.slider("Resolución de la malla", 10, 50, 20)
        if st.button("Generar Mapa de Campo"):
            with st.spinner("Calculando campo..."):
                fig_field = plot_electric_field(charges, grid_size=grid_res)
                st.pyplot(fig_field)
    
    st.subheader("Campo en un punto específico")
    cp_col1, cp_col2 = st.columns(2)
    px = cp_col1.number_input("Punto X (m)", value=1.0)
    py = 0.0
    if "2D" in mode:
        py = cp_col2.number_input("Punto Y (m)", value=1.0)
    
    e_field = calculate_electric_field_at_point((px, py), charges)
    
    ecol1, ecol2, ecol3 = st.columns(3)
    ecol1.metric("Campo Ex", f"{e_field[0]:.4e} N/C")
    ecol2.metric("Campo Ey", f"{e_field[1]:.4e} N/C")
    ecol3.metric("Magnitud E", f"{np.linalg.norm(e_field):.4e} N/C")

st.sidebar.markdown("---")
st.sidebar.info("Desarrollado como herramienta educativa para Física.")
