import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Sistema de Agua", layout="wide")

# CSS para animación
st.markdown("""
<style>
    .fade-in { animation: fadeInAnimation 0.8s ease-in-out; }
    @keyframes fadeInAnimation { from { opacity: 0; } to { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# 1. CARGA Y PROCESAMIENTO
@st.cache_data
def load_csv_data():
    df = pd.read_csv("datos.csv", header=1, encoding='latin-1')
    
    new_cols = ["Area", "Codigo", "Alerta_24", "Alerta_25", "Alerta_25Dic", "Alerta_26", 
                "C_Accion", "Accion_24", "Accion_25", "Accion_25Dic", "Accion_26", 
                "RFE_24", "RFE_25", "RFE_25Dic", "RFE_26"]
    df = df.iloc[:, :len(new_cols)]
    df.columns = new_cols
    
    df["Area"] = df["Area"].ffill()
    df["Codigo_Clean"] = df["Codigo"].astype(str).str.replace('\n', ' ', regex=False).str.strip()
    df["Base"] = df["Codigo_Clean"].apply(lambda x: x.split(" Muestreo")[0].strip())
    return df

try:
    if 'df' not in st.session_state:
        st.session_state.df = load_csv_data()
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
st.title(f"Área: {area}")

df_f = st.session_state.df[st.session_state.df["Area"] == area]
if filtro_base != "TODOS": df_f = df_f[df_f["Base"] == filtro_base]

# 4. Gráficas en 2 Columnas
bases_en_vista = df_f["Base"].unique()
cols = st.columns(2) # Definimos el layout de 2 columnas

for i, base in enumerate(bases_en_vista):
    with cols[i % 2]: # Alternar entre columna 0 y 1
        fig = go.Figure()
        subset = df_f[df_f["Base"] == base]
        
        for _, row in subset.iterrows():
            y = [row[f"{metrica}_24"], row[f"{metrica}_25"], row[f"{metrica}_25Dic"], row[f"{metrica}_26"]]
            fig.add_trace(go.Scatter(
                x=["2024", "2025", "2025 (Dic)", "2026"], y=y, 
                mode='lines+markers', name=str(row['Codigo_Clean']),
                line=dict(width=5, shape='spline', smoothing=1.3),
                marker=dict(size=12)
            ))
        
        fig.update_layout(
            title=f"Código Base: {base}", height=320,
            xaxis=dict(type='category'), template="plotly_white",
            margin=dict(l=20, r=20, t=50, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
