import streamlit as st
from datetime import date

# Configuración de la App
st.set_page_config(page_title="Vantaje Algoritmo v2.8.1", layout="wide")

st.title("🎾 Vantaje Algoritmo v2.8.1")
st.markdown("### Dashboard de Análisis Predictivo Profesional")

# --- SECCIÓN 1: CONFIGURACIÓN DEL ENCUENTRO ---
st.header("1. Configuración del Encuentro")
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    torneo = st.text_input("Torneo", "ATP Madrid")
    superficie_actual = st.selectbox("Superficie Actual", ["Arcilla", "Dura", "Césped", "Indoor"])
    h2h = st.text_input("Historial H2H", "0-0")
with col_m2:
    j1_nom = st.text_input("Jugador 1", "Djokovic")
    j1_rank = st.number_input("Rank J1", 1, 1000, 1) 
    j1_cuota = st.number_input("Cuota J1", 1.0, 50.0, 1.90)
with col_m3:
    j2_nom = st.text_input("Jugador 2", "Federer")
    j2_rank = st.number_input("Rank J2", 1, 1000, 3) 
    j2_cuota = st.number_input("Cuota J2", 1.0, 50.0, 1.90)

st.divider()

# --- SECCIÓN 2: CARGA DE DATOS ---
def cargar_jugador_full(nombre):
    st.subheader(f"Carga de Datos: {nombre}")
    partidos = []
    for i in range(3):
        with st.expander(f"Partido Reciente {i+1}", expanded=(i==0)):
            c1, c2, c2_r, c3 = st.columns([2, 1, 1, 1])
            with c1: rival = st.text_input(f"Rival", f"Rival {i+1}", key=f"r_{nombre}_{i}")
            with c2: res = st.selectbox("Resultado", ["Ganó", "Perdió", "Gano por retiro", "Perdio por retiro"], key=f"res_{nombre}_{i}")
            with c2_r: r_rank = st.number_input("Rank Rival", 1, 1000, 100, key=f"rr_{nombre}_{i}")
            with c3: surf = st.selectbox(f"Surf", ["Arcilla", "Dura", "Césped", "Indoor"], key=f"s_{nombre}_{i}")
            
            st.markdown("**Estadísticas del Match:**")
            # Ampliamos a más columnas para que entren G2S, G1Dev y G2Dev
            c5, c6, c7, c8, c9, c10a, c10b = st.columns([1, 1, 1, 1, 1, 1, 1])
            with c5: s1_in = st.number_input("% P1S", 0, 100, 65, key=f"s1in_{nombre}_{i}")
            with c6: p1 = st.number_input("% G1S", 0, 100, 70, key=f"p1_{nombre}_{i}")
            with c7: p2 = st.number_input("% G2S", 0, 100, 50, key=f"p2_{nombre}_{i}")
            with c8: d1 = st.number_input("% G1Dev", 0, 100, 30, key=f"d1_{nombre}_{i}")
            with c9: d2 = st.number_input("% G2Dev", 0, 100, 45, key=f"d2_{nombre}_{i}")
            with c10a: bs_sv = st.number_input("Bks Salvados", 0, 50, 2, key=f"bssv_{nombre}_{i}")
            with c10b: bs_enf = st.number_input("Bks Enfrentados", 0, 50, 3, key=f"bsenf_{nombre}_{i}")
            
            partidos.append({"s1in":s1_in, "p1":p1, "p2":p2, "d1":d1, "d2":d2, "bs_sv": bs_sv, "bs_enf": bs_enf})
    return partidos

data_j1 = cargar_jugador_full(j1_nom)
st.divider()
data_j2 = cargar_jugador_full(j2_nom)

# --- SECCIÓN 3: VEREDICTO ---
if st.button("EJECUTAR ANÁLISIS VANTAGE"):
    st.header(f"📋 Informe Técnico: {j1_nom} vs {j2_nom}")
    
    def get_avg_vantage(data):
        total_bs_sv = sum([p['bs_sv'] for p in data])
        total_bs_enf = sum([p['bs_enf'] for p in data])
        return {
            'P1S': sum([p['s1in'] for p in data]) / 3,
            'G1S': sum([p['p1'] for p in data]) / 3,
            'G2S': sum([p['p2'] for p in data]) / 3,
            'G1Dev': sum([p['d1'] for p in data]) / 3,
            'BPS_frac': f"{total_bs_sv}/{total_bs_enf}",
            'BPS_pct': (total_bs_sv / total_bs_enf * 100) if total_bs_enf > 0 else 100.0,
            'enfrento_breaks': total_bs_enf > 0
        }

    avg_j1 = get_avg_vantage(data_j1)
    avg_j2 = get_avg_vantage(data_j2)

    st.info(f"**Diferencial de Ranking:** {abs(j1_rank - j2_rank)} puestos ({j1_nom if j1_rank < j2_rank else j2_nom} favorito por estatus)")

    st.subheader("📊 Métricas Comparativas")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("G1S (Poder)", f"{avg_j1['G1S']:.1f}%", f"{avg_j1['G1S'] - avg_j2['G1S']:.1f}%")
    c2.metric("G2S (Seguridad)", f"{avg_j1['G2S']:.1f}%", f"{avg_j1['G2S'] - avg_j2['G2S']:.1f}%")
    c3.metric("G1Dev (Resto)", f"{avg_j1['G1Dev']:.1f}%", f"{avg_j1['G1Dev'] - avg_j2['G1Dev']:.1f}%")
    
    if avg_j1['enfrento_breaks']:
        c4.metric("BPS (Resiliencia)", avg_j1['BPS_frac'], f"{avg_j1['BPS_pct']:.1f}%")
    else:
        c4.metric("BPS (Resiliencia)", "Dominio", "Sin breaks")

    st.divider()

    st.subheader("🎯 Proyecciones de Valor")
    col_a, col_b = st.columns(2)
    
    with col_a:
        puntos_j1 = avg_j1['G1S'] + avg_j1['G1Dev']
        puntos_j2 = avg_j2['G1S'] + avg_j2['G1Dev']
        ganador_proy = j1_nom if puntos_j1 > puntos_j2 else j2_nom
        st.success(f"**CUOTA A (Predicción):** \n\n **WIN {ganador_proy}**")
    
    with col_b:
        if avg_j1['G1S'] > 72 and avg_j2['G1S'] > 72:
            proy_g = "OVER 22.5 Games"
        else:
            proy_g = "Over 21.5 Games / Proyección Estándar"
        st.info(f"**CUOTA B (Estructural):** \n\n **{proy_g}**")


