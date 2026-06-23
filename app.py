import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración inicial de la página
st.set_page_config(page_title="Monitoreo Sistema de Agua", layout="wide")

st.title("📊 Análisis Histórico: Sistema de Agua")
st.markdown("Plataforma interactiva para evaluar tendencias de Límites de Alerta, Acción y RFE. Permite comparar datos históricos y documentar revisiones del año en curso de manera ágil.")

# Pre-carga de puntos de uso basada en la tabla original
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
        {"No.": 41, "Tipo": "Agua Inyectables", "Punto de Uso": "CGA-N1-01, salida termocompresor", "Código": "SV-201", "Área": "Cuarto de aguas"},
        {"No.": 43, "Tipo": "Agua Inyectables", "Punto de Uso": "CGA-N1-01, salida intercambiador", "Código": "SV-203", "Área": "Cuarto de aguas"},
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

# Mantener los datos en la sesión
if 'df_agua' not in st.session_state:
    st.session_state.df_agua = load_initial_data()

meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre", "Sin Actualizar"]

st.subheader("1. Base de Datos Interactiva (Editor Directo)")
st.info("💡 Puedes editar los valores directamente en la tabla. 
- Ajusta el mes de revisión para 2026.
- Si marcas la casilla 'Sin_Desviaciones', el gráfico automáticamente tomará un valor de 0 incidentes para todos los límites.")

col_config = {
    "Mes_Revision_2026": st.column_config.SelectboxColumn("Mes Rev. 2026", options=meses, required=True),
    "Sin_Desviaciones": st.column_config.CheckboxColumn("Sin Desviaciones (0 Alertas/Acciones/RFE)")
}

# Editor de datos incrustado en la interfaz
edited_df = st.data_editor(
    st.session_state.df_agua, 
    column_config=col_config, 
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True
)
st.session_state.df_agua = edited_df

st.divider()
st.subheader("2. Gráficos de Tendencia Dinámicos")

# Selectores para navegación de áreas y puntos
col1, col2 = st.columns(2)
with col1:
    areas = ["Todas"] + sorted(edited_df["Área"].dropna().unique().tolist())
    selected_area = st.selectbox("1. Filtrar por Área:", areas)

with col2:
    if selected_area != "Todas":
        codigos = edited_df[edited_df["Área"] == selected_area]["Código"].dropna().unique().tolist()
    else:
        codigos = edited_df["Código"].dropna().unique().tolist()
        
    selected_code = st.selectbox("2. Seleccionar Código (Punto de Uso):", codigos)

plot_data = edited_df[edited_df["Código"] == selected_code]

if not plot_data.empty:
    plot_data = plot_data.iloc[0]
    st.markdown(f"**Punto de Uso:** {plot_data['Punto de Uso']} | **Área:** {plot_data['Área']} | **Tipo de Agua:** {plot_data['Tipo']}")
    
    mes_2026 = plot_data["Mes_Revision_2026"]
    x_labels = ["2024", "2025", "2025 (Dic)", f"2026 ({mes_2026})"]
    
    # Comprobación de checkbox de desviaciones
    if plot_data["Sin_Desviaciones"]:
        y_alerta = [0, 0, 0, 0]
        y_accion = [0, 0, 0, 0]
        y_rfe = [0, 0, 0, 0]
        st.success("✅ Este punto está marcado sin desviaciones (0 incidentes registrados en todos los rubros).")
    else:
        y_alerta = [plot_data["Alerta_2024"], plot_data["Alerta_2025"], plot_data["Alerta_2025_Dic"], plot_data["Alerta_2026"]]
        y_accion = [plot_data["Acción_2024"], plot_data["Acción_2025"], plot_data["Acción_2025_Dic"], plot_data["Acción_2026"]]
        y_rfe = [plot_data["RFE_2024"], plot_data["RFE_2025"], plot_data["RFE_2025_Dic"], plot_data["RFE_2026"]]

    fig = go.Figure()
    
    # Gráfico tipo PowerBI con curvas suaves
    fig.add_trace(go.Scatter(x=x_labels, y=y_alerta, mode='lines+markers', name='Límite Alerta', 
                             line=dict(shape='spline', color='#1E90FF', width=3), marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=x_labels, y=y_accion, mode='lines+markers', name='Límite Acción', 
                             line=dict(shape='spline', color='#FF8C00', width=3), marker=dict(size=8)))
    fig.add_trace(go.Scatter(x=x_labels, y=y_rfe, mode='lines+markers', name='RFE', 
                             line=dict(shape='spline', color='#DC143C', width=3), marker=dict(size=8)))
    
    fig.update_layout(
        title=f"Tendencia de Eventos - Código: {selected_code}",
        xaxis_title="Periodo Evaluado",
        yaxis_title="Cantidad de Eventos Registrados",
        plot_bgcolor='white',
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray', rangemode="tozero", zeroline=True, zerolinewidth=2, zerolinecolor='LightGray')
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No hay datos disponibles para la selección actual.")
