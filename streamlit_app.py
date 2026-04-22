import streamlit as st

st.set_page_config(page_title="Tennis Analyst Pro v2.2", layout="wide")

st.title("🎾 Tennis Analyst Pro v2.2")
st.markdown("### Análisis Profesional: Contexto, H2H y Condición Física")

# --- SECCIÓN 1: DATOS DEL PARTIDO ACTUAL Y H2H ---
st.header("1. Información del Encuentro")
col_match1, col_match2, col_match3 = st.columns(3)
with col_match1:
    torneo = st.text_input("Torneo", "ATP Madrid")
    superficie_actual = st.selectbox("Superficie Actual", ["Arcilla", "Dura", "Césped"])
    h2h_info = st.text_input("Historial H2H (Ej: 2-1 a favor de Sonego)", "0-0")
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
        c1, c2, c3, c4, c5, c6, c7, c8 = st.columns([2, 1, 1, 1, 1, 1, 1, 1.5])
        with c1: rival = st.text_input(f"Rival P{i+1}", f"Rival {i+1}", key=f"r_{nombre}_{i}")
        with c2: r_rank = st.number_input(f"Rank R", 1, 1000, 100, key=f"rr_{nombre}_{i}")
        with c3: surf = st.selectbox(f"Surf", ["Arcilla", "Dura", "Césped"], key=f"s_{nombre}_{i}")
        with c4: s1 = st.number_input(f"%1erS", 0, 100, 65, key=f"s1_{nombre}_{i}")
        with c5: p1 = st.number_input(f"%G1er", 0, 100, 70, key=f"p1_{nombre}_{i}")
        with c6: p2 = st.number_input(f"%G2do", 0, 100, 50, key=f"p2_{nombre}_{i}")
        with c7: df = st.number_input(f"DF", 0, 20, 2, key=f"df_{nombre}_{i}")
        with c8: res = st.selectbox(f"Resultado", ["Ganó", "Perdió", "Ganó (Retiro)", "Perdió (Retiro)"], key=f"res_{nombre}_{i}")
        
        lista_partidos.append({
            "rival_rank": r_rank, "surf": surf, "s1": s1, "p1": p1, "p2": p2, "df": df, "resultado": res
        })
    return lista_partidos

historial_j1 = cargar_historial(j1_nombre)
st.divider()
historial_j2 = cargar_historial(j2_nombre)

# --- LÓGICA DEL VEREDICTO v2.2 ---
if st.button("GENERAR ANÁLISIS PROFESIONAL"):
    st.header("📝 Informe Técnico del Especialista")
    
    # Detección de Retiros recientes
    retiros_j1 = [p for p in historial_j1 if "Retiro" in p['resultado']]
    retiros_j2 = [p for p in historial_j2 if "Retiro" in p['resultado']]
    
    # Promedios
    prom_p1_j1 = sum([p['p1'] for p in historial_j1]) / 3
    prom_p1_j2 = sum([p['p1'] for p in historial_j2]) / 3
    
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.subheader("📊 Comparativa")
        st.write(f"**H2H:** {h2h_info}")
        st.write(f"**Efectividad 1er Saque:** {j1_nombre} ({prom_p1_j1:.1f}%) vs {j2_nombre} ({prom_p1_j2:.1f}%)")

    with col_res2:
        st.subheader("⚠️ Alertas de Integridad")
        if retiros_j1:
            st.error(f"OJO: {j1_nombre} tuvo un partido con RETIRO recientemente. Verificar estado físico.")
        if retiros_j2:
            st.error(f"OJO: {j2_nombre} tuvo un partido con RETIRO recientemente. Verificar estado físico.")
        if not retiros_j1 and not retiros_j2:
            st.success("Ambos jugadores parecen llegar físicamente íntegros (sin retiros recientes).")

    st.divider()
    
    # Veredicto Narrativo
    analisis = f"Encuentro en {torneo} con un H2H de {h2h_info}. "
    if "Ganó (Retiro)" in [p['resultado'] for p in historial_j1]:
        analisis += f"Atención: una de las victorias de {j1_nombre} fue por retiro, lo que podría sesgar sus estadísticas al alza. "
    
    if prom_p1_j1 > prom_p1_j2 + 7:
        analisis += f"Técnicamente, {j1_nombre} llega con un servicio mucho más sólido. "
    
    analisis += f"Dada la superficie de {superficie_actual} y las cuotas ({j1_cuota} / {j2_cuota}), "
    
    if j1_cuota > 2.0 and prom_p1_j1 > prom_p1_j2:
        analisis += f"hay una oportunidad de valor en {j1_nombre}."
    else:
        analisis += "se recomienda cautela o buscar mercados alternativos."
        
    st.info(analisis)



