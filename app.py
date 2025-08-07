# app.py
import pandas as pd
import streamlit as st
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Análisis de Vehículos", layout="wide")

# Título de la aplicación
st.header("🚗 Análisis de Anuncios de Venta de Vehículos")

# Leer datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv('vehicles_us.csv')
    # Convertir a datetime
    df['date_posted'] = pd.to_datetime(df['date_posted'])
    # Crear columna de edad del vehículo
    df['age'] = df['date_posted'].dt.year - df['model_year']
    return df

car_data = cargar_datos()

# Mostrar vista previa de los datos (opcional)
st.write("### Vista previa de los datos")
st.dataframe(car_data.head())

# Sección de visualizaciones
st.write("### Explora los datos")

# Casilla de verificación para histograma
if st.checkbox('Mostrar histograma del odómetro'):
    st.write('Creación de un histograma para el odómetro')
    fig = px.histogram(car_data, x="odometer", nbins=50, title="Distribución del odómetro",
                    labels={"odometer": "Kilometraje (millas)"})
    st.plotly_chart(fig, use_container_width=True)

# Casilla de verificación para gráfico de dispersión
if st.checkbox('Mostrar gráfico de dispersión: Precio vs Odómetro'):
    st.write('Relación entre precio y kilometraje')
    fig = px.scatter(car_data, x="odometer", y="price", color="condition",
                    title="Precio vs Kilometraje",
                    labels={"odometer": "Kilometraje", "price": "Precio (USD)"},
                    hover_data=["model", "model_year"])
    st.plotly_chart(fig, use_container_width=True)

# Opcional: Histograma de precios
if st.checkbox('Mostrar distribución de precios'):
    st.write('Distribución de precios de vehículos')
    fig = px.histogram(car_data, x="price", nbins=50, title="Distribución de precios",
                    color_discrete_sequence=['green'])
    fig.update_layout(xaxis=dict(range=[0, 50000]))  # Limitar eje X para mejor visualización
    st.plotly_chart(fig, use_container_width=True)

# Información adicional
st.write("### Información del dataset")
st.write(f"Total de anuncios: {len(car_data)}")
st.write(f"Rango de precios: ${car_data['price'].min():,.0f} - ${car_data['price'].max():,.0f}")
st.write(f"Rango de kilometraje: {car_data['odometer'].min():,.0f} - {car_data['odometer'].max():,.0f} millas")