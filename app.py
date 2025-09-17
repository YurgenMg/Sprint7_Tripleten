import streamlit as st
import plotly.express as px

# Importar la función de procesamiento de datos desde el módulo src
from src.data_processing import load_and_preprocess_data

# --- Configuración de la Página ---
st.set_page_config(
    page_title="US Vehicle Analysis Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estilos CSS Personalizados ---
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
    }
    .stProgress .st-bo {
        background-color: #4CAF50;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Carga de Datos ---
@st.cache_data(show_spinner=True)
def cached_load_data():
    with st.spinner('Cargando datos... Por favor espere.'):
        file_path = "data/raw/vehicles_us.csv"
        return load_and_preprocess_data(file_path)

car_data = cached_load_data()

# --- Barra Lateral de Controles ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/car-sale.png", width=100)
    st.title("🎯 Panel de Control")
    st.markdown("---")
    
    # Agregar selector de modo de análisis
    analysis_mode = st.radio(
        "📊 Modo de Análisis",
        ["General", "Por Fabricante", "Tendencias Temporales"]
    )

# Filtro por año del modelo
min_year = int(car_data['model_year'].min())
max_year = int(car_data['model_year'].max())

# Agregar opción para seleccionar un año específico o un rango
year_filter_type = st.sidebar.radio(
    "Tipo de filtro de año:",
    ["Año específico", "Rango de años"]
)

if year_filter_type == "Año específico":
    selected_year = st.sidebar.selectbox(
        "Seleccionar año:",
        range(min_year, max_year + 1),
        index=list(range(min_year, max_year + 1)).index(2001) if 2001 in range(min_year, max_year + 1) else 0
    )
    # Configurar el rango para un solo año
    selected_year_range = (selected_year, selected_year)
else:
    selected_year_range = st.sidebar.slider(
        "Filtrar por rango de años:",
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
st.title("🚗 Análisis del Mercado de Vehículos USA")
st.markdown("""
    <div style='background-color: #e8f4ea; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
        <h4 style='color: #2e7d32; margin: 0;'>📊 Estado del Análisis</h4>
        <p style='margin: 0.5rem 0;'>
            Mostrando <strong style='color: #2e7d32;'>{}</strong> de <strong style='color: #2e7d32;'>{}</strong> anuncios 
            según los filtros seleccionados
        </p>
    </div>
""".format(len(filtered_data), len(car_data)), unsafe_allow_html=True)

# --- Métricas Clave ---
col_metrics = st.columns(4)
with col_metrics[0]:
    st.markdown("""
        <div class='metric-card'>
            <h3 style='margin: 0; color: #1976D2;'>💰 Precio Promedio</h3>
            <h2 style='margin: 0.5rem 0;'>${:,.0f}</h2>
        </div>
    """.format(filtered_data['price'].mean()), unsafe_allow_html=True)

with col_metrics[1]:
    st.markdown("""
        <div class='metric-card'>
            <h3 style='margin: 0; color: #388E3C;'>📏 Kilometraje Medio</h3>
            <h2 style='margin: 0.5rem 0;'>{:,.0f} mi</h2>
        </div>
    """.format(filtered_data['odometer'].mean()), unsafe_allow_html=True)

with col_metrics[2]:
    st.markdown("""
        <div class='metric-card'>
            <h3 style='margin: 0; color: #E64A19;'>📅 Año Promedio</h3>
            <h2 style='margin: 0.5rem 0;'>{:.1f}</h2>
        </div>
    """.format(filtered_data['model_year'].mean()), unsafe_allow_html=True)

with col_metrics[3]:
    most_common_condition = filtered_data['condition'].mode()[0]
    st.markdown("""
        <div class='metric-card'>
            <h3 style='margin: 0; color: #7B1FA2;'>🚘 Condición Común</h3>
            <h2 style='margin: 0.5rem 0;'>{}</h2>
        </div>
    """.format(most_common_condition.title()), unsafe_allow_html=True)

st.markdown("---")

# --- Visualizaciones ---
tab1, tab2 = st.tabs(["📊 Distribuciones", "🔄 Correlaciones"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        if show_odo_hist:
            st.markdown("""
                <div style='background-color: white; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <h3 style='color: #1976D2; margin-bottom: 1rem;'>📏 Distribución del Kilometraje</h3>
            """, unsafe_allow_html=True)
            fig_odo = px.histogram(filtered_data, x="odometer", nbins=50,
                                labels={"odometer": "Kilometraje (millas)"},
                                color_discrete_sequence=['#1976D2'])
            fig_odo.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(t=20, l=20, r=20, b=20)
            )
            st.plotly_chart(fig_odo, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        if show_price_hist:
            st.markdown("""
                <div style='background-color: white; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                    <h3 style='color: #388E3C; margin-bottom: 1rem;'>💰 Distribución de Precios</h3>
            """, unsafe_allow_html=True)
            fig_price = px.histogram(filtered_data, x="price", nbins=50,
                                color_discrete_sequence=['#388E3C'])
            fig_price.update_layout(
                xaxis=dict(range=[0, 50000]),
                plot_bgcolor='white',
                paper_bgcolor='white',
                margin=dict(t=20, l=20, r=20, b=20)
            )
            st.plotly_chart(fig_price, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    if show_scatter:
        st.markdown("""
            <div style='background-color: white; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
                <h3 style='color: #7B1FA2; margin-bottom: 1rem;'>🔄 Relación Precio vs. Kilometraje</h3>
        """, unsafe_allow_html=True)
        fig_scatter = px.scatter(filtered_data, 
                             x="odometer", 
                             y="price", 
                             color="condition",
                             labels={"odometer": "Kilometraje (millas)", 
                                    "price": "Precio (USD)",
                                    "condition": "Condición"},
                             hover_data=["model", "model_year"])
        fig_scatter.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=20, l=20, r=20, b=20),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor='rgba(255, 255, 255, 0.8)'
            )
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# --- Análisis Específico por Modo ---
if analysis_mode == "Por Fabricante":
    st.markdown("### 🏢 Análisis por Fabricante")
    
    # Métricas por fabricante
    manufacturer_stats = filtered_data.groupby('manufacturer').agg({
        'price': ['mean', 'count'],
        'condition_score': 'mean'
    }).round(2)
    
    # Ordenar por cantidad de vehículos
    manufacturer_stats = manufacturer_stats.sort_values(('price', 'count'), ascending=False)
    
    # Mostrar top fabricantes
    st.markdown("""
        <div style='background-color: white; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h3 style='color: #1976D2; margin-bottom: 1rem;'>📊 Top Fabricantes</h3>
    """, unsafe_allow_html=True)
    
    # Gráfico de barras de cantidad por fabricante
    fig_manufacturers = px.bar(
        manufacturer_stats.head(10).reset_index(),
        x='manufacturer',
        y=('price', 'count'),
        title="Top 10 Fabricantes por Cantidad de Vehículos",
        labels={'manufacturer': 'Fabricante', 'value': 'Cantidad de Vehículos'},
        color=('price', 'mean'),
        color_continuous_scale='Viridis'
    )
    fig_manufacturers.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=50, l=20, r=20, b=20)
    )
    st.plotly_chart(fig_manufacturers, use_container_width=True)
    
    # Tabla de estadísticas por fabricante
    st.markdown("#### 📈 Estadísticas Detalladas")
    st.dataframe(manufacturer_stats.head(10))
    st.markdown("</div>", unsafe_allow_html=True)

elif analysis_mode == "Tendencias Temporales":
    st.markdown("### 📅 Análisis Temporal")
    
    # Preparar datos temporales
    temporal_data = filtered_data.copy()
    temporal_data['year_month'] = temporal_data['date_posted'].dt.to_period('M')
    temporal_stats = temporal_data.groupby('year_month').agg({
        'price': ['mean', 'count'],
        'condition_score': 'mean'
    }).reset_index()
    temporal_stats['year_month'] = temporal_stats['year_month'].astype(str)
    
    # Renombrar columnas para facilitar el uso
    temporal_stats.columns = ['year_month', 'price_mean', 'price_count', 'condition_score']
    
    # Gráfico de línea temporal
    st.markdown("""
        <div style='background-color: white; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h3 style='color: #1976D2; margin-bottom: 1rem;'>📈 Evolución Temporal</h3>
    """, unsafe_allow_html=True)
    
    fig_temporal = px.line(
        temporal_stats,
        x='year_month',
        y='price_mean',
        title="Evolución del Precio Medio",
        labels={
            'year_month': 'Fecha',
            'price_mean': 'Precio Medio ($)'
        }
    )
    fig_temporal.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=50, l=20, r=20, b=20)
    )
    st.plotly_chart(fig_temporal, use_container_width=True)
    
    # Gráfico de volumen de ventas
    fig_volume = px.bar(
        temporal_stats,
        x='year_month',
        y='price_count',
        title="Volumen de Anuncios por Mes",
        labels={
            'year_month': 'Fecha',
            'price_count': 'Cantidad de Anuncios'
        }
    )
    fig_volume.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=50, l=20, r=20, b=20)
    )
    st.plotly_chart(fig_volume, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Vista Previa de Datos Filtrados ---
st.markdown("---")
with st.expander("📋 Ver Datos Detallados"):
    st.markdown("""
        <div style='background-color: white; padding: 1rem; border-radius: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <h3 style='color: #1976D2; margin-bottom: 1rem;'>🔍 Datos Seleccionados</h3>
    """, unsafe_allow_html=True)
    
    # Agregar filtros de búsqueda
    search_col1, search_col2 = st.columns(2)
    with search_col1:
        search_manufacturer = st.text_input("🔍 Buscar por fabricante")
    with search_col2:
        price_range = st.slider(
            "💰 Rango de precios",
            min_value=int(filtered_data['price'].min()),
            max_value=int(filtered_data['price'].max()),
            value=(int(filtered_data['price'].min()), int(filtered_data['price'].max()))
        )
    
    # Aplicar filtros de búsqueda
    display_data = filtered_data.copy()
    if search_manufacturer:
        display_data = display_data[display_data['manufacturer'].str.contains(search_manufacturer, case=False)]
    display_data = display_data[
        (display_data['price'] >= price_range[0]) &
        (display_data['price'] <= price_range[1])
    ]
    
    # Agregar botones de descarga
    col_download1, col_download2 = st.columns(2)
    with col_download1:
        csv = display_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar CSV",
            data=csv,
            file_name="vehicles_filtered.csv",
            mime="text/csv"
        )
    with col_download2:
        # Crear un buffer de bytes para el archivo Excel
        from io import BytesIO
        excel_buffer = BytesIO()
        display_data.to_excel(excel_buffer, index=False)
        excel_buffer.seek(0)
        
        st.download_button(
            label="📥 Descargar Excel",
            data=excel_buffer,
            file_name="vehicles_filtered.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # Mostrar datos con formato mejorado
    st.dataframe(
        display_data.style.background_gradient(subset=['price'], cmap='Greens'),
        height=300
    )
    
    # Agregar resumen estadístico
    with st.expander("📊 Resumen Estadístico"):
        st.dataframe(display_data.describe())
    
    st.markdown("</div>", unsafe_allow_html=True)