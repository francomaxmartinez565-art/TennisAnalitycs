import streamlit as st
from datetime import date

st.set_page_config(page_title="Tennis Analyst Pro v2.3", layout="wide")

st.title("🎾 Tennis Analyst Pro v2.3")
st.markdown("### Análisis Profesional: Cronología, H2H y Condición Física")

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

# --- FUNCIÓN PARA CARGAR HISTORIAL CON FECHAS ---
def cargar_historial(nombre):
    st.subheader(f"Últimos 3 partidos de {nombre}")
    lista_partidos = []
    
    for i in range(3):
        st.write(f"**Partido {i+1}**")
        c1, c2, c3, c4, c5, c6, c7, c8, c9 = st.columns([1.5, 1.5, 1, 1, 1, 1, 1, 0.8, 1.5])
        with c1: fecha = st.date_input(f"Fecha P{i+1}", date.today(), key=f"f_{nombre}_{i}")
        with c2: rival = st.text_input(f"Rival P{i+1}", f"Rival {i+1}", key=f"r_{nombre}_{i}")
        with c3: r_rank = st.number_input(f"Rank R", 1, 1000, 100, key=f"rr_{nombre}_{i}")
        with c4: surf = st.selectbox(f"Surf", ["Arcilla", "Dura", "Césped"], key=f"s_{nombre}_{i}")
        with c5: s1 = st.number_input(f"%1erS", 0, 100, 65, key=f"s1_{nombre}_{i}")
        with c6: p1 = st.number_input(f"%G1er", 0, 100, 70, key=f"p1_{nombre}_{i}")
        with c7: p2 = st.number_input(f"%G2do", 0, 100, 50, key=f"p2_{nombre}_{i}")
        with c8: df = st.number_input(f"DF", 0, 20, 2, key=f"df_{nombre}_{i}")
        with c9: res = st.selectbox(f"Resultado", ["Ganó", "Perdió", "Ganó (Retiro)", "Perdió (Retiro)"], key=f"res_{nombre}_{i}")
        
        lista_partidos.append({
            "fecha": fecha, "rival_rank": r_rank, "surf": surf, "s1": s1, "p1": p1, "p2": p2, "df": df, "resultado": res
        })
    return lista_partidos

historial_j1 = cargar_historial(j1_nombre)
st.divider()
historial_j2 = cargar_historial(j2_nombre)

# --- LÓGICA DEL VEREDICTO v2.3 ---
if st.button("GENERAR ANÁLISIS PROFESIONAL"):
    st.header("📝 Informe Técnico del Especialista")
    
    # Cálculo de inactividad
    dias_inactivo_j1 = (date.today() - historial_j1[0]['fecha']).days
    dias_inactivo_j2 = (date.today() - historial_j2[0]['fecha']).days
    
    # Promedios
    prom_p1_j1 = sum([p['p1'] for p in historial_j1]) / 3
    prom_p1_j2 = sum([p['p2'] for p in historial_j2]) / 3 # Corregido para comparar
    
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        st.subheader("📊 Comparativa y Ritmo")
        st.write(f"**H2H:** {h2h_info}")
        st.write(f"**Último partido {j1_nombre}:** Hace {dias_inactivo_j1} días.")
        st.write(f"**Último partido {j2_nombre}:** Hace {dias_inactivo_j2} días.")

    with col_res2:
        st.subheader("⚠️ Alertas de Contexto")
        if dias_inactivo_j1 > 15:
            st.warning(f"RITMO: {j1_nombre} lleva más de 2 semanas sin competir.")
        if dias_inactivo_j2 > 15:
            st.warning(f"RITMO: {j2_nombre} lleva más de 2 semanas sin competir.")
        
        # Alertas de Retiro
        retiros = [p for p in historial_j1 + historial_j2 if "Retiro" in p['resultado']]
        if retiros:
            st.error("Se detectaron abandonos recientes en el historial.")

    st.divider()
    
    # Veredicto
    analisis = f"Análisis para {torneo}. "
    if dias_inactivo_j1 < dias_inactivo_j2 - 7:
        analisis += f"{j1_nombre} llega con mucho más ritmo de competencia actual. "
    
    analisis += f"En términos de potencia, el diferencial de primer saque es de {abs(prom_p1_j1 - prom_p1_j2):.1f}%. "
    
    if j1_cuota > 2.0 and dias_inactivo_j1 < 7:
        analisis += f"La cuota de {j1_nombre} es atractiva considerando su actividad reciente."
        
    st.info(analisis)



