import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Planta", layout="wide", initial_sidebar_state="expanded")

# 1. CSS para animaciones
st.markdown("""
<style>
    .fade-in { animation: fadeInAnimation 0.8s ease-in-out; }
    @keyframes fadeInAnimation { from { opacity: 0; } to { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# 2. BASE DE DATOS COMPLETA (Transcripción exacta de tu tabla)
@st.cache_data
def load_data():
    # [Área, Código, Nombre, Alerta, Acción, RFE]
    # Valores: [2024, 2025, 2025Dic, 2026]
    data = [
        ("Cuarto de aguas", "C", "Cisterna", [3,0,0,0], [1,0,0,0], [0,0,0,0]),
        ("Cuarto de aguas", "2S", "Filtro Dual", [4,0,0,0], [2,1,0,0], [0,0,0,0]),
        ("Cuarto de aguas", "3S", "Filtro Suavizador", [3,0,0,0], [0,0,0,0], [0,0,0,0]),
        ("Cuarto de aguas", "4S", "Tanque Suavizada", [6,0,0,0], [1,0,0,0], [0,0,0,0]),
        ("Cuarto de aguas", "5S", "Osmosis Inversa", [16,0,0,0], [4,0,0,0], [1,0,0,0]),
        ("Cuarto de aguas", "SV-201", "CGA-N1 Salida Termo", [3,0,0,0], [0,0,1,0], [0,0,0,0]),
        ("Cuarto de aguas", "SV-203", "CGA-N1 Salida Interc", [16,1,0,0], [9,0,0,0], [0,0,0,0]),
        ("Inyectables", "HV-207-AI", "Muestreo Normal", [5,3,0,1], [4,5,0,1], [1,0,2,1]),
        ("Inyectables", "HV-207-DI", "Muestreo Valvula", [10,1,0,0], [13,2,0,0], [9,0,0,0]),
        ("Inyectables", "HV-208-AI", "Muestreo Normal", [17,3,0,0], [10,1,0,1], [1,0,0,0]),
        ("Inyectables", "HV-208-DI", "Muestreo Valvula", [6,0,0,0], [6,1,0,0], [4,0,0,0]),
        ("Sólidos", "PU-17L", "Cuarto Granulación", [1,1,0,2], [8,1,1,0], [0,0,0,0]),
        ("Sólidos", "PU-18L", "Área Técnica", [3,0,0,1], [0,0,0,0], [0,0,0,0]),
        ("Líquidos", "PU-1L", "Cto Manuf Líquidos", [3,0,0,0], [2,0,0,0], [0,0,0,0]),
        ("Semisólidos", "PU-4L", "Semisólidos 3", [7,10,0,1], [8,6,0,2], [0,1,0,1]),
        ("Externos", "PU-27L", "Desarrollo", [0,0,0,0], [1,0,0,0], [0,0,0,0]),
    ]
    rows = []
    for a, c, n, al, ac, r in data:
        rows.append({"Área":a, "Código":c, "Nombre":n, 
                     "Alerta_2024":al[0], "Alerta_2025":al[1], "Alerta_2025_Dic":al[2], "Alerta_2026":al[3],
                     "Acción_2024":ac[0], "Acción_2025":ac[1], "Acción_2025_Dic":ac[2], "Acción_2026":ac[3],
                     "RFE_2024":r[0], "RFE_2025":r[1], "RFE_2025_Dic":r[2], "RFE_2026":r[3]})
    return pd.DataFrame(rows)

if 'df_agua' not in st.session_state: st.session_state.df_agua = load_data()

# 3. Sidebar
with st.sidebar:
    st.title("🎛️ Filtros")
    area = st.selectbox("Área", st.session_state.df_agua["Área"].unique())
    # Filtro por Código Base para agrupar Normal/Válvula
    codigos_area = st.session_state.df_agua[st.session_state.df_agua["Área"] == area]["Código"].tolist()
    punto = st.selectbox("Punto de Uso", ["TODOS"] + codigos_area)
    metrica = st.selectbox("Métrica", ["Alerta", "Acción", "RFE"])

# 4. Panel Principal con Animación Fade-in
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
st.title(f"Vista: {area}")

df_f = st.session_state.df_agua[st.session_state.df_agua["Área"] == area]
if punto != "TODOS": df_f = df_f[df_f["Código"] == punto]

# 5. Gráficas
for _, row in df_f.iterrows():
    y = [row[f"{metrica}_2024"], row[f"{metrica}_2025"], row[f"{metrica}_2025_Dic"], row[f"{metrica}_2026"]]
    
    fig = go.Figure(go.Scatter(
        x=["2024", "2025", "2025 (Dic)", "2026"], y=y, 
        mode='lines+markers', line=dict(width=5, shape='spline', smoothing=1.3),
        marker=dict(size=12)
    ))
    
    fig.update_layout(
        title=f"{row['Nombre']} ({row['Código']})", 
        height=320, width=420,
        xaxis=dict(type='category'), yaxis=dict(range=[-0.5, max(y)+5]),
        margin=dict(l=20, r=20, t=50, b=20), template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=False)
st.markdown('</div>', unsafe_allow_html=True)

# 6. Edición y Guardado
with st.expander("⚙️ Editar Datos"):
    st.session_state.df_agua = st.data_editor(st.session_state.df_agua, use_container_width=True)
    st.download_button("💾 Guardar CSV", st.session_state.df_agua.to_csv(index=False), "datos_planta.csv")
