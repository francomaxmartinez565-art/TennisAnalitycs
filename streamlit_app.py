import streamlit as st
from datetime import date

# Configuración v2.9.0
st.set_page_config(page_title="Vantaje Algoritmo v2.9.0", layout="wide")

st.title("🎾 Vantaje Algoritmo v2.9.0")
st.markdown("### Dashboard Pro: Análisis de Probabilidades")

# --- SECCIÓN 1: CONFIGURACIÓN ---
st.header("1. Configuración del Encuentro")
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    torneo = st.text_input("Torneo", "ATP Masters")
    superficie_actual = st.selectbox("Superficie Actual", ["Arcilla", "Dura", "Césped", "Indoor"])
    h2h = st.text_input("Historial H2H", "0-0")
with col_m2:
    j1_nom = st.text_input("Jugador 1", "Djokovic")
    j1_rank = st.number_input("Rank J1", 1, 1000, 1) 
    j1_cuota = st.number_input("Cuota J1", 1.0, 50.0, 1.90)
with col_m3:
    j2_nom = st.text_input("Jugador 2", "Federer")
    j2_rank = st.number_input("Rank J2", 1, 1000, 1) 
    j2_cuota = st.number_input("Cuota J2", 1.0, 50.0, 1.90)

st.divider()

# --- SECCIÓN 2: CARGA DE DATOS ---
def cargar_jugador_full(nombre):
    st.subheader(f"Carga de Datos: {nombre}")
    partidos = []
    for i in range(3):
        with st.expander(f"Partido Reciente {i+1}", expanded=(i==0)):
            c1, c1_f, c2, c2_r, c3 = st.columns([1.5, 1, 1, 1, 1])
            with c1: rival = st.text_input(f"Rival", f"Rival {i+1}", key=f"r_{nombre}_{i}")
            with c1_f: fecha_p = st.date_input("Fecha", date.today(), key=f"f_{nombre}_{i}")
            with c2: res = st.selectbox("Resultado", ["Ganó", "Perdió", "Gano por retiro", "Perdio por retiro"], key=f"res_{nombre}_{i}")
            with c2_r: r_rank = st.number_input("Rank Rival", 1, 1000, 50, key=f"rr_{nombre}_{i}")
            with c3: surf = st.selectbox(f"Superficie", ["Arcilla", "Dura", "Césped", "Indoor"], key=f"s_{nombre}_{i}")
            
            st.markdown("**Estadísticas:**")
            c5, c6, c7, c8, c9, c10a, c10b = st.columns(7)
            with c5: s1_in = st.number_input("% P1S", 0, 100, 65, key=f"p1s_{nombre}_{i}")
            with c6: p1 = st.number_input("% G1S", 0, 100, 70, key=f"p1_{nombre}_{i}")
            with c7: p2 = st.number_input("% G2S", 0, 100, 50, key=f"p2_{nombre}_{i}")
            with c8: d1 = st.number_input("% G1Dev", 0, 100, 30, key=f"d1_{nombre}_{i}")
            with c9: d2 = st.number_input("% G2Dev", 0, 100, 45, key=f"d2_{nombre}_{i}")
            with c10a: bs_sv = st.number_input("Bks Salv", 0, 50, 2, key=f"bssv_{nombre}_{i}")
            with c10b: bs_enf = st.number_input("Bks Enf", 0, 50, 3, key=f"bsenf_{nombre}_{i}")
            
            partidos.append({"p1":p1, "d1":d1, "bs_sv": bs_sv, "bs_enf": bs_enf})
    return partidos

data_j1 = cargar_jugador_full(j1_nom)
st.divider()
data_j2 = cargar_jugador_full(j2_nom)

# --- SECCIÓN 3: RESULTADOS ---
if st.button("EJECUTAR ANÁLISIS VANTAGE"):
    def stats(data):
        avg_p1 = sum([p['p1'] for p in data]) / 3
        avg_d1 = sum([p['d1'] for p in data]) / 3
        sv = sum([p['bs_sv'] for p in data]); enf = sum([p['bs_enf'] for p in data])
        bps = (sv / enf * 100) if enf > 0 else 100.0
        return avg_p1, avg_d1, bps

    p1_j1, d1_j1, bps_j1 = stats(data_j1)
    p1_j2, d1_j2, bps_j2 = stats(data_j2)
    poder_j1 = p1_j1 + d1_j1
    poder_j2 = p1_j2 + d1_j2
    ganador = j1_nom if poder_j1 > poder_j2 else j2_nom
    dif = abs(poder_j1 - poder_j2)

    # Lógica de mercado
    j_verde = f"Win {ganador}"
    # Línea de juegos basada en la suma de G1S de ambos
    suma_saque = p1_j1 + p1_j2
    if suma_saque > 150: j_amarilla = "Over 22.5 Games"
    elif suma_saque > 135: j_amarilla = "Over 21.5 Games"
    else: j_amarilla = "Under 21.5 Games"
    
    j_roja = f"Win {ganador} 2-0" if dif > 12 else f"Win {ganador} 2-1"

    st.header(f"📋 Informe: {j1_nom} vs {j2_nom}")
    post = f"🎾 Vantaje Report: {j1_nom} vs {j2_nom}\n\n🟢 {j_verde}\n🟡 {j_amarilla}\n🔴 {j_roja}\n\n📊 Dato: {ganador} con {max(p1_j1, p1_j2):.1f}% G1S y {max(bps_j1, bps_j2):.1f}% BPS."
    st.text_area("Post para X:", post, height=150)
