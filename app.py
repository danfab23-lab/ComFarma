import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Dashboard Sistema de Agua", layout="wide")

# CSS para animación y estilo
st.markdown("""
<style>
    .fade-in { animation: fadeInAnimation 0.8s ease-in-out; }
    @keyframes fadeInAnimation { from { opacity: 0; } to { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# 1. CARGA DE DATOS COMPLETA
@st.cache_data
def load_data():
    # Estructura: (Área, Código, Alerta[24,25,25Dic,26], Acción[24,25,25Dic,26], RFE[24,25,25Dic,26])
    # He agrupado los de inyectables para que salgan juntos en la lista
    data = [
        # ... (Mantengo los datos de las áreas previas)
        ("Inyectables", "HV-207-AI Normal", [5,3,0,1], [4,5,0,1], [1,0,2,1]),
        ("Inyectables", "HV-207-DI Válvula", [0,0,0,0], [0,0,0,0], [0,0,0,0]),
        ("Inyectables", "HV-208-AI Normal", [17,3,0,0], [10,1,0,1], [1,0,0,0]),
        ("Inyectables", "HV-208-DI Válvula", [0,0,0,0], [0,0,0,0], [0,0,0,0]),
        # ... resto de tus datos ...
    ]
    # (Para el resto de datos, asegúrate de mantener la estructura [24,25,25Dic,26])
    rows = []
    for a, c, al, ac, r in data:
        rows.append({"Área":a, "Código":c, "Alerta_2024":al[0], "Alerta_2025":al[1], "Alerta_2025_Dic":al[2], "Alerta_2026":al[3],
                     "Acción_2024":ac[0], "Acción_2025":ac[1], "Acción_2025_Dic":ac[2], "Acción_2026":ac[3],
                     "RFE_2024":r[0], "RFE_2025":r[1], "RFE_2025_Dic":r[2], "RFE_2026":r[3]})
    return pd.DataFrame(rows)

if 'df_agua' not in st.session_state: st.session_state.df_agua = load_data()

# 2. Sidebar
with st.sidebar:
    st.title("🎛️ Filtros")
    seccion = st.selectbox("Área", st.session_state.df_agua["Área"].unique())
    codigos = ["MOSTRAR TODOS"] + st.session_state.df_agua[st.session_state.df_agua["Área"] == seccion]["Código"].tolist()
    punto = st.selectbox("Punto de Uso", codigos)
    metrica = st.selectbox("Métrica", ["Alerta", "Acción", "RFE"])

# 3. Panel Principal
st.markdown('<div class="fade-in">', unsafe_allow_html=True)
st.title(f"Vista: {seccion}")

# Filtrado
df_f = st.session_state.df_agua[st.session_state.df_agua["Área"] == seccion]
if punto != "MOSTRAR TODOS": df_f = df_f[df_f["Código"] == punto]

# 4. Gráficas
for _, row in df_f.iterrows():
    y = [row[f"{metrica}_2024"], row[f"{metrica}_2025"], row[f"{metrica}_2025_Dic"], row[f"{metrica}_2026"]]
    
    fig = go.Figure(go.Scatter(
        x=["2024", "2025", "2025 (Dic)", "2026"], y=y, 
        mode='lines+markers', line=dict(width=5, shape='spline', smoothing=1.3), 
        marker=dict(size=12)
    ))
    
    fig.update_layout(title=f"Código: {row['Código']}", height=320, width=420, 
                      xaxis=dict(type='category'), yaxis=dict(range=[-0.5, max(y)+5]), 
                      margin=dict(l=20, r=20, t=50, b=20), template="plotly_white")
    st.plotly_chart(fig, use_container_width=False)
st.markdown('</div>', unsafe_allow_html=True)

# 5. Edición y Guardado
with st.expander("⚙️ Editar y Guardar Base de Datos"):
    st.session_state.df_agua = st.data_editor(st.session_state.df_agua, use_container_width=True)
    
    # Botón para "Guardar" (Descarga el CSV actualizado)
    csv = st.session_state.df_agua.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="💾 Guardar Cambios (Descargar CSV actualizado)",
        data=csv,
        file_name='datos_agua_actualizados.csv',
        mime='text/csv',
    )
