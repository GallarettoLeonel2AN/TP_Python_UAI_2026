import pandas as pd
import os
from modelo_ia import ValidadorGastoVeterinario

def test_limpieza_datos_pandas():
    
    ruta_test = "test_datos_temporales.csv"
    datos_falsos = pd.DataFrame({
        "peso_kg": [10.5, 5.2],
        "edad_meses": [12, 6],
        "dias_internacion": [1, 0],
        "es_raza_peligrosa": [0, 0],
        "costo_total": [16500, 0] 
    })
    datos_falsos.to_csv(ruta_test, index=False)
    

    validador = ValidadorGastoVeterinario(ruta_test)
    datos_limpios = validador.procesar_datos_pandas()
    
    
    assert len(datos_limpios) == 1
    
    
    if os.path.exists(ruta_test):
        os.remove(ruta_test)