import unittest
import pandas as pd
import numpy as np
from src.data_processing import load_and_preprocess_data

class TestDataProcessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Crear datos de prueba"""
        # Crear un DataFrame de prueba
        cls.test_data = pd.DataFrame({
            'model': ['toyota camry', 'honda civic', 'ford f-150'],
            'price': [15000, 12000, np.nan],
            'model_year': [2015, np.nan, 2018],
            'condition': ['good', 'excellent', 'fair'],
            'odometer': [50000, 30000, 80000],
            'date_posted': ['2023-01-01', '2023-02-01', '2023-03-01'],
            'paint_color': ['red', np.nan, 'blue'],
            'is_4wd': [1, np.nan, 0],
            'cylinders': [4, 4, np.nan]
        })
        
        # Guardar datos de prueba en un archivo temporal
        cls.test_file = 'test_data.csv'
        cls.test_data.to_csv(cls.test_file, index=False)
        
        # Procesar los datos
        cls.processed_data = load_and_preprocess_data(cls.test_file)
    
    def test_no_missing_values(self):
        """Verificar que no hay valores faltantes en las columnas importantes"""
        important_columns = ['price', 'model_year', 'condition', 'odometer']
        for column in important_columns:
            with self.subTest(column=column):
                self.assertEqual(self.processed_data[column].isna().sum(), 0)
    
    def test_price_range(self):
        """Verificar que los precios están en el rango esperado"""
        self.assertTrue(all(self.processed_data['price'] > 500))
        self.assertTrue(all(self.processed_data['price'] <= self.processed_data['price'].quantile(0.99)))
    
    def test_age_calculation(self):
        """Verificar el cálculo de la edad del vehículo"""
        current_year = pd.to_datetime('now').year
        self.assertTrue(all(self.processed_data['age'] >= 0))
        self.assertTrue(all(self.processed_data['age'] <= current_year - self.processed_data['model_year']))
    
    def test_manufacturer_extraction(self):
        """Verificar la extracción del fabricante"""
        expected_manufacturers = ['Toyota', 'Honda', 'Ford']
        actual_manufacturers = self.processed_data['manufacturer'].unique()
        self.assertTrue(all(mfr in actual_manufacturers for mfr in expected_manufacturers))
    
    def test_condition_score(self):
        """Verificar la conversión de condición a puntaje"""
        self.assertTrue(all(self.processed_data['condition_score'].between(0, 5)))
        
    def test_data_types(self):
        """Verificar los tipos de datos correctos"""
        self.assertEqual(self.processed_data['model_year'].dtype, 'int16')
        self.assertEqual(self.processed_data['cylinders'].dtype, 'int8')
        self.assertEqual(self.processed_data['is_4wd'].dtype, 'bool')
        self.assertEqual(self.processed_data['age'].dtype, 'int16')
    
    @classmethod
    def tearDownClass(cls):
        """Limpiar archivos temporales"""
        import os
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)

if __name__ == '__main__':
    unittest.main()