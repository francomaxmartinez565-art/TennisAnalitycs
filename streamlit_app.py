import streamlit as st
from datetime import date

# Configuración de la App
st.set_page_config(page_title="Vantaje Algoritmo v2.8.4", layout="wide")

st.title("🎾 Vantaje Algoritmo v2.8.4")
st.markdown("### Dashboard de Análisis Predictivo & Educación Estratégica")

# --- SECCIÓN 1: CONFIGURACIÓN DEL ENCUENTRO ---
st.header("1. Configuración del Encuentro")
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    torneo = st.text_input("Torneo", "ATP Madrid")
    superficie_actual = st.selectbox("Superficie Actual", ["Arcilla", "Dura", "Césped", "Indoor"])
    h2h = st.text_input("Historial H2H", "0-0")
with col_m2:
    j1_nom = st.text_input("Jugador 1", "R. Jódar")
    j1_rank = st.number_input("Rank J1", 1, 1000, 42) 
    j1_cuota = st.number_input("Cuota J1", 1.0, 50.0, 2.50)
with col_m3:
    j2_nom = st.text_input("Jugador 2", "A. De Miñaur")
    j2_rank = st.number_input("Rank J2", 1, 1000, 8) 
    j2_cuota = st.number_input("Cuota J2", 1.0, 50.0, 1.50)

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
            with c2: res = st.selectbox("Resultado", ["Ganó", "Perdió", "Gano por retiro", "Perdio por retiro"], key=f"res_{nombre}_{i}")
            with c2_r: r_rank = st.number_input("Rank Rival", 1, 1000, 100, key=f"rr_{nombre}_{i}")
            with c3: surf = st.selectbox(f"Superficie", ["Arcilla", "Dura", "Césped", "Indoor"], key=f"s_{nombre}_{i}")
            
            st.markdown("**Estadísticas del Match:**")
            c5, c6, c7, c8, c9, c10a, c10b = st.columns([1, 1, 1, 1, 1, 1, 1])
            with c5: s1_in = st.number_input("% P1S", 0, 100, 65, key=f"p1s_{nombre}_{i}")
            with c6: p1 = st.number_input("% G1S", 0, 100, 70, key=f"p1_{nombre}_{i}")
            with c7: p2 = st.number_input("% G2S", 0, 100, 50, key=f"p2_{nombre}_{i}")
            with c8: d1 = st.number_input("% G1Dev", 0, 100, 30, key=f"d1_{nombre}_{i}")
            with c9: d2 = st.number_input("% G2Dev", 0, 100, 45, key=f"d2_{nombre}_{i}")
            with c10a: bs_sv = st.number_input("Bks Salvados", 0, 50, 2, key=f"bssv_{nombre}_{i}")
            with c10b: bs_enf = st.number_input("Bks Enfrentados", 0, 50, 3, key=f"bsenf_{nombre}_{i}")
            
            partidos.append({"res": res, "s1in":s1_in, "p1":p1, "p2":p2, "d1":d1, "d2":d2, "bs_sv": bs_sv, "bs_enf": bs_enf})
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
            'G1S': sum([p['p1'] for p in data]) / 3,
            'G2S': sum([p['p2'] for p in data]) / 3,
            'G1Dev': sum([p['d1'] for p in data]) / 3,
            'BPS_pct': (total_bs_sv / total_bs_enf * 100) if total_bs_enf > 0 else 100.0
        }

    avg_j1 = get_avg_vantage(data_j1)
    avg_j2 = get_avg_vantage(data_j2)

    # Lógica de Poder Combinado
    puntos_j1 = avg_j1['G1S'] + avg_j1['G1Dev']
    puntos_j2 = avg_j2['G1S'] + avg_j2['G1Dev']
    diff_puntos = abs(puntos_j1 - puntos_j2)
    ganador_proy = j1_nom if puntos_j1 > puntos_j2 else j2_nom
    underdog = j2_nom if ganador_proy == j1_nom else j1_nom

    # Visualización de Métricas
    st.subheader("📊 Métricas Comparativas Proyectadas")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("G1S (Poder)", f"{avg_j1['G1S']:.1f}%", f"{avg_j1['G1S'] - avg_j2['G1S']:.1f}%")
    c2.metric("G2S (Seguridad)", f"{avg_j1['G2S']:.1f}%", f"{avg_j1['G2S'] - avg_j2['G2S']:.1f}%")
    c3.metric("G1Dev (Resto)", f"{avg_j1['G1Dev']:.1f}%", f"{avg_j1['G1Dev'] - avg_j2['G1Dev']:.1f}%")
    c4.metric("BPS (Resiliencia)", f"{avg_j1['BPS_pct']:.1f}%", f"{avg_j1['BPS_pct'] - avg_j2['BPS_pct']:.1f}%")

    st.divider()

    # Variables de Valor y Hándicaps
    st.subheader("🎯 Variables de Valor y Hándicaps")
    col_v1, col_v2, col_v3 = st.columns(3)

    with col_v1:
        st.markdown("**Predicción y Score**")
        score = "2-0" if diff_puntos > 15 else "2-1 o Cerrado"
        st.success(f"🏆 WIN {ganador_proy} ({score})")
        if avg_j1['G1S'] > 75 and avg_j2['G1S'] > 75:
            st.error("🚨 ALTA Probabilidad de Tie-break")

    with col_v2:
        st.markdown("**Hándicaps Sugeridos**")
        handicap = f"{underdog} +3.5" if diff_puntos < 6 else f"{ganador_proy} -2.5"
        st.write(f"Sugerencia: {handicap} Juegos")

    with col_v3:
        st.markdown("**Línea de Juegos**")
        linea = "Over 22.5" if (avg_j1['G1S'] + avg_j2['G1S'] > 140) else "Under 21.5"
        st.info(f"📈 {linea} Games")

    # Argumento Técnico
    st.markdown("---")
    st.markdown("### 📝 Argumento Estratégico")
    st.info(f"""
    El análisis proyecta valor en **{ganador_proy}**. El diferencial de {diff_puntos:.1f}% en eficiencia 
    bajo las condiciones de **{superficie_actual}** indica un mejor control de los puntos clave. 
    La clave será la protección del primer servicio para neutralizar el resto de **{underdog}**.
    """)

    # Píldora Educativa
    st.divider()
    st.subheader("🎓 Píldora Educativa Vantaje")
    
    if avg_j1['G1S'] > 75 or avg_j2['G1S'] > 75:
        concepto = "Dominio del Primer Servicio"
        leccion = "Un G1S superior al 75% indica que el sacador dicta el ritmo. En estos casos, los quiebres son raros y los partidos suelen irse a sets largos o tie-breaks."
    elif abs(avg_j1['G1Dev'] - avg_j2['G1Dev']) > 15:
        concepto = "Diferencial de Retorno"
        leccion = "Si un jugador devuelve significativamente mejor que el otro, el ranking importa menos. La capacidad de poner la pelota en juego y generar presión constante suele romper la resistencia del sacador."
    else:
        concepto = "Resiliencia (BPS)"
        leccion = "El Break Point Saved (BPS) es una métrica de jerarquía mental. Salvar puntos de quiebre en momentos críticos es lo que permite cubrir hándicaps ajustados."

    with st.expander(f"📘 Concepto: {concepto}", expanded=True):
        st.write(leccion)
