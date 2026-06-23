import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Configuración de la página - sidebar expandido por defecto
st.set_page_config(page_title="Dashboard Sistema de Agua", layout="wide", initial_sidebar_state="expanded")

# 2. CSS para asegurar que los filtros sean visibles
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E9ECEF; }
    .sidebar-title { font-size: 0.85rem; color: #1E40AF; font-weight: 800; margin-top: 20px; margin-bottom: 10px; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# 3. Base de Datos (igual a la versión anterior que funcionaba)
@st.cache_data
def load_initial_data():
    datos_crudos = [
        ("Cuarto de aguas", "6S", [3,0,0,0], [1,0,0,0], [0,0,0,0]),
        ("Cuarto de aguas", "SV-203", [16,0,0,0], [4,0,0,0], [1,0,0,0]),
        ("Sólidos", "PU-17L", [1,1,0,0], [3,1,0,0], [0,0,0,0]),
        ("Inyectables", "SV-204", [4,0,0,0], [2,0,0,0], [0,0,0,0]),
        ("Inyectables", "HV-207-AI M. Normal", [5,3,0,1], [4,5,0,1], [1,0,2,1])
    ]
    filas = []
    for area, codigo, alerta, accion, rfe in datos_crudos:
        filas.append({"Área": area, "Código": codigo, "Alerta_2024": alerta[0], "Alerta_2025": alerta[1], "Alerta_2025_Dic": alerta[2], "Alerta_2026": alerta[3], "Acción_2024": accion[0], "Acción_2025": accion[1], "Acción_2025_Dic": accion[2], "Acción_2026": accion[3], "RFE_2024": rfe[0], "RFE_2025": rfe[1], "RFE_2025_Dic": rfe[2], "RFE_2026": rfe[3], "Sin_Desviaciones": False})
    return pd.DataFrame(filas)

if 'df_agua' not in st.session_state: st.session_state.df_agua = load_initial_data()

# 4. MENÚ LATERAL (SIDEBAR) - SIEMPRE VISIBLE
with st.sidebar:
    st.title("🎛️ Panel de Control")
    st.write("Selecciona los filtros para actualizar las vistas.")
    
    areas_list = ["Cuarto de aguas", "Sólidos", "Líquidos", "Semisólidos", "Inyectables", "Externos a producción"]
    seccion_seleccionada = st.selectbox("Área", areas_list, index=4)
    
    codigos_area = st.session_state.df_agua[st.session_state.df_agua["Área"] == seccion_seleccionada]["Código"].tolist()
    punto_seleccionado = st.selectbox("Punto de Uso", ["MOSTRAR TODOS"] + codigos_area)
    
    metrica_activa = st.selectbox("Límite a analizar", ["Alerta", "Acción", "RFE"])

# 5. Panel Principal
st.title(f"Vista: {seccion_seleccionada}")
df_filtrado = st.session_state.df_agua[st.session_state.df_agua["Área"] == seccion_seleccionada]
if punto_seleccionado != "MOSTRAR TODOS":
    df_filtrado = df_filtrado[df_filtrado["Código"] == punto_seleccionado]

# Gráficas
x_labels = ["2024", "2025", "2025 (Dic)", "2026"]
for _, row in df_filtrado.iterrows():
    y_vals = [row[f"{metrica_activa}_2024"], row[f"{metrica_activa}_2025"], row[f"{metrica_activa}_2025_Dic"], row[f"{metrica_activa}_2026"]]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_labels, y=y_vals, mode='lines+markers', line=dict(shape='spline', width=4)))
    fig.update_layout(title=row['Código'], height=200, margin=dict(l=10, r=10, t=30, b=10), xaxis=dict(type='category'), yaxis=dict(range=[-0.5, max(y_vals)+2]))
    st.plotly_chart(fig, use_container_width=True)

# 6. Editor
with st.expander("⚙️ Editar Base de Datos"):
    st.session_state.df_agua = st.data_editor(st.session_state.df_agua, use_container_width=True)
