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

# --- LÓGICA DEL VEREDICTO PROFESIONAL ---
if st.button("GENERAR ANÁLISIS PROFESIONAL"):
    st.header("📝 Veredicto Técnico Final")
    
    # Cálculos promedios
    prom_p1_j1 = sum([p['p1'] for p in historial_j1]) / 3
    prom_p1_j2 = sum([p['p1'] for p in historial_j2]) / 3
    
    # Chequeo de superficie (Adaptación)
    surf_check_j1 = sum([1 for p in historial_j1 if p['surf'] == superficie_actual])
    surf_check_j2 = sum([1 for p in historial_j2 if p['surf'] == superficie_actual])

    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.subheader("📊 Comparativa de Rendimiento")
        if prom_p1_j1 > prom_p1_j2:
            st.write(f"- **Dominio de Saque:** {j1_nombre} presenta mayor efectividad con el primer servicio ({prom_p1_j1:.1f}% vs {prom_p1_j2:.1f}%).")
        else:
            st.write(f"- **Dominio de Saque:** {j2_nombre} lidera la efectividad con el primer servicio.")
            
        st.write(f"- **Adaptación a {superficie_actual}:** {j1_nombre} jugó {surf_check_j1}/3 partidos recientes en esta superficie; {j2_nombre} jugó {surf_check_j2}/3.")

    with col_v2:
        st.subheader("💡 Análisis de Valor (Value Bet)")
        favorito_ia = j1_nombre if j1_cuota < j2_cuota else j2_nombre
        st.write(f"- **Mercado:** Las cuotas sugieren un partido de {abs(j1_cuota - j2_cuota):.2f} de diferencia.")
        
    st.info(f"**Sugerencia de Especialista:** El cruce entre {j1_nombre} ({j1_rank}) y {j2_nombre} ({j2_rank}) en {superficie_actual} se define por la estabilidad. " + 
            (f"{j1_nombre} llega con mejor rodaje específico." if surf_check_j1 > surf_check_j2 else f"{j2_nombre} parece estar mejor adaptado."))



