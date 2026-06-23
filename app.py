import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Configuración de la página (Debe ser la primera línea)
st.set_page_config(page_title="Dashboard Sistema de Agua", layout="wide", initial_sidebar_state="expanded")

# 2. Inyección de CSS personalizado para igualar el diseño de la imagen
st.markdown("""
<style>
    /* Fondo general más claro */
    .stApp { background-color: #F8F9FA; }
    
    /* Ocultar barra superior por defecto de Streamlit para más limpieza */
    header {visibility: hidden;}
    
    /* Estilo de las tarjetas KPI (Métricas superiores) */
    .kpi-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
        height: 100%;
        border: 1px solid #E9ECEF;
    }
    .kpi-title { font-size: 0.85rem; color: #8B98A5; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-value { font-size: 2.8rem; color: #1E40AF; font-weight: 800; margin: 10px 0; line-height: 1; }
    .kpi-value-text { font-size: 1.8rem; color: #343A40; font-weight: 700; margin: 10px 0; line-height: 1.2; }
    .kpi-subtitle { font-size: 0.85rem; color: #8B98A5; font-style: italic; }
    
    /* Línea azul decorativa en la primera tarjeta */
    .blue-line { height: 4px; background-color: #1E40AF; width: 40px; border-radius: 2px; margin-top: 15px; }
    
    /* Punto verde de estado operativo */
    .status-dot { height: 12px; width: 12px; background-color: #10B981; border-radius: 50%; display: inline-block; margin-left: 10px; margin-bottom: 4px; }
    
    /* Ajustes del menú lateral */
    [data-testid="stSidebar"] { background-color: white; }
    .sidebar-title { font-size: 0.8rem; color: #8B98A5; font-weight: bold; padding-left: 10px; margin-top: 20px; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

# 3. Base de Datos Inicial
@st.cache_data
def load_initial_data():
    puntos = [
        {"No.": 1, "Tipo": "Agua potable", "Punto de Uso": "Cisterna", "Código": "C", "Área": "Cuarto de aguas"},
        {"No.": 2, "Tipo": "Agua Pre-tratada", "Punto de Uso": "Filtro Dual Media", "Código": "2S", "Área": "Cuarto de aguas"},
        {"No.": 3, "Tipo": "Agua Pre-tratada", "Punto de Uso": "Filtro suavisador", "Código": "3S", "Área": "Cuarto de aguas"},
        {"No.": 4, "Tipo": "Agua Pre-tratada", "Punto de Uso": "Tanque de agua suavizada", "Código": "4S", "Área": "Cuarto de aguas"},
        {"No.": 5, "Tipo": "Agua Pre-tratada", "Punto de Uso": "Osmosis Inversa", "Código": "5S", "Área": "Cuarto de aguas"},
        {"No.": 8, "Tipo": "Agua Purificada", "Punto de Uso": "Cuarto de manufactura de líquidos #1", "Código": "PU-1L", "Área": "Líquidos"},
        {"No.": 11, "Tipo": "Agua Purificada", "Punto de Uso": "Semisólidos 3", "Código": "PU-4L", "Área": "Semisólidos"},
        {"No.": 12, "Tipo": "Agua Purificada", "Punto de Uso": "Semisólidos 2", "Código": "PU-5L", "Área": "Semisólidos"},
        {"No.": 13, "Tipo": "Agua Purificada", "Punto de Uso": "Semisólidos 1", "Código": "PU-6L", "Área": "Semisólidos"},
        {"No.": 20, "Tipo": "Agua Purificada", "Punto de Uso": "Zona de lavado Microbiología", "Código": "PU-13L", "Área": "Control de calidad"},
        {"No.": 22, "Tipo": "Agua Purificada", "Punto de Uso": "Zona de lavado de Desarrollo", "Código": "PU-15L", "Área": "Desarrollo"},
        {"No.": 24, "Tipo": "Agua Purificada", "Punto de Uso": "Cuarto de granulación 2", "Código": "PU-17L", "Área": "Sólidos"},
        {"No.": 25, "Tipo": "Agua Purificada", "Punto de Uso": "Área Técnica de granulación", "Código": "PU-18L", "Área": "Sólidos"},
        {"No.": 26, "Tipo": "Agua Purificada", "Punto de Uso": "Cuarto de granulación", "Código": "PU-19L", "Área": "Sólidos"},
        {"No.": 27, "Tipo": "Agua Purificada", "Punto de Uso": "Cuarto de lavado sólidos", "Código": "PU-20L", "Área": "Sólidos"},
        {"No.": 41, "Tipo": "Agua Inyectables", "Punto de Uso": "CGA-N1-01, salida termocompresor", "Código": "SV-201", "Área": "Inyectables"},
        {"No.": 43, "Tipo": "Agua Inyectables", "Punto de Uso": "CGA-N1-01, salida intercambiador", "Código": "SV-203", "Área": "Inyectables"},
        {"No.": 44, "Tipo": "Agua Inyectables", "Punto de Uso": "Lavado y despirogenizado", "Código": "SV-204", "Área": "Inyectables"},
        {"No.": 46, "Tipo": "Agua Inyectables", "Punto de Uso": "Lavado de material Planta baja", "Código": "HV-207-AI", "Área": "Inyectables"},
        {"No.": 48, "Tipo": "Agua Inyectables", "Punto de Uso": "Preparación de soluciones", "Código": "HV-208-AI", "Área": "Inyectables"},
        {"No.": 52, "Tipo": "Vapor puro", "Punto de Uso": "Salida Generador de vapor", "Código": "1 VP", "Área": "Inyectables"},
        {"No.": 53, "Tipo": "Vapor puro", "Punto de Uso": "Autoclave Högner", "Código": "2 VP", "Área": "Inyectables"},
        {"No.": 54, "Tipo": "Vapor puro", "Punto de Uso": "Tanque de fabricación 500 L", "Código": "3 VP", "Área": "Inyectables"},
        {"No.": 55, "Tipo": "Vapor puro", "Punto de Uso": "Autoclave Shinva", "Código": "4 VP", "Área": "Inyectables"}
    ]
    df = pd.DataFrame(puntos)
    metricas = ["Alerta", "Acción", "RFE"]
    años = ["2024", "2025", "2025_Dic", "2026"]
    for m in metricas:
        for a in años:
            df[f"{m}_{a}"] = 0
    df["Mes_Revision_2026"] = "Enero"
    df["Sin_Desviaciones"] = False
    return df

if 'df_agua' not in st.session_state:
    st.session_state.df_agua = load_initial_data()

# 4. Navegación Lateral (Sidebar)
with st.sidebar:
    st.markdown('<div class="sidebar-title">SECCIÓN</div>', unsafe_allow_html=True)
    areas_list = sorted(st.session_state.df_agua["Área"].dropna().unique().tolist())
    areas_upper = [a.upper() for a in areas_list]
    # Forzamos que "INYECTABLES" sea una opción destacada si existe
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

st.write("") # Espaciador

# 6. Grid de Gráficas Individuales
df_filtrado = st.session_state.df_agua[st.session_state.df_agua["Área"] == area_real]
if punto_seleccionado != "ALL":
    df_filtrado = df_filtrado[df_filtrado["Código"] == punto_seleccionado]

# Creamos columnas para el grid (2 gráficas por fila)
cols_por_fila = 2
filas = [st.columns(cols_por_fila) for _ in range((len(df_filtrado) + cols_por_fila - 1) // cols_por_fila)]

for i, (_, row) in enumerate(df_filtrado.iterrows()):
    col = filas[i // cols_por_fila][i % cols_por_fila]
    
    # Extraer datos
    codigo = row["Código"]
    mes = row["Mes_Revision_2026"]
    x_labels = ["2024", "2025", "2025(Dic)", f"2026({mes[:3]})"]
    
    if row["Sin_Desviaciones"]:
        y_vals = [0, 0, 0, 0]
    else:
        y_vals = [row[f"{metrica_activa}_2024"], row[f"{metrica_activa}_2025"], row[f"{metrica_activa}_2025_Dic"], row[f"{metrica_activa}_2026"]]
    
    valor_actual = y_vals[-1]
    
    with col:
        # Contenedor estilo tarjeta para la gráfica
        with st.container():
            st.markdown(f"""
            <div style="background-color: white; border-radius: 15px; padding: 20px; border: 1px solid #E9ECEF; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <span style="font-size: 1.2rem; font-weight: bold; color: #1E293B;">{codigo}</span>
                    <span style="font-size: 0.7rem; font-weight: bold; color: #ADB5BD; cursor: pointer;">DETALLE</span>
                </div>
                <div style="font-size: 0.8rem; font-weight: bold; color: #1E40AF; margin-bottom: 15px;">NORMAL: {valor_actual}</div>
            """, unsafe_allow_html=True)
            
            # Gráfica minimalista con Plotly
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

# 7. Editor de Base de Datos (Oculto en un expander para mantener limpio el Dashboard)
st.divider()
with st.expander("⚙️ ACTUALIZAR BASE DE DATOS (Ingresar Límites y RFE)", expanded=False):
    st.info("💡 Edita los valores aquí. Los cambios se reflejarán inmediatamente en las gráficas superiores.")
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
    col_config = {
        "Mes_Revision_2026": st.column_config.SelectboxColumn("Mes Rev. 2026", options=meses, required=True),
        "Sin_Desviaciones": st.column_config.CheckboxColumn("Sin Desviaciones (0 en todo)")
    }
    
    edited_df = st.data_editor(
        st.session_state.df_agua, 
        column_config=col_config, 
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True
    )
    st.session_state.df_agua = edited_df
