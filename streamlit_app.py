import streamlit as st
from datetime import date

st.set_page_config(page_title="Tennis Analyst Pro v2.4", layout="wide")

st.title("🎾 Tennis Analyst Pro v2.4")
st.markdown("### Dashboard de Análisis Predictivo Profesional")

# --- SECCIÓN 1: DATOS GENERALES ---
st.header("1. Configuración del Partido")
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    torneo = st.text_input("Torneo", "ATP Madrid")
    superficie_actual = st.selectbox("Superficie Actual", ["Arcilla", "Dura", "Césped"])
with col_m2:
    j1_nom = st.text_input("Jugador 1", "Sonego")
    j1_rank = st.number_input("Rank J1", 1, 1000, 52)
    j1_cuota = st.number_input("Cuota J1", 1.0, 50.0, 1.90)
with col_m3:
    j2_nom = st.text_input("Jugador 2", "Lajovic")
    j2_rank = st.number_input("Rank J2", 1, 1000, 65)
    j2_cuota = st.number_input("Cuota J2", 1.0, 50.0, 1.90)

h2h = st.text_input("Historial H2H (Ej: 1-0)", "0-0")

st.divider()

# --- CARGA DE DATOS COMPLETA ---
def cargar_jugador_full(nombre):
    st.subheader(f"Historial Completo: {nombre}")
    partidos = []
    for i in range(3):
        with st.expander(f"Partido {i+1}", expanded=True):
            c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
            with c1: f = st.date_input(f"Fecha", date.today(), key=f"f_{nombre}_{i}")
            with c2: r = st.text_input(f"Rival", f"Rival {i+1}", key=f"r_{nombre}_{i}")
            with c3: rr = st.number_input(f"Rank Rival", 1, 1000, 100, key=f"rr_{nombre}_{i}")
            with c4: s = st.selectbox(f"Surf", ["Arcilla", "Dura", "Césped"], key=f"s_{nombre}_{i}")
            
            # Métricas que faltaban
            c5, c6, c7, c8, c9, c10 = st.columns(6)
            with c5: p1 = st.number_input("%G1erS", 0, 100, 70, key=f"p1_{nombre}_{i}")
            with c6: p2 = st.number_input("%G2doS", 0, 100, 50, key=f"p2_{nombre}_{i}")
            with c7: d1 = st.number_input("%G1erDev", 0, 100, 30, key=f"d1_{nombre}_{i}")
            with c8: d2 = st.number_input("%G2doDev", 0, 100, 45, key=f"d2_{nombre}_{i}")
            with c9: bs = st.number_input("%BrkSalv", 0, 100, 60, key=f"bs_{nombre}_{i}")
            with c10: res = st.selectbox("Resultado", ["Ganó", "Perdió", "Ganó (Ret)", "Perdió (Ret)"], key=f"res_{nombre}_{i}")
            
            partidos.append({"fecha":f, "p1":p1, "p2":p2, "d1":d1, "d2":d2, "bs":bs, "res":res, "surf":s})
    return partidos

data_j1 = cargar_jugador_full(j1_nom)
st.divider()
data_j2 = cargar_jugador_full(j2_nom)

# --- VEREDICTO FINAL PROFESIONAL ---
if st.button("GENERAR VEREDICTO FINAL"):
    st.header("📋 Veredicto Final del Analista")
    
    # Cálculos de promedios
    def get_avg(data, key): return sum([p[key] for p in data]) / 3
    
    # Análisis comparativo
    avg_p1_j1, avg_p1_j2 = get_avg(data_j1, 'p1'), get_avg(data_j2, 'p1')
    avg_dev_j1 = (get_avg(data_j1, 'd1') + get_avg(data_j1, 'd2')) / 2
    avg_dev_j2 = (get_avg(data_j2, 'd1') + get_avg(data_j2, 'd2')) / 2
    avg_bs_j1, avg_bs_j2 = get_avg(data_j1, 'bs'), get_avg(data_j2, 'bs')

    # Visualización en columnas
    col_v1, col_v2, col_v3 = st.columns(3)
    with col_v1:
        st.metric("Puntos Saque J1 vs J2", f"{avg_p1_j1:.1f}%", f"{avg_p1_j1 - avg_p1_j2:.1f}%")
        st.write("**Fortaleza al Saque**")
    with col_v2:
        st.metric("Puntos Devolución J1 vs J2", f"{avg_dev_j1:.1f}%", f"{avg_dev_j1 - avg_dev_j2:.1f}%")
        st.write("**Agresividad al Resto**")
    with col_v3:
        st.metric("Break Points Salvados", f"{avg_bs_j1:.1f}%", f"{avg_bs_j1 - avg_bs_j2:.1f}%")
        st.write("**Capacidad de Supervivencia**")

    st.divider()

    # INFORME NARRATIVO
    informe = f"**INFORME DE VALOR:** El partido en {superficie_actual} entre {j1_nom} y {j2_nom} "
    
    # Lógica de ventaja técnica
    if avg_p1_j1 > avg_p1_j2 + 5 and avg_dev_j1 > avg_dev_j2:
        informe += f"muestra una superioridad técnica clara de {j1_nom} en ambas facetas del juego. "
    elif avg_dev_j2 > avg_dev_j1 + 5:
        informe += f"pone en peligro a {j1_nom} debido a la gran capacidad de devolución de {j2_nom}. "
    
    # Lógica de Clutch (Break points)
    if avg_bs_j1 > 70:
        informe += f"{j1_nom} viene demostrando una mentalidad fría salvando el {avg_bs_j1:.1f}% de sus break points. "
    
    # Conclusión sobre la cuota
    if j1_cuota > 2.0 and avg_p1_j1 > avg_p1_j2:
        informe += f"**Veredicto:** Existe VALOR en la cuota de {j1_nom} ({j1_cuota}). Las estadísticas de saque respaldan un resultado distinto al que marcan las casas."
    else:
        informe += f"**Veredicto:** El mercado está bien ajustado. Partido de pronóstico reservado, ideal para seguir en Vivo."

    st.info(informe)


