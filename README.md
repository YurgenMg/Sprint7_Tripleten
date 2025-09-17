# 🚗 Dashboard de Análisis de Vehículos USA

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.0%2B-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Licencia: MIT](https://img.shields.io/badge/Licencia-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

Un dashboard interactivo para el análisis profundo del mercado de vehículos usados en Estados Unidos. Esta herramienta profesional permite a los usuarios explorar y analizar factores clave que influyen en los precios de los vehículos, facilitando la toma de decisiones informada en el mercado automotriz.

![Dashboard Preview](https://raw.githubusercontent.com/YurgenMg/Sprint7_Tripleten/main/docs/dashboard_preview.png)

## 🌟 Características Principales

- 📊 **Visualizaciones Interactivas**: Gráficos dinámicos y personalizables
- 🔍 **Filtros Avanzados**: Por año, condición y otros parámetros clave
- 📈 **Análisis en Tiempo Real**: Actualización instantánea de estadísticas
- 💡 **Insights Automáticos**: Descubre patrones y tendencias importantes
- 📱 **Diseño Responsivo**: Experiencia óptima en cualquier dispositivo

## 📊 Visualizaciones Disponibles

### 1. Análisis de Kilometraje
- 📈 Distribución detallada del kilometraje
- 🎯 Identificación de rangos más comunes
- 📉 Detección de valores atípicos

### 2. Análisis de Precios
- 💰 Distribución completa de precios
- 📊 Segmentación por rangos de precio
- 💎 Identificación de oportunidades de mercado

### 3. Relación Precio-Kilometraje
- 🔄 Correlación dinámica entre variables
- 🎨 Segmentación por condición del vehículo
- 🎯 Identificación de tendencias de mercado

## ⚙️ Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. Clone el repositorio:
   ```bash
   git clone https://github.com/YurgenMg/Sprint7_Tripleten.git
   cd Sprint7_Tripleten
   ```

2. Cree y active un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. Instale las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Uso

1. Inicie el dashboard:
   ```bash
   streamlit run app.py
   ```

2. Acceda a través de su navegador:
   - Por defecto: `http://localhost:8501`
   - La URL exacta se mostrará en la terminal

3. Explore las funcionalidades:
   - Use los filtros de la barra lateral
   - Interactúe con los gráficos
   - Exporte datos y visualizaciones

## 📁 Estructura del Proyecto

```
Sprint7_Tripleten/
├── 📊 app.py                # Aplicación principal Streamlit
├── 📝 requirements.txt      # Dependencias del proyecto
├── 📜 LICENSE              # Licencia MIT
├── 📖 README.md            # Documentación principal
├── 🔧 setup.py             # Configuración del paquete
├── 📂 data/                # Datos del proyecto
│   ├── raw/                # Datos sin procesar
│   └── processed/          # Datos procesados
├── 📚 docs/                # Documentación detallada
├── 📓 notebooks/           # Jupyter notebooks
├── 📊 results/             # Resultados y figuras
├── 🛠️ src/                 # Código fuente
└── 🧪 tests/               # Pruebas unitarias
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Cree una rama para su característica (`git checkout -b feature/AmazingFeature`)
3. Commit sus cambios (`git commit -m 'Add: Nueva característica'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abra un Pull Request

## 📜 Licencia

Este proyecto está bajo la Licencia MIT - vea el archivo [`LICENSE`](LICENSE) para más detalles.

## 👥 Autor

- **YurgenMg** - [GitHub](https://github.com/YurgenMg)

## 🙏 Agradecimientos

- [Tripleten](https://tripleten.com) por la formación y los datos proporcionados
- La comunidad de Streamlit por sus excelentes herramientas
- Todos los contribuidores que han ayudado a mejorar este proyecto