import streamlit as st
import plotly.express as px
import pandas as pd

# Importar la función de procesamiento de datos desde el módulo src
from src.data_processing import load_and_preprocess_data

# --- Configuración de la Página ---
st.set_page_config(page_title="Dashboard de Análisis de Vehículos", layout="wide")

# --- Carga de Datos ---
@st.cache_data
def cached_load_data():
    file_path = "data/raw/vehicles_us.csv"
    return load_and_preprocess_data(file_path)

car_data = cached_load_data()

# --- Barra Lateral de Controles ---
st.sidebar.header("Filtros y Controles")

# Filtro por año del modelo
min_year = int(car_data['model_year'].min())
max_year = int(car_data['model_year'].max())
selected_year_range = st.sidebar.slider(
    "Filtrar por año del modelo:",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)  # Por defecto, selecciona todos los años
)

# Filtro por condición del vehículo
available_conditions = sorted(car_data['condition'].dropna().unique())
selected_conditions = st.sidebar.multiselect(
    "Filtrar por condición:",
    options=available_conditions,
    default=available_conditions
)

st.sidebar.write("---")

# Checkboxes para mostrar/ocultar gráficos
st.sidebar.subheader("Mostrar/Ocultar Gráficos")
show_odo_hist = st.sidebar.checkbox('Histograma de odómetro', value=True)
show_price_hist = st.sidebar.checkbox('Histograma de precios')
show_scatter = st.sidebar.checkbox('Dispersión: Precio vs Odómetro', value=True)

# --- Filtrado de Datos ---
# Aplicar los filtros seleccionados en la barra lateral
filtered_data = car_data[
    (car_data['model_year'] >= selected_year_range[0]) &
    (car_data['model_year'] <= selected_year_range[1]) &
    (car_data['condition'].isin(selected_conditions))
]

# --- Página Principal ---
st.title("🚗 Dashboard de Análisis de Vehículos")
st.markdown(f"Mostrando **{len(filtered_data)}** de **{len(car_data)}** anuncios según los filtros seleccionados.")


# --- Visualizaciones ---
st.divider()

# Organizar los histogramas en columnas
col1, col2 = st.columns(2)

with col1:
    if show_odo_hist:
        st.subheader("Distribución del Odómetro")
        fig_odo = px.histogram(filtered_data, x="odometer", nbins=50,
                               labels={"odometer": "Kilometraje (millas)"})
        st.plotly_chart(fig_odo, use_container_width=True)

with col2:
    if show_price_hist:
        st.subheader("Distribución de Precios")
        fig_price = px.histogram(filtered_data, x="price", nbins=50,
                                 color_discrete_sequence=['green'])
        fig_price.update_layout(xaxis=dict(range=[0, 50000]))
        st.plotly_chart(fig_price, use_container_width=True)

# Gráfico de dispersión
if show_scatter:
    st.subheader("Relación Precio vs. Kilometraje por Condición")
    fig_scatter = px.scatter(filtered_data, x="odometer", y="price", color="condition",
                             labels={"odometer": "Kilometraje", "price": "Precio (USD)"},
                             hover_data=["model", "model_year"])
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- Vista Previa de Datos Filtrados (Opcional) ---
st.divider()
if st.checkbox("Mostrar tabla de datos filtrados"):
    st.write("### Datos Seleccionados")
    st.dataframe(filtered_data)