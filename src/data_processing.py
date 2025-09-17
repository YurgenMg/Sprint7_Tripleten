import pandas as pd

def load_and_preprocess_data(file_path: str) -> pd.DataFrame:
    """
    Carga los datos desde un archivo CSV, los preprocesa y devuelve un DataFrame.

    Args:
        file_path: La ruta al archivo CSV.

    Returns:
        Un DataFrame de pandas con los datos procesados.
    """
    # Leer datos
    df = pd.read_csv(file_path)
    
    # --- Limpieza y Preprocesamiento ---

    # Convertir 'date_posted' a datetime
    df['date_posted'] = pd.to_datetime(df['date_posted'])
    
    # Asegurar que 'model_year' y 'cylinders' sean numéricos, convirtiendo errores a NaN
    df['model_year'] = pd.to_numeric(df['model_year'], errors='coerce')
    df['cylinders'] = pd.to_numeric(df['cylinders'], errors='coerce')

    # --- Manejo de Valores Ausentes ---

    # Rellenar 'model_year' con la mediana por grupo de 'model'
    df['model_year'] = df.groupby('model')['model_year'].transform(
        lambda x: x.fillna(x.median())
    )

    # Rellenar 'cylinders' con la moda por grupo de 'model'
    # Si la moda está vacía, se usa la mediana del grupo
    df['cylinders'] = df.groupby('model')['cylinders'].transform(
        lambda x: x.fillna(x.mode()[0] if not x.mode().empty else x.median())
    )

    # Rellenar 'odometer' usando interpolación lineal por edad
    # Primero, calculamos una edad temporal para ordenar
    df['age_temp'] = df['date_posted'].dt.year - df['model_year']
    df = df.sort_values('age_temp')
    df['odometer'] = df['odometer'].interpolate(method='linear', limit_direction='forward')
    # Rellenar los restantes (si los hay) con la mediana global
    df['odometer'] = df['odometer'].fillna(df['odometer'].median())

    # Rellenar 'paint_color' con 'unknown'
    df['paint_color'] = df['paint_color'].fillna('unknown')

    # Rellenar 'is_4wd' con 0 (asumiendo que si no se especifica, no es 4WD)
    df['is_4wd'] = df['is_4wd'].fillna(0)

    # Eliminar filas donde 'price' o 'model_year' son nulos después del relleno
    df.dropna(subset=['price', 'model_year'], inplace=True)

    # --- Tratamiento de Valores Atípicos ---

    # Eliminar anuncios con precios irrisorios
    df = df[df['price'] > 500]

    # Eliminar precios extremadamente altos (cuantil 0.99)
    q99 = df['price'].quantile(0.99)
    df = df[df['price'] <= q99]

    # --- Creación de Nuevas Características (Feature Engineering) ---

    # Crear columna de edad del vehículo
    df['age'] = df['date_posted'].dt.year - df['model_year']
    # Eliminar vehículos con edad negativa (error en los datos)
    df = df[df['age'] >= 0]

    # Extraer marca del modelo
    df['manufacturer'] = df['model'].str.split().str[0].str.title()

    # Clasificar por categoría de edad según reglas de negocio
    df['age_category'] = pd.cut(
        df['age'],
        bins=[0, 3, 7, 15, 100],
        labels=['Nuevo (0-3)', 'Reciente (4-7)', 'Usado (8-15)', 'Viejo (>15)'],
        right=False
    )

    # Convertir condición a escala numérica para análisis cuantitativos
    condition_map = {
        'new': 5,      # Mejor condición posible
        'like new': 4, # Casi nuevo
        'excellent': 3, # Excelente estado
        'good': 2,     # Buen estado
        'fair': 1,     # Estado aceptable
        'salvage': 0   # Necesita reparación
    }
    df['condition_score'] = df['condition'].map(condition_map)

    # Optimización de tipos de datos para reducir uso de memoria
    df['model_year'] = df['model_year'].astype('int16')  # Años no requieren int64
    df['cylinders'] = df['cylinders'].astype('int8')     # Cilindros típicamente 1-12
    df['is_4wd'] = df['is_4wd'].astype('bool')          # Boolean para banderas
    df['age'] = df['age'].astype('int16')               # Edad no requiere int64
    
    # Eliminar columnas temporales y no necesarias
    if 'age_temp' in df.columns:
        df = df.drop('age_temp', axis=1)

    return df