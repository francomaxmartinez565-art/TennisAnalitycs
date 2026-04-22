import streamlit as st
from datetime import date

st.set_page_config(page_title="Tennis Analyst Pro v2.6", layout="wide")

st.title("🎾 Tennis Analyst Pro v2.6")
st.markdown("### Dashboard de Análisis Predictivo Profesional")

# --- SECCIÓN 1: CONFIGURACIÓN DEL PARTIDO ---
st.header("1. Configuración del Encuentro")
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    torneo = st.text_input("Torneo", "ATP Madrid")
    superficie_actual = st.selectbox("Superficie Actual", ["Arcilla", "Dura", "Césped", "Indoor"])
    h2h = st.text_input("Historial H2H (Ej: 1-0)", "0-0")
with col_m2:
    j1_nom = st.text_input("Jugador 1", "")
    j1_rank = st.number_input("Rank J1", 1, 1000, 52)
    j1_cuota = st.number_input("Cuota J1", 1.0, 50.0, 1.90)
with col_m3:
    j2_nom = st.text_input("Jugador 2", "")
    j2_rank = st.number_input("Rank J2", 1, 1000, 65)
    j2_cuota = st.number_input("Cuota J2", 1.0, 50.0, 1.90)

st.divider()

# --- CARGA DE DATOS COMPLETA ---
def cargar_jugador_full(nombre):
    st.subheader(f"Historial Completo: {nombre}")
    partidos = []
    for i in range(3):
        with st.expander(f"Partido {i+1}", expanded=True):
            c1, c2, c3, c4 = st.columns([1.5, 1.5, 1, 1])
            with c1: f = st.date_input(f"Fecha", date.today(), key=f"f_{nombre}_{i}")
            with c2: r = st.text_input(f"Rival", f"Rival {i+1}", key=f"r_{nombre}_{i}")
            with c3: rr = st.number_input(f"Rank Rival", 1, 1000, 100, key=f"rr_{nombre}_{i}")
            with c4: s = st.selectbox(f"Surf", ["Arcilla", "Dura", "Césped"], key=f"s_{nombre}_{i}")
            
            # Métricas Completas (Incluyendo %1erS)
            c5, c6, c7, c8, c9, c10, c11, c12 = st.columns(8)
            with c5: s1_in = st.number_input("%1erS (In)", 0, 100, 65, key=f"s1in_{nombre}_{i}")
            with c6: p1 = st.number_input("%G1erS", 0, 100, 70, key=f"p1_{nombre}_{i}")
            with c7: p2 = st.number_input("%G2doS", 0, 100, 50, key=f"p2_{nombre}_{i}")
            with c8: d1 = st.number_input("%G1erDev", 0, 100, 30, key=f"d1_{nombre}_{i}")
            with c9: d2 = st.number_input("%G2doDev", 0, 100, 45, key=f"d2_{nombre}_{i}")
            with c10: bs = st.number_input("%BrkSalv", 0, 100, 60, key=f"bs_{nombre}_{i}")
            with c11: df = st.number_input("DF", 0, 30, 2, key=f"df_{nombre}_{i}")
            with c12: res = st.selectbox("Resultado", ["Ganó", "Perdió", "Ganó (Ret)", "Perdió (Ret)"], key=f"res_{nombre}_{i}")
            
            partidos.append({"fecha":f, "s1in":s1_in, "p1":p1, "p2":p2, "d1":d1, "d2":d2, "bs":bs, "df":df, "res":res, "surf":s})
    return partidos

data_j1 = cargar_jugador_full(j1_nom)
st.divider()
data_j2 = cargar_jugador_full(j2_nom)

# --- VEREDICTO FINAL PROFESIONAL ---
if st.button("GENERAR VEREDICTO FINAL"):
    st.header("📋 Veredicto Final del Analista")
    
    def get_avg(data, key): return sum([p[key] for p in data]) / 3
    
    # Cálculos de Promedios
    avg_s1in_j1, avg_s1in_j2 = get_avg(data_j1, 's1in'), get_avg(data_j2, 's1in')
    avg_p1_j1, avg_p1_j2 = get_avg(data_j1, 'p1'), get_avg(data_j2, 'p1')
    avg_dev_j1 = (get_avg(data_j1, 'd1') + get_avg(data_j1, 'd2')) / 2
    avg_dev_j2 = (get_avg(data_j2, 'd1') + get_avg(data_j2, 'd2')) / 2
    avg_bs_j1, avg_bs_j2 = get_avg(data_j1, 'bs'), get_avg(data_j2, 'bs')
    avg_df_j1, avg_df_j2 = get_avg(data_j1, 'df'), get_avg(data_j2, 'df')

    # Visualización de KPIs comparativos
    c_kpi1, c_kpi2, c_kpi3, c_kpi4 = st.columns(4)
    c_kpi1.metric("Fiabilidad 1er Saque (% In)", f"{avg_s1in_j1:.1f}%", f"{avg_s1in_j1 - avg_s1in_j2:.1f}%")
    c_kpi2.metric("Puntos Ganados 1er S", f"{avg_p1_j1:.1f}%", f"{avg_p1_j1 - avg_p1_j2:.1f}%")
    c_kpi3.metric("Eficacia al Resto (Prom)", f"{avg_dev_j1:.1f}%", f"{avg_dev_j1 - avg_dev_j2:.1f}%")
    c_kpi4.metric("Salvado de Breaks", f"{avg_bs_j1:.1f}%", f"{avg_bs_j1 - avg_bs_j2:.1f}%")

    st.divider()

    # INFORME NARRATIVO PROFESIONAL
    informe = f"**INFORME TÉCNICO:** El cruce entre {j1_nom} y {j2_nom} en {torneo} ({superficie_actual}). "
    
    # Análisis de Saque: Cantidad vs Calidad
    if avg_s1in_j1 > 70 and avg_p1_j1 > 75:
        informe += f"{j1_nom} domina con un saque de alta precisión y efectividad. "
    elif avg_s1in_j1 > 75 and avg_p1_j1 < 60:
        informe += f"Ojo: {j1_nom} mete muchos primeros pero no hace daño con ellos. "

    # Disciplina (Dobles Faltas)
    if avg_df_j1 > 5:
        informe += f"Alerta de inestabilidad para {j1_nom} con {avg_df_j1:.1f} DFs por partido. "

    # Conclusión Final
    if j1_cuota > 2.10 and avg_p1_j1 > avg_p1_j2 + 5:
        st.success(informe + f"**VEREDICTO: VALUE BET en {j1_nom}.** Los números de saque superan la expectativa de la cuota.")
    elif abs(avg_p1_j1 - avg_p1_j2) < 4 and abs(avg_dev_j1 - avg_dev_j2) < 4:
        st.warning(informe + "**VEREDICTO: PARTIDO TRABADO. Las métricas son idénticas, se proyecta un match largo o Over de games.**")
    else:
        st.info(informe + f"**VEREDICTO: El mercado refleja fielmente la estadística actual.**")



