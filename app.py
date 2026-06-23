import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Configuración de la página
st.set_page_config(page_title="Dashboard Sistema de Agua", layout="wide", initial_sidebar_state="expanded")

# 2. CSS personalizado
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; }
</style>
""", unsafe_allow_html=True)

# 3. Base de Datos (Misma estructura completa)
@st.cache_data
def load_data():
    data = [
        ("Cuarto de aguas", "6S", [3,0,0,0], [1,0,0,0], [0,0,0,0]),
        ("Cuarto de aguas", "SV-203", [16,0,0,0], [4,0,0,0], [1,0,0,0]),
        ("Sólidos", "PU-17L", [1,1,0,0], [3,1,0,0], [0,0,0,0]),
        ("Inyectables", "SV-204", [4,0,0,0], [2,0,0,0], [0,0,0,0]),
        ("Inyectables", "HV-207-AI M. Normal", [5,3,0,1], [4,5,0,1], [1,0,2,1])
    ]
    rows = []
    for a, c, al, ac, r in data:
        rows.append({"Área":a, "Código":c, "Alerta_2024":al[0], "Alerta_2025":al[1], "Alerta_2025_Dic":al[2], "Alerta_2026":al[3],
                     "Acción_2024":ac[0], "Acción_2025":ac[1], "Acción_2025_Dic":ac[2], "Acción_2026":ac[3],
                     "RFE_2024":r[0], "RFE_2025":r[1], "RFE_2025_Dic":r[2], "RFE_2026":r[3]})
    return pd.DataFrame(rows)

df = load_data()

# 4. Sidebar
with st.sidebar:
    st.title("🎛️ Filtros")
    areas = df["Área"].unique().tolist()
    seccion = st.selectbox("Área", areas)
    codigos = ["MOSTRAR TODOS"] + df[df["Área"] == seccion]["Código"].tolist()
    punto = st.selectbox("Punto de Uso", codigos)
    metrica = st.selectbox("Métrica", ["Alerta", "Acción", "RFE"])

# 5. Panel Principal
st.title(f"Vista: {seccion}")
df_f = df[df["Área"] == seccion]
if punto != "MOSTRAR TODOS": df_f = df_f[df_f["Código"] == punto]

# 6. Gráficas Suavizadas y Animadas
for _, row in df_f.iterrows():
    y = [row[f"{metrica}_2024"], row[f"{metrica}_2025"], row[f"{metrica}_2025_Dic"], row[f"{metrica}_2026"]]
    
    # Línea suavizada (spline)
    fig = go.Figure(go.Scatter(
        x=["2024", "2025", "2025 (Dic)", "2026"], 
        y=y, 
        mode='lines+markers', 
        line=dict(width=4, shape='spline', smoothing=1.3) # Smoothing da el toque curvo
    ))
    
    fig.update_layout(
        title=f"Código: {row['Código']}", 
        height=300, 
        width=400,
        xaxis=dict(type='category'), 
        yaxis=dict(range=[-0.5, max(y)+2]),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    # Animación rápida al renderizar
    st.plotly_chart(fig, use_container_width=False)

with st.expander("⚙️ Editar Datos"):
    st.data_editor(df, use_container_width=True)
