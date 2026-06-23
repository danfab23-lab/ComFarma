import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Configuración
st.set_page_config(page_title="Dashboard Sistema de Agua", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    .fade-in { animation: fadeInAnimation 0.8s ease-in-out; }
    @keyframes fadeInAnimation { from { opacity: 0; } to { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# 2. BASE DE DATOS COMPLETA (Actualizada con todos tus datos)
@st.cache_data
def load_data():
    # Estructura: (Área, Código, Alerta[24,25,25Dic,26], Acción[24,25,25Dic,26], RFE[24,25,25Dic,26])
    data = [
        ("Cuarto de aguas", "6S", [3,0,0,0], [1,0,0,0], [0,0,0,0]),
        ("Cuarto de aguas", "7SS", [4,0,0,0], [2,1,0,0], [0,0,0,0]),
        ("Cuarto de aguas", "SV-201", [3,0,0,0], [0,0,1,0], [0,0,0,0]),
        ("Cuarto de aguas", "SV-202", [6,0,0,0], [1,0,0,0], [0,0,0,0]),
        ("Cuarto de aguas", "SV-203", [16,0,0,0], [4,0,0,0], [1,0,0,0]),
        ("Cuarto de aguas", "SV-205", [16,1,0,0], [9,0,0,0], [0,0,0,0]),
        ("Cuarto de aguas", "HV-210", [16,5,0,0], [10,5,0,1], [3,1,0,0]),
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
        ("Líquidos", "PU-1L", [3,0,0,0], [2,0,0,0], [0,0,0,0]),
        ("Líquidos", "PU-2L", [4,1,0,0], [4,0,0,0], [0,0,0,0]),
        ("Líquidos", "PU-3L", [5,0,0,1], [2,0,1,0], [0,0,0,0]),
        ("Líquidos", "PU-22L", [3,4,0,1], [10,2,0,0], [0,0,0,0]),
        ("Líquidos", "PU-34L", [1,2,0,0], [1,1,1,0], [0,0,0,0]),
        ("Líquidos", "PU-35L", [0,0,0,0], [1,0,0,0], [0,0,0,0]),
        ("Semisólidos", "PU-4L", [7,10,0,1], [8,6,0,2], [0,1,0,1]),
        ("Semisólidos", "PU-5L", [5,2,0,3], [2,0,0,0], [0,0,0,1]),
        ("Semisólidos", "PU-6L", [2,0,0,0], [0,0,0,0], [0,0,0,0]),
        ("Semisólidos", "PU-7L", [3,0,0,1], [0,1,0,0], [0,0,0,0]),
        ("Semisólidos", "PU-8L", [3,4,0,0], [4,2,0,0], [0,0,0,0]),
        ("Semisólidos", "PU-9L", [11,2,0,0], [3,0,0,0], [0,0,0,0]),
        ("Semisólidos", "PU-10L", [6,2,0,1], [5,2,1,0], [0,0,0,0]),
        ("Semisólidos", "PU-33L", [5,0,0,1], [2,4,2,0], [0,2,0,1]),
        ("Inyectables", "SV-204", [4,0,0,0], [2,0,0,0], [0,0,0,0]),
        ("Inyectables", "HV-207-AI M. Normal", [5,3,0,1], [4,5,0,1], [1,0,2,1]),
        ("Inyectables", "HV-207-DI M. Normal", [10,1,0,0], [13,2,0,0], [9,0,0,0]),
        ("Inyectables", "HV-208-AI M. Normal", [17,3,0,0], [10,1,0,1], [1,0,0,0]),
        ("Inyectables", "HV-208-DI M. Normal", [6,0,0,0], [6,1,0,0], [4,0,0,0]),
        ("Inyectables", "1 VP", [0,3,0,0], [3,0,0,0], [0,0,0,0]),
        ("Inyectables", "2 VP", [5,4,0,0], [2,0,0,0], [0,0,0,0]),
        ("Inyectables", "3 VP", [0,8,0,0], [1,2,0,0], [0,0,0,0]),
        ("Inyectables", "4 VP", [2,7,0,0], [2,0,0,0], [1,0,0,0]),
        ("Externos", "PU-27L", [0,0,0,0], [1,0,0,0], [0,0,0,0]),
        ("Externos", "PU-13L", [2,0,0,1], [0,0,0,1], [0,0,0,0]),
        ("Externos", "PU-14L", [0,4,0,0], [3,0,0,0], [0,0,0,0]),
        ("Externos", "PU-15L", [2,1,0,0], [3,0,0,0], [0,0,0,0]),
        ("Externos", "PU-16L", [5,0,0,0], [0,0,0,0], [0,0,0,0]),
        ("Externos", "PU-11L", [0,0,0,0], [0,0,0,0], [0,0,0,0]),
        ("Externos", "PU-12L", [0,0,0,0], [0,0,0,0], [0,0,0,0]),
        ("Externos", "PU-30L", [0,0,0,0], [3,0,0,0], [0,0,0,0]),
        ("Externos", "PU-36L", [0,1,0,0], [1,0,0,0], [0,0,0,0])
    ]
    rows = []
    for a, c, al, ac, r in data:
        rows.append({"Área":a, "Código":c, "Alerta_2024":al[0], "Alerta_2025":al[1], "Alerta_2025_Dic":al[2], "Alerta_2026":al[3],
                     "Acción_2024":ac[0], "Acción_2025":ac[1], "Acción_2025_Dic":ac[2], "Acción_2026":ac[3],
                     "RFE_2024":r[0], "RFE_2025":r[1], "RFE_2025_Dic":r[2], "RFE_2026":r[3]})
    return pd.DataFrame(rows)

df = load_data()

# 3. Sidebar
with st.sidebar:
    st.title("🎛️ Filtros")
    areas = df["Área"].unique().tolist()
    seccion = st.selectbox("Área", areas)
    codigos = ["MOSTRAR TODOS"] + df[df["Área"] == seccion]["Código"].tolist()
    punto = st.selectbox("Punto de Uso", codigos)
    metrica = st.selectbox("Métrica", ["Alerta", "Acción", "RFE"])

# 4. Panel Principal con Animación Fade-in
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
st.title(f"Vista: {seccion}")
df_f = df[df["Área"] == seccion]
if punto != "MOSTRAR TODOS": df_f = df_f[df_f["Código"] == punto]

# 5. Gráficas Suavizadas y Cuadradas
for _, row in df_f.iterrows():
    y_vals = [row[f"{metrica}_2024"], row[f"{metrica}_2025"], row[f"{metrica}_2025_Dic"], row[f"{metrica}_2026"]]
    fig = go.Figure(go.Scatter(x=["2024", "2025", "2025 (Dic)", "2026"], y=y_vals, mode='lines+markers', 
                               line=dict(width=5, shape='spline', smoothing=1.3), marker=dict(size=12)))
    fig.update_layout(title=f"Código: {row['Código']}", height=320, width=420, xaxis=dict(type='category'), 
                      yaxis=dict(range=[-0.5, max(y_vals)+5]), margin=dict(l=20, r=20, t=50, b=20), template="plotly_white")
    st.plotly_chart(fig, use_container_width=False)

st.markdown('</div>', unsafe_allow_html=True)
with st.expander("⚙️ Editar Base de Datos"):
    st.session_state.df_agua = st.data_editor(df, use_container_width=True)
