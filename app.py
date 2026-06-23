import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configuración básica
st.set_page_config(page_title="Dashboard Planta", layout="wide")

# Animación CSS
st.markdown("""
<style>
    .fade-in { animation: fadeInAnimation 0.5s ease-in-out; }
    @keyframes fadeInAnimation { from { opacity: 0; } to { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# 1. CARGA DE DATOS (Lee el archivo datos.csv directamente)
@st.cache_data
def load_data():
    # header=1 salta la primera fila de etiquetas generales y toma la segunda como columnas
    df = pd.read_csv("datos.csv", header=1)
    
    # Normalizamos nombres de columnas para que no haya ambigüedades
    # El archivo tiene: Area, Codigo, 2024, 2025, 2025(Dic), 2026...
    # Ajustamos para tener nombres limpios: Area, Codigo, Alerta_24, Alerta_25...
    # Esta parte asume el orden exacto de tu CSV
    new_cols = ["Area", "Codigo", "Alerta_24", "Alerta_25", "Alerta_25Dic", "Alerta_26", 
                "C_Accion", "Accion_24", "Accion_25", "Accion_25Dic", "Accion_26", 
                "RFE_24", "RFE_25", "RFE_25Dic", "RFE_26"]
    df.columns = new_cols
    
    df["Area"] = df["Area"].ffill() # Llena las celdas vacías del área
    # Creamos el código base para agrupar (tomando el texto antes del primer salto de línea o espacio)
    df["Base"] = df["Codigo"].astype(str).str.split('\n').str[0].str.split(' ').str[0]
    return df

# Carga de datos con control de errores simple
try:
    if 'df' not in st.session_state:
        st.session_state.df = load_data()
except Exception as e:
    st.error(f"Error al leer datos.csv: {e}")
    st.stop()

# 2. Sidebar
with st.sidebar:
    st.title("🎛️ Filtros")
    area = st.selectbox("Área", st.session_state.df["Area"].dropna().unique())
    bases = ["TODOS"] + sorted(st.session_state.df[st.session_state.df["Area"]==area]["Base"].unique().tolist())
    filtro_base = st.selectbox("Código Base", bases)
    metrica = st.selectbox("Métrica", ["Alerta", "Accion", "RFE"])

# 3. Panel Principal
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
st.title(f"Dashboard: {area}")

df_f = st.session_state.df[st.session_state.df["Area"] == area]
if filtro_base != "TODOS": df_f = df_f[df_f["Base"] == filtro_base]

# 4. Gráficas
for base in df_f["Base"].unique():
    subset = df_f[df_f["Base"] == base]
    fig = go.Figure()
    
    for _, row in subset.iterrows():
        y = [row[f"{metrica}_24"], row[f"{metrica}_25"], row[f"{metrica}_25Dic"], row[f"{metrica}_26"]]
        fig.add_trace(go.Scatter(
            x=["2024", "2025", "2025 (Dic)", "2026"], y=y, 
            mode='lines+markers', name=str(row['Codigo']),
            line=dict(width=5, shape='spline', smoothing=1.3),
            marker=dict(size=12)
        ))
    
    fig.update_layout(title=f"Código: {base}", height=320, width=450,
                      xaxis=dict(type='category'), template="plotly_white",
                      margin=dict(l=20, r=20, t=50, b=20),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=False)

st.markdown('</div>', unsafe_allow_html=True)

# 5. Edición
with st.expander("⚙️ Editar Datos"):
    st.session_state.df = st.data_editor(st.session_state.df, use_container_width=True)
    st.download_button("Descargar CSV", st.session_state.df.to_csv(index=False), "datos_planta.csv")
