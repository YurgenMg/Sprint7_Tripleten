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
    
    # Convertir a datetime
    df['date_posted'] = pd.to_datetime(df['date_posted'])
    
    # Crear columna de edad del vehículo
    df['age'] = df['date_posted'].dt.year - df['model_year']
    
    return df
