# Módulo de Procesamiento de Datos

## Descripción General

Este módulo proporciona funcionalidades para cargar y preprocesar datos de vehículos usados. Implementa una pipeline de procesamiento que incluye limpieza de datos, manejo de valores ausentes, tratamiento de valores atípicos y generación de características derivadas.

## Funciones Principales

### `load_and_preprocess_data(file_path: str) -> pd.DataFrame`

Carga los datos desde un archivo CSV y aplica una serie de transformaciones para preparar los datos para el análisis.

#### Parámetros
- `file_path` (str): Ruta al archivo CSV que contiene los datos de vehículos.

#### Retorna
- `pd.DataFrame`: DataFrame de pandas con los datos procesados.

#### Proceso de Preprocesamiento

1. **Conversión de Tipos de Datos**
   - `date_posted` → datetime
   - `model_year` → numeric
   - `cylinders` → numeric

2. **Manejo de Valores Ausentes**
   - `model_year`: Rellenado con la mediana por modelo
   - `cylinders`: Rellenado con la moda por modelo
   - `odometer`: Interpolación lineal basada en la edad del vehículo
   - `paint_color`: Rellenado con 'unknown'
   - `is_4wd`: Rellenado con 0 (asumiendo no 4WD)

3. **Limpieza de Datos**
   - Eliminación de precios irrisorios (<$500)
   - Eliminación de outliers extremos (>99% percentil)
   - Eliminación de vehículos con edad negativa

4. **Feature Engineering**
   - `age`: Edad del vehículo calculada
   - `manufacturer`: Extraída del modelo
   - `age_category`: Categorización de edad
   - `condition_score`: Puntuación numérica de condición

5. **Optimización de Tipos de Datos**
   - Conversión a tipos más eficientes para optimizar memoria

## Reglas de Negocio

1. Los precios menores a $500 se consideran erróneos
2. Se asume que vehículos sin especificación 4WD no son 4WD
3. Las categorías de edad son:
   - Nuevo: 0-3 años
   - Reciente: 4-7 años
   - Usado: 8-15 años
   - Viejo: >15 años
4. Escala de condición:
   - New (5)
   - Like New (4)
   - Excellent (3)
   - Good (2)
   - Fair (1)
   - Salvage (0)

## Dependencias

- pandas
- numpy (implícito a través de pandas)

## Ejemplo de Uso

```python
from src.data_processing import load_and_preprocess_data

# Cargar y procesar datos
df = load_and_preprocess_data("data/raw/vehicles_us.csv")

# Ver información básica
print(df.info())
```