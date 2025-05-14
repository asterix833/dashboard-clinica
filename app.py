
import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("datos_dashboard_clinica.csv")

df = cargar_datos()

st.set_page_config(page_title="Dashboard Clínica Di Pietro", layout="wide")
st.title("📊 Dashboard de Conversaciones - Clínica Di Pietro")

# Filtros
col1, col2, col3 = st.columns(3)

with col1:
    tratamientos = st.multiselect("Filtrar por tratamiento", options=sorted(df.tratamiento.unique()), default=sorted(df.tratamiento.unique()))

with col2:
    fecha_inicio = pd.to_datetime(df.fecha_inicio)
    fecha_min = fecha_inicio.min()
    fecha_max = fecha_inicio.max()
    fechas = st.slider("Rango de fechas", min_value=fecha_min, max_value=fecha_max, value=(fecha_min, fecha_max))

with col3:
    solo_confirmados = st.checkbox("Solo turnos confirmados", value=False)

# Aplicar filtros
filtro = (
    df["tratamiento"].isin(tratamientos)
    & (pd.to_datetime(df["fecha_inicio"]) >= fechas[0])
    & (pd.to_datetime(df["fecha_inicio"]) <= fechas[1])
)
if solo_confirmados:
    filtro &= df["turno_confirmado"]

df_filtrado = df[filtro]

# KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total conversaciones", len(df_filtrado))

with col2:
    st.metric("Turnos confirmados", df_filtrado["turno_confirmado"].sum())

with col3:
    st.metric("Con urgencia", df_filtrado["urgencia"].sum())

with col4:
    st.metric("Con obra social", df_filtrado["obra_social"].sum())

# Gráficos
st.subheader("📈 Conversaciones por Tratamiento")
g1 = px.bar(df_filtrado.groupby("tratamiento").size().reset_index(name="cantidad"),
            x="tratamiento", y="cantidad", title="Cantidad de Conversaciones por Tratamiento")
st.plotly_chart(g1, use_container_width=True)

st.subheader("📊 Tasa de Turnos Confirmados por Tratamiento")
df_turno = df_filtrado.groupby("tratamiento")["turno_confirmado"].mean().reset_index()
df_turno["tasa"] = (df_turno["turno_confirmado"] * 100).round(2)
g2 = px.bar(df_turno, x="tratamiento", y="tasa",
            labels={"tasa": "% confirmados"}, title="% de Turnos Confirmados")
st.plotly_chart(g2, use_container_width=True)

# Tabla de detalle
st.subheader("🧾 Detalle de Conversaciones")
st.dataframe(df_filtrado, use_container_width=True)
