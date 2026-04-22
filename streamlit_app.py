import streamlit as st

st.set_page_config(page_title="Tennis Analyst Pro v2.0", layout="wide")

st.title("🎾 Tennis Analyst Pro v2.0")
st.markdown("### Análisis Profesional de Rendimiento y Contexto")

# --- SECCIÓN 1: DATOS DEL PARTIDO ACTUAL ---
st.header("1. Información del Encuentro")
col_match1, col_match2, col_match3 = st.columns(3)
with col_match1:
    torneo = st.text_input("Torneo", "ATP Madrid")
    superficie_actual = st.selectbox("Superficie Actual", ["Arcilla", "Dura", "Césped"])
with col_match2:
    j1_nombre = st.text_input("Jugador 1", "Sonego")
    j1_rank = st.number_input("Ranking J1", 1, 1000, 52)
    j1_cuota = st.number_input("Cuota J1", 1.0, 50.0, 1.90)
with col_match3:
    j2_nombre = st.text_input("Jugador 2", "Lajovic")
    j2_rank = st.number_input("Ranking J2", 1, 1000, 65)
    j2_cuota = st.number_input("Cuota J2", 1.0, 50.0, 1.90)

st.divider()

# --- FUNCIÓN PARA CARGAR HISTORIAL ---
def cargar_historial(nombre):
    st.subheader(f"Últimos 3 partidos de {nombre}")
    lista_partidos = []
    
    for i in range(3):
        st.write(f"**Partido {i+1}**")
        c1, c2, c3, c4, c5, c6, c7, c8 = st.columns([2, 1, 1, 1, 1, 1, 1, 1])
        with c1: rival = st.text_input(f"Rival P{i+1}", f"Rival {i+1}", key=f"r_{nombre}_{i}")
        with c2: r_rank = st.number_input(f"Rank R", 1, 1000, 100, key=f"rr_{nombre}_{i}")
        with c3: surf = st.selectbox(f"Surf", ["Arcilla", "Dura", "Césped"], key=f"s_{nombre}_{i}")
        with c4: s1 = st.number_input(f"%1erS", 0, 100, 65, key=f"s1_{nombre}_{i}")
        with c5: p1 = st.number_input(f"%G1er", 0, 100, 70, key=f"p1_{nombre}_{i}")
        with c6: p2 = st.number_input(f"%G2do", 0, 100, 50, key=f"p2_{nombre}_{i}")
        with c7: df = st.number_input(f"DF", 0, 20, 2, key=f"df_{nombre}_{i}")
        with c8: res = st.selectbox(f"Res", ["Ganó", "Perdió"], key=f"res_{nombre}_{i}")
        
        lista_partidos.append({
            "rival_rank": r_rank, "surf": surf, "s1": s1, "p1": p1, "p2": p2, "df": df, "resultado": res
        })
    return lista_partidos

historial_j1 = cargar_historial(j1_nombre)
st.divider()
historial_j2 = cargar_historial(j2_nombre)

# --- LÓGICA DEL VEREDICTO PROFESIONAL v2.1 ---
if st.button("GENERAR ANÁLISIS PROFESIONAL"):
    st.header("📝 Informe Técnico del Especialista")
    
    # Cálculos promedios
    prom_p1_j1 = sum([p['p1'] for p in historial_j1]) / 3
    prom_p2_j1 = sum([p['p2'] for p in historial_j1]) / 3
    prom_df_j1 = sum([p['df'] for p in historial_j1]) / 3
    
    prom_p1_j2 = sum([p['p1'] for p in historial_j2]) / 3
    prom_p2_j2 = sum([p['p2'] for p in historial_j2]) / 3
    prom_df_j2 = sum([p['df'] for p in historial_j2]) / 3
    
    # Análisis de Superficie
    surf_j1 = sum([1 for p in historial_j1 if p['surf'] == superficie_actual])
    surf_j2 = sum([1 for p in historial_j2 if p['surf'] == superficie_actual])

    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.subheader("📊 Métricas de Rendimiento")
        st.write(f"**Servicio:** {j1_nombre} gana el {prom_p1_j1:.1f}% con el primero, mientras que {j2_nombre} está en {prom_p1_j2:.1f}%.")
        st.write(f"**Segundos Saques:** {j1_nombre} ({prom_p2_j1:.1f}%) vs {j2_nombre} ({prom_p2_j2:.1f}%).")
        st.write(f"**Disciplina:** Promedio de DFs: {prom_df_j1:.1f} vs {prom_df_j2:.1f}.")

    with col_res2:
        st.subheader("🎯 Factores de Decisión")
        # Detección de Value Bet
        if prom_p1_j1 > prom_p1_j2 + 5 and j1_cuota > 1.80:
            st.success(f"VALOR DETECTADO: {j1_nombre} tiene métricas superiores a lo que indica su cuota de {j1_cuota}.")
        
        # Alerta de Superficie
        if surf_j1 < 2:
            st.warning(f"ADAPTACIÓN: {j1_nombre} solo tiene {surf_j1} partido(s) reciente(s) en {superficie_actual}.")

    # Párrafo Final Estilo Profesional
    st.divider()
    resumen_ia = f"El duelo entre {j1_nombre} (Rank {j1_rank}) y {j2_nombre} (Rank {j2_rank}) presenta un escenario "
    if abs(prom_p1_j1 - prom_p1_j2) < 4:
        resumen_ia += "de máxima paridad en los servicios. La clave estará en los puntos ganados con el segundo saque, donde "
    else:
        resumen_ia += f"donde {j1_nombre if prom_p1_j1 > prom_p1_j2 else j2_nombre} llega con una ventaja mecánica en potencia. "
    
    resumen_ia += f"Considerando la cuota de {j1_cuota} vs {j2_cuota}, el mercado espera un partido cerrado. "
    resumen_ia += f"Recomendación técnica: Evaluar {'Handicap' if abs(j1_rank - j2_rank) < 20 else 'Ganador directo'}."
    
    st.info(resumen_ia)




