import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Planta", layout="wide", initial_sidebar_state="expanded")

# CSS para animaciones
st.markdown("""
<style>
    .fade-in { animation: fadeInAnimation 0.8s ease-in-out; }
    @keyframes fadeInAnimation { from { opacity: 0; } to { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# 1. BASE DE DATOS COMPLETA (Transcrita exactamente de tu imagen)
@st.cache_data
def load_full_data():
    # [Área, Código Base, Subtipo, Alerta[24,25,25Dic,26], Acción[24,25,25Dic,26], RFE[24,25,25Dic,26]]
    data = [
        ("Cuarto de aguas", "6S", "Principal", [3,0,0,0], [1,0,0,0], [0,0,0,0]),
        ("Cuarto de aguas", "SV-201", "CGA-N1", [3,0,0,0], [0,0,1,0], [0,0,0,0]),
        ("Inyectables", "HV-207", "Normal", [5,3,0,1], [4,5,0,1], [1,0,2,1]),
        ("Inyectables", "HV-207", "Válvula", [10,1,0,0], [13,2,0,0], [9,0,0,0]),
        ("Inyectables", "HV-208", "Normal", [17,3,0,0], [10,1,0,1], [1,0,0,0]),
        ("Inyectables", "HV-208", "Válvula", [6,0,0,0], [6,1,0,0], [4,0,0,0]),
        ("Inyectables", "VP", "1 VP", [0,3,0,0], [3,0,0,0], [0,0,0,0]),
        ("Inyectables", "VP", "2 VP", [5,4,0,0], [2,0,0,0], [0,0,0,0]),
        ("Inyectables", "VP", "3 VP", [0,8,0,0], [1,2,0,0], [0,0,0,0]),
        ("Inyectables", "VP", "4 VP", [2,7,0,0], [2,0,0,0], [1,0,0,0]),
        ("Sólidos", "PU-17L", "Cto Granulación", [1,1,0,2], [8,1,1,0], [0,0,0,0]),
        ("Sólidos", "PU-18L", "Área Técnica", [3,0,0,1], [0,0,0,0], [0,0,0,0]),
        ("Líquidos", "PU-1L", "Cto Manuf", [3,0,0,0], [2,0,0,0], [0,0,0,0]),
        ("Externos", "PU-13L", "Lab. Control", [2,0,0,1], [0,0,0,1], [0,0,0,0]),
        ("Externos", "PU-27L", "Desarrollo", [0,0,0,0], [1,0,0,0], [0,0,0,0])
    ]
    rows = []
    for a, c, s, al, ac, r in data:
        rows.append({"Área":a, "Código":c, "Tipo":s, 
                     "Alerta_24":al[0], "Alerta_25":al[1], "Alerta_25Dic":al[2], "Alerta_26":al[3],
                     "Acción_24":ac[0], "Acción_25":ac[1], "Acción_25Dic":ac[2], "Acción_26":ac[3],
                     "RFE_24":r[0], "RFE_25":r[1], "RFE_25Dic":r[2], "RFE_26":r[3]})
    return pd.DataFrame(rows)

if 'df' not in st.session_state: st.session_state.df = load_full_data()

# 2. Sidebar
with st.sidebar:
    st.title("🎛️ Filtros")
    area = st.selectbox("Área", st.session_state.df["Área"].unique())
    # Filtro para agrupar (ej. todos los HV-207 juntos)
    codigos_base = ["TODOS"] + st.session_state.df[st.session_state.df["Área"]==area]["Código"].unique().tolist()
    filtro_base = st.selectbox("Código Base", codigos_base)
    metrica = st.selectbox("Métrica", ["Alerta", "Acción", "RFE"])

# 3. Panel Principal Animado
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
st.title(f"Dashboard: {area}")

# Filtrado
df_f = st.session_state.df[st.session_state.df["Área"] == area]
if filtro_base != "TODOS": df_f = df_f[df_f["Código"] == filtro_base]

# 4. Gráficas Agrupadas
# Iteramos sobre los códigos bases únicos presentes en la vista
codigos_en_vista = df_f["Código"].unique()

for c in codigos_en_vista:
    fig = go.Figure()
    subset = df_f[df_f["Código"] == c]
    
    for _, row in subset.iterrows():
        y = [row[f"{metrica}_24"], row[f"{metrica}_25"], row[f"{metrica}_25Dic"], row[f"{metrica}_26"]]
        fig.add_trace(go.Scatter(
            x=["2024", "2025", "2025 (Dic)", "2026"], y=y, 
            mode='lines+markers', name=row['Tipo'], # Aquí aparece 'Normal' o 'Válvula' en la leyenda
            line=dict(width=5, shape='spline', smoothing=1.3), marker=dict(size=12)
        ))
    
    fig.update_layout(
        title=f"Código: {c}", height=320, width=420,
        xaxis=dict(type='category'), yaxis=dict(range=[-0.5, 20]),
        margin=dict(l=20, r=20, t=50, b=20), template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=False)

st.markdown('</div>', unsafe_allow_html=True)

# 5. Edición y Guardado Seguro
with st.expander("⚙️ Editar y Guardar Datos"):
    st.session_state.df = st.data_editor(st.session_state.df, use_container_width=True)
    st.download_button("💾 Guardar Cambios (CSV)", st.session_state.df.to_csv(index=False), "datos_planta.csv")
