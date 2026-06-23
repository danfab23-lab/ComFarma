import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. Configuración
st.set_page_config(page_title="Dashboard Sistema de Agua", layout="wide", initial_sidebar_state="expanded")

# 2. CSS
st.markdown("""
<style>
    .stApp { background-color: #F8F9FA; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; }
</style>
""", unsafe_allow_html=True)

# 3. BASE DE DATOS COMPLETA (Transcrita de tu tabla)
@st.cache_data
def load_initial_data():
    # Estructura: (Área, Código, [Alerta 24, 25, 25Dic, 26], [Acción 24, 25, 25Dic, 26], [RFE 24, 25, 25Dic, 26])
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
    rows = []
    for a, c, al, ac, r in data:
        rows.append({"Área":a, "Código":c, "Alerta_2024":al[0], "Alerta_2025":al[1], "Alerta_2025_Dic":al[2], "Alerta_2026":al[3],
                     "Acción_2024":ac[0], "Acción_2025":ac[1], "Acción_2025_Dic":ac[2], "Acción_2026":ac[3],
                     "RFE_2024":r[0], "RFE_2025":r[1], "RFE_2025_Dic":r[2], "RFE_2026":r[3], "Sin_Desviaciones": False})
    return pd.DataFrame(rows)

if 'df_agua' not in st.session_state: st.session_state.df_agua = load_initial_data()

# 4. Sidebar (Re-configurado para que no se pierda)
with st.sidebar:
    st.title("🎛️ Filtros")
    areas = st.session_state.df_agua["Área"].unique().tolist()
    seccion = st.selectbox("Área", areas, index=areas.index("Inyectables"))
    codigos = ["MOSTRAR TODOS"] + st.session_state.df_agua[st.session_state.df_agua["Área"] == seccion]["Código"].tolist()
    punto = st.selectbox("Punto de Uso", codigos)
    metrica = st.selectbox("Métrica", ["Alerta", "Acción", "RFE"])

# 5. Panel Principal
st.title(f"Vista: {seccion}")
df = st.session_state.df_agua[st.session_state.df_agua["Área"] == seccion]
if punto != "MOSTRAR TODOS": df = df[df["Código"] == punto]

for _, row in df.iterrows():
    y = [row[f"{metrica}_2024"], row[f"{metrica}_2025"], row[f"{metrica_2025_Dic"], row[f"{metrica}_2026"]]
    fig = go.Figure(go.Scatter(x=["2024", "2025", "2025 (Dic)", "2026"], y=y, mode='lines+markers', line=dict(width=4)))
    fig.update_layout(title=row['Código'], height=200, xaxis=dict(type='category'), yaxis=dict(range=[-0.5, max(y)+2]))
    st.plotly_chart(fig, use_container_width=True)

with st.expander("⚙️ Editar Datos"):
    st.session_state.df_agua = st.data_editor(st.session_state.df_agua, use_container_width=True)
