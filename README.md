# Análisis de Anuncios de Venta de Coches en EE. UU.

Este proyecto analiza un conjunto de datos de anuncios de vehículos usados para descubrir información clave sobre los factores que influyen en el precio. El objetivo es entender la relación entre características como el año del modelo, el kilometraje, la condición y el precio de venta.

Los resultados se presentan en un **dashboard web interactivo** construido con Streamlit que permite a los usuarios explorar los datos y las visualizaciones de forma dinámica.

## Características del Dashboard

*   **Histograma de Kilometraje:** Visualiza la distribución del odómetro de los vehículos.
*   **Histograma de Precios:** Explora la distribución de los precios de venta.
*   **Gráfico de Dispersión (Precio vs. Kilometraje):** Analiza la correlación entre el precio y el kilometraje, con puntos coloreados según la **condición** del vehículo.

## Instalación

1.  Clona este repositorio en tu máquina local.
2.  Asegúrate de tener Python 3.8+ instalado.
3.  Instala las dependencias necesarias ejecutando el siguiente comando en la raíz del proyecto:

    ```bash
    pip install -r requirements.txt
    ```

## Uso

Para lanzar el dashboard interactivo, ejecuta el siguiente comando desde el directorio raíz del proyecto:

```bash
streamlit run app.py
```

Esto iniciará un servidor local y abrirá la aplicación en tu navegador web.

## Estructura del Proyecto

- **data/**: Contiene los datos brutos (`raw`) y procesados (`processed`).
- **notebooks/**: Jupyter notebooks para limpieza, análisis exploratorio y estadístico.
- **src/**: Código fuente modularizado para procesamiento, análisis y utilidades.
- **tests/**: Pruebas unitarias para garantizar la calidad del código.
- **docs/**: Documentación adicional como el diccionario de datos y la metodología.
- **results/**: Almacena resultados generados, como figuras estáticas.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.