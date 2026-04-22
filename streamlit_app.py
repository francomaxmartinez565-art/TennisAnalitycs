import streamlit as st

# Título y configuración
st.set_page_config(page_title="Analista Tenis Pro", layout="wide")
st.title("🎾 Mi Analista de Tenis")
st.subheader("Ingresa los datos de los últimos 3 partidos")

# Entrada de Datos Generales
col_info1, col_info2 = st.columns(2)
with col_info1:
    torneo = st.text_input("Torneo", "ATP Madrid")
with col_info2:
    superficie = st.selectbox("Superficie", ["Arcilla", "Dura", "Césped"])

st.divider()

# Función para crear las columnas de carga
def cargar_jugador(nombre_label):
    nombre = st.text_input(f"Nombre del {nombre_label}", nombre_label)
    st.write(f"Estadísticas (Último | Penúltimo | Antepenúltimo)")
    
    c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
    with c1: saque1 = st.text_input(f"%1erS", "60, 60, 60", key=f"s1_{nombre_label}")
    with c2: pts1 = st.text_input(f"%P1erServ", "70, 70, 70", key=f"p1_{nombre_label}")
    with c3: pts2 = st.text_input(f"%P2doServ", "40, 40, 40", key=f"p2_{nombre_label}")
    with c4: dev1 = st.text_input(f"PG1Dev", "30, 30, 30", key=f"d1_{nombre_label}")
    with c5: dev2 = st.text_input(f"PG2Dev", "40, 40, 40", key=f"d2_{nombre_label}")
    with c6: df = st.text_input(f"DF", "2, 2, 2", key=f"df_{nombre_label}")
    with c7: brk = st.text_input(f"BrkSalv", "2/4, 2/4, 2/4", key=f"bk_{nombre_label}")

    # Procesar promedios simples para el veredicto
    def get_avg(txt):
        try: return sum([float(x.strip()) for x in txt.split(",")]) / 3
        except: return 0
    
    return {
        "nombre": nombre,
        "avg_1er": get_avg(pts1),
        "avg_2do": get_avg(pts2),
        "avg_df": get_avg(df),
        "last_2do": float(pts2.split(",")[0]) if "," in pts2 else 0
    }

# Carga de los dos jugadores
jugador_a = cargar_jugador("Jugador 1")
st.divider()
jugador_b = cargar_jugador("Jugador 2")

st.divider()

if st.button("GENERAR VEREDICTO"):
    st.header("📋 Veredicto de la IA")
    
    res = f"Analizando partido en {torneo} ({superficie}). "
    
    # Lógica de comparación
    if jugador_a['avg_1er'] > jugador_b['avg_1er'] + 5:
        res += f"{jugador_a['nombre']} tiene un primer servicio más dominante. "
    elif jugador_b['avg_1er'] > jugador_a['avg_1er'] + 5:
        res += f"{jugador_b['nombre']} domina mejor con el primer saque. "
    
    if jugador_a['avg_df'] > 4:
        res += f"Ojo: {jugador_a['nombre']} es muy inestable (promedia {jugador_a['avg_df']:.1f} DF). "
    
    if jugador_a['last_2do'] < 40:
        res += f"Alerta: {jugador_a['nombre']} sufrió mucho con su segundo saque en el último partido ({jugador_a['last_2do']}%). "

    st.info(res)
    
    # Sugerencia
    if jugador_a['avg_1er'] > jugador_b['avg_1er'] and jugador_a['avg_df'] < jugador_b['avg_df']:
        st.success(f"Sugerencia Técnica: Victoria de {jugador_a['nombre']}.")
    elif jugador_b['avg_1er'] > jugador_a['avg_1er'] and jugador_b['avg_df'] < jugador_a['avg_df']:
        st.success(f"Sugerencia Técnica: Victoria de {jugador_b['nombre']}.")
    else:
        st.warning("Pronóstico Reservado: Los números son muy parejos o contradictorios.")

