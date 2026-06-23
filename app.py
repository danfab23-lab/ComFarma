import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Configuración de la página
st.set_page_config(page_title="Dashboard Sistema de Agua", layout="wide", initial_sidebar_state="expanded")

# 2. Inyección de CSS personalizado para la interfaz limpia
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    header {visibility: hidden;}
    .kpi-card {
        background-color: white; border-radius: 15px; padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); text-align: center;
        height: 100%; border: 1px solid #E9ECEF;
    }
    .kpi-title { font-size: 0.85rem; color: #8B98A5; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-value { font-size: 2.8rem; color: #1E40AF; font-weight: 800; margin: 10px 0; line-height: 1; }
    .kpi-value-text { font-size: 1.8rem; color: #343A40; font-weight: 700; margin: 10px 0; line-height: 1.2; }
    .kpi-subtitle { font-size: 0.85rem; color: #8B98A5; font-style: italic; }
    .blue-line { height: 4px; background-color: #1E40AF; width: 40px; border-radius: 2px; margin-top: 15px; }
    .status-dot { height: 12px; width: 12px; background-color: #10B981; border-radius: 50%; display: inline-block; margin-left: 10px; margin-bottom: 4px; }
    [data-testid="stSidebar"] { background-color: white; }
    .sidebar-title { font-size: 0.8rem; color: #8B98A5; font-weight: bold; padding-left: 10px; margin-top: 20px; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

# 3. Base de Datos Inicial Precargada con Datos Históricos (Actualizada)
@st.cache_data
def load_initial_data():
    # Estructura: (Area, Codigo, [Alerta 24, 25, 25Dic, 26], [Accion 24, 25, 25Dic, 26], [RFE 24, 25, 25Dic, 26])
    datos_crudos = [
        # Cuarto de aguas
        ("Cuarto de aguas", "6S", [3,0,0,0], [1,0,0,0], [0,0,0,0]),
        ("Cuarto de aguas", "7SS", [4,0,0,0], [2,1,0,0], [0,0,0,0]),
        ("Cuarto de aguas", "SV-201", [3,0,0,0], [0,0,1,0], [0,0,0,0]),
        ("Cuarto de aguas", "SV-202", [6,0,0,0], [1,0,0,0], [0,0,0,0]),
        ("Cuarto de aguas", "SV-203", [16,0,0,0], [4,0,0,0], [1,0,0,0]),
        ("Cuarto de aguas", "SV-205", [16,1,0,0], [9,0,0,0], [0,0,0,0]),
        ("Cuarto de aguas", "HV-210", [16,5,0,0], [10,5,0,1], [3,1,0,0]),
        # Sólidos
        ("Sólidos", "PU-17L", [1,1,0,0], [3,1,0,0], [0,0,0,0]),
        ("Sólidos", "PU-18L", [1,0,0,0], [1,0,0,0], [0,0,0,0]),
        ("Sólidos", "PU-19L", [6,0,0,0], [2,1,0,0], [0,0,0,0]),
        ("Sólidos", "PU-20L", [2,1,0,0], [4,0,0,0], [0,0,0,0]),
        ("Sólidos", "PU-21L", [2,0,0,0], [0,0,0,0], [0,0,0,0]),
        ("Sólidos", "PU-23L", [3,0,0,1], [2,0,1,0], [0,0,0,0]),
        ("Sólidos", "PU-24L", [1,1,0,2], [8,1,1,0], [0,0,0,0]),
        ("Sólidos", "PU-25L", [3,0,0,1], [0,0,0,0], [0,0,0,0]),
        ("Sólidos", "PU-26L", [1,1,0,0], [2,0,0,0], [0,0,0,0]),
        ("Sólidos", "PU-28L", [3,2,0,0], [2,3,0,0], [0,0,0,0]),
        # Líquidos
        ("Líquidos", "PU-1L", [3,0,0,0], [2,0,0,0], [0,0,0,0]),
        ("Líquidos", "PU-2L", [4,1,0,0], [4,0,0,0], [0,0,0,0]),
        ("Líquidos", "PU-3L", [5,0,0,1], [2,0,1,0], [0,0,0,0]),
        ("Líquidos", "PU-22L", [3,4,0,1], [10,2,0,0], [0,0,0,0]),
        ("Líquidos", "PU-34L", [1,2,0,0], [1,1,1,0], [0,0,0,0]),
        ("Líquidos", "PU-35L", [0,0,0,0], [1,0,0,0], [0,0,0,0]),
        # Semisólidos
        ("Semisólidos", "PU-4L", [7,10,0,1], [8,6,0,2], [0,1,0,1]),
        ("Semisólidos", "PU-5L", [5,2,0,3], [2,0,0,0], [0,0,0,1]),
        ("Semisólidos", "PU-6L", [2,0,0,0], [0,0,0,0], [0,0,0,0]),
        ("Semisólidos", "PU-7L", [3,0,0,1], [0,1,0,0], [0,0,0,0]),
        ("Semisólidos", "PU-8L", [3,4,0,0], [4,2,0,0], [0,0,0,0]),
        ("Semisólidos", "PU-9L", [11,2,0,0], [3,0,0,0], [0,0,0,0]),
        ("Semisólidos", "PU-10L", [6,2,0,1], [5,2,1,0], [0,0,0,0]),
        ("Semisólidos", "PU-33L", [5,0,0,1], [2,4,2,0], [0,2,0,1]),
        # Inyectables
        ("Inyectables", "SV-204", [4,0,0,0], [2,0,0,0], [0,0,0,0]),
        ("Inyectables", "HV-207-AI M. Normal", [5,3,0,1], [4,5,0,1], [1,0,2,1]),
        ("Inyectables", "HV-207-AI M. Valvula", [0,0,0,0], [0,0,0,0], [0,0,0,0]),
        ("Inyectables", "HV-207-DI M. Normal", [10,1,0,0], [13,2,0,0], [9,0,0,0]),
        ("Inyectables", "HV-207-DI M. Valvula", [0,0,0,0], [0,0,0,0], [0,0,0,0]),
        ("Inyectables", "HV-208-AI M. Normal", [17,3,0,0], [10,1,0,1], [1,0,0,0]),
        ("Inyectables", "HV-208-AI M. Valvula", [0,0,0,0], [0,0,0,0], [0,0,0,0]),
        ("Inyectables", "HV-208-DI M. Normal", [6,0,0,0], [6,1,0,0], [4,0,0,0]),
        ("Inyectables", "HV-208-DI M. Valvula", [0,0,0,0], [0,0,0,0], [0,0,0,0]),
        ("Inyectables", "1 VP", [0,3,0,0], [3,0,0,0], [0,0,0,0]),
        ("Inyectables", "2 VP", [5,4,0,0], [2,0,0,0], [0,0,0,0]),
        ("Inyectables", "3 VP", [0,8,0,0], [1,2,0,0], [0,0,0,0]),
        ("Inyectables", "4 VP", [2,7,0,0], [2,0,0,0], [1,0,0,0]),
        # Externos a producción
        ("Externos a producción", "PU-27L", [0,0,0,0], [1,0,0,0], [0,0,0,0]),
        ("Externos a producción", "PU-13L", [2,0,0,1], [0,0,0,1], [0,0,0,0]),
        ("Externos a producción", "PU-14L", [0,4,0,0], [3,0,0,0], [0,0,0,0]),
        ("Externos a producción", "PU-15L", [2,1,0,0], [3,0,0,0], [0,0,0,0]),
        ("Externos a producción", "PU-16L", [5,0,0,0], [0,0,0,0], [0,0,0,0]),
        ("Externos a producción", "PU-11L", [0,0,0,0], [0,0,0,0], [0,0,0,0]),
        ("Externos a producción", "PU-12L", [0,0,0,0], [0,0,0,0], [0,0,0,0]),
        ("Externos a producción", "PU-30L", [0,0,0,0], [3,0,0,0], [0,0,0,0]),
        ("Externos a producción", "PU-36L", [0,1,0,0], [1,0,0,0], [0,0,0,0])
    ]
    
    filas = []
    for area, codigo, alerta, accion, rfe in datos_crudos:
        filas.append({
            "Área": area, "Código": codigo,
            "Alerta_2024": alerta[0], "Alerta_2025": alerta[1], "Alerta_2025_Dic": alerta[2], "Alerta_2026": alerta[3],
            "Acción_2024": accion[0], "Acción_2025": accion[1], "Acción_2025_Dic": accion[2], "Acción_2026": accion[3],
            "RFE_2024": rfe[0], "RFE_2025": rfe[1], "RFE_2025_Dic": rfe[2], "RFE_2026": rfe[3],
            "Mes_Revision_2026": "Enero", "Sin_Desviaciones": False
        })
    return pd.DataFrame(filas)

if 'df_agua' not in st.session_state:
    st.session_state.df_agua = load_initial_data()

# 4. Navegación Lateral (Sidebar)
with st.sidebar:
    st.markdown('<div class="sidebar-title">SECCIÓN</div>', unsafe_allow_html=True)
    areas_list = ["Cuarto de aguas", "Sólidos", "Líquidos", "Semisólidos", "Inyectables", "Externos a producción"]
    areas_upper = [a.upper() for a in areas_list]
    default_index = areas_upper.index("INYECTABLES") if "INYECTABLES" in areas_upper else 0
    
    seccion_seleccionada = st.radio("Sección", areas_upper, index=default_index, label_visibility="collapsed")
    area_real = areas_list[areas_upper.index(seccion_seleccionada)]
    
    st.markdown(f'<div class="sidebar-title">PUNTOS EN {seccion_seleccionada}</div>', unsafe_allow_html=True)
    codigos_area = st.session_state.df_agua[st.session_state.df_agua["Área"] == area_real]["Código"].tolist()
    opciones_puntos = ["ALL"] + codigos_area
    punto_seleccionado = st.radio("Puntos", opciones_puntos, label_visibility="collapsed")
    
    st.markdown('<div class="sidebar-title">LÍMITE</div>', unsafe_allow_html=True)
    metrica_activa = st.radio("Métrica", ["Alerta", "Acción", "RFE"], label_visibility="collapsed")

# 5. Panel Principal - KPIs Superiores
col1, col2, col3 = st.columns(3)
cantidad_puntos = len(codigos_area) if punto_seleccionado == "ALL" else 1

with col1:
    st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-title">PUNTOS EN SECCIÓN</div>
            <div class="kpi-value">{cantidad_puntos}</div>
            <div class="blue-line"></div>
        </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-title">MÉTRICA ACTIVA</div>
            <div class="kpi-value">{metrica_activa.upper()}</div>
            <div class="kpi-subtitle">Visualizando límites de {metrica_activa.lower()}</div>
        </div>
    ''', unsafe_allow_html=True)

with col3:
    st.markdown('''
        <div class="kpi-card">
            <div class="kpi-title">ESTADO GENERAL</div>
            <div class="kpi-value-text">Sistema<br>Operativo <span class="status-dot"></span></div>
        </div>
    ''', unsafe_allow_html=True)

st.write("") 

# 6. Grid de Gráficas Individuales
df_filtrado = st.session_state.df_agua[st.session_state.df_agua["Área"] == area_real]
if punto_seleccionado != "ALL":
    df_filtrado = df_filtrado[df_filtrado["Código"] == punto_seleccionado]

cols_por_fila = 2
filas = [st.columns(cols_por_fila) for _ in range((len(df_filtrado) + cols_por_fila - 1) // cols_por_fila)]

for i, (_, row) in enumerate(df_filtrado.iterrows()):
    col = filas[i // cols_por_fila][i % cols_por_fila]
    codigo = row["Código"]
    mes = row["Mes_Revision_2026"]
    x_labels = ["2024", "2025", "2025(Dic)", f"2026({mes[:3]})"]
    
    if row["Sin_Desviaciones"]:
        y_vals = [0, 0, 0, 0]
    else:
        y_vals = [row[f"{metrica_activa}_2024"], row[f"{metrica_activa}_2025"], row[f"{metrica_activa}_2025_Dic"], row[f"{metrica_activa}_2026"]]
    
    valor_actual = y_vals[-1]
    
    with col:
        with st.container():
            st.markdown(f"""
            <div style="background-color: white; border-radius: 15px; padding: 20px; border: 1px solid #E9ECEF; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <span style="font-size: 1.2rem; font-weight: bold; color: #1E293B;">{codigo}</span>
                    <span style="font-size: 0.7rem; font-weight: bold; color: #ADB5BD; cursor: pointer;">DETALLE</span>
                </div>
                <div style="font-size: 0.8rem; font-weight: bold; color: #1E40AF; margin-bottom: 15px;">ACTUAL: {valor_actual}</div>
            """, unsafe_allow_html=True)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x_labels, y=y_vals, 
                mode='lines+markers', 
                line=dict(shape='spline', color='#1E40AF', width=4), 
                marker=dict(size=8, color='#1E40AF', symbol='circle')
            ))
            
            fig.update_layout(
                height=200, 
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=True, gridcolor='#F1F5F9', showticklabels=False, zeroline=False),
                yaxis=dict(showgrid=True, gridcolor='#F1F5F9', showticklabels=False, zeroline=False, rangemode='tozero'),
                hovermode="x unified"
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown("</div>", unsafe_allow_html=True)

# 7. Editor de Base de Datos
st.divider()
with st.expander("⚙️ ACTUALIZAR BASE DE DATOS (Ingresar Límites y RFE)", expanded=False):
    st.info("💡 Haz doble clic en cualquier celda para editar el valor. Puedes agregar nuevas filas al final de la tabla. Los cambios se reflejarán inmediatamente en los gráficos.")
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    col_config = {
        "Mes_Revision_2026": st.column_config.SelectboxColumn("Mes Rev. 2026", options=meses, required=True),
        "Sin_Desviaciones": st.column_config.CheckboxColumn("Sin Desviaciones (0 en todo)")
    }
    
    edited_df = st.data_editor(
        st.session_state.df_agua, 
        column_config=col_config, 
        num_rows="dynamic",  # Esto permite agregar y borrar filas
        use_container_width=True,
        hide_index=True
    )
    st.session_state.df_agua = edited_df
