import streamlit as st
from datetime import date

# Configuración de la App
st.set_page_config(page_title="Vantaje Algoritmo v2.8.7", layout="wide")

st.title("🎾 Vantaje Algoritmo v2.8.7")
st.markdown("### Dashboard Pro: Análisis, Educación y Respaldo")

# --- SECCIÓN 1: CONFIGURACIÓN DEL ENCUENTRO ---
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
            with c1_f: fecha_partido = st.date_input("Fecha", date.today(), key=f"f_{nombre}_{i}")
            with c2: res = st.selectbox("Resultado", ["Ganó", "Perdió"], key=f"res_{nombre}_{i}")
            # --- RANKING DEL RIVAL REINCORPORADO ---
            with c2_r: r_rank = st.number_input("Rank Rival", 1, 1000, 50, key=f"rr_{nombre}_{i}")
            with c3: surf = st.selectbox(f"Superficie", ["Arcilla", "Dura", "Césped", "Indoor"], key=f"s_{nombre}_{i}")
            
            st.markdown("**Estadísticas del Match:**")
            c5, c6, c7, c8, c9, c10a, c10b = st.columns(7)
            with c5: s1_in = st.number_input("% P1S", 0, 100, 65, key=f"p1s_{nombre}_{i}")
            with c6: p1 = st.number_input("% G1S", 0, 100, 70, key=f"p1_{nombre}_{i}")
            with c7: p2 = st.number_input("% G2S", 0, 100, 50, key=f"p2_{nombre}_{i}")
            with c8: d1 = st.number_input("% G1Dev", 0, 100, 30, key=f"d1_{nombre}_{i}")
            with c9: d2 = st.number_input("% G2Dev", 0, 100, 45, key=f"d2_{nombre}_{i}")
            with c10a: bs_sv = st.number_input("Bks Salvados", 0, 50, 2, key=f"bssv_{nombre}_{i}")
            with c10b: bs_enf = st.number_input("Bks Enfrentados", 0, 50, 3, key=f"bsenf_{nombre}_{i}")
            
            partidos.append({"res": res, "p1":p1, "d1":d1, "bs_sv": bs_sv, "bs_enf": bs_enf})
    return partidos

data_j1 = cargar_jugador_full(j1_nom)
st.divider()
data_j2 = cargar_jugador_full(j2_nom)

# --- SECCIÓN 3: PROCESAMIENTO Y POST ---
if st.button("EJECUTAR ANÁLISIS VANTAGE"):
    def calcular_metricas(data):
        total_p1 = sum([p['p1'] for p in data]) / 3
        total_d1 = sum([p['d1'] for p in data]) / 3
        sv = sum([p['bs_sv'] for p in data])
        enf = sum([p['bs_enf'] for p in data])
        bps = (sv / enf * 100) if enf > 0 else 100.0
        return total_p1, total_d1, bps

    avg_j1_p1, avg_j1_d1, bps_j1 = calcular_metricas(data_j1)
    avg_j2_p1, avg_j2_d1, bps_j2 = calcular_metricas(data_j2)

    puntos_j1 = avg_j1_p1 + avg_j1_d1
    puntos_j2 = avg_j2_p1 + avg_j2_d1
    ganador_proy = j1_nom if puntos_j1 > puntos_j2 else j2_nom
    diff_puntos = abs(puntos_j1 - puntos_j2)
    
    st.header

