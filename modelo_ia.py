import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error


class ValidadorGastoVeterinario:
    """Clase para validar datos y estimar costos veterinarios."""

    def __init__(self, ruta_archivo_csv = None):
        self.ruta_archivo_csv = ruta_archivo_csv
        self.datos_grafico_split = None
        self.precision_modelo = 0.0
        self.error_promedio = 0.0

    def procesar_datos_pandas(self):
        """Lee, limpia y prepara los datos para entrenar el modelo."""
        try:
            datos = pd.read_csv(self.ruta_archivo_csv)
        except FileNotFoundError as error:
            raise FileNotFoundError("No se encontro el archivo CSV.") from error
        except Exception as error:
            raise ValueError("No se pudo leer el archivo CSV.") from error

        datos = datos.dropna().copy()
        datos = datos[datos["costo_total"] > 0]
        datos = datos[datos["dias_internacion"] > 0]
        datos["peso_kg"] = datos["peso_kg"].apply(lambda valor: float(valor))
        datos["edad_meses"] = [int(valor) for valor in datos["edad_meses"]]
        datos["dias_internacion"] = [int(valor) for valor in datos["dias_internacion"]]
        datos["es_raza_peligrosa"] = [int(valor) for valor in datos["es_raza_peligrosa"]]
        datos["costo_total"] = datos["costo_total"].apply(lambda valor: float(valor))

        return datos

    def entrenar_modelo(self):
        """Entrena un modelo de regresion lineal y lo guarda en disco."""
        try:
            datos = self.procesar_datos_pandas()
        except Exception as error:
            raise RuntimeError(f"No se pudieron preparar los datos: {error}") from error

        columnas_caracteristicas = [
            "peso_kg",
            "edad_meses",
            "dias_internacion",
            "es_raza_peligrosa",
        ]
        columna_objetivo = "costo_total"

        variables_entrada = datos[columnas_caracteristicas]
        variable_objetivo = datos[columna_objetivo]

        X_train, X_test, y_train, y_test = train_test_split(
            variables_entrada, 
            variable_objetivo, 
            test_size=0.3, 
            random_state=42 # evita que cambien los datos cada vez que se recarga la pagina
        )

        modelo = LinearRegression()
        modelo.fit(X_train, y_train)

        self.precision_modelo = modelo.score(X_test, y_test)
        
        predicciones_test = modelo.predict(X_test)
        self.error_promedio = mean_absolute_error(y_test, predicciones_test)
        
        
        df_train = X_train.copy()
        df_train["costo_total"] = y_train
        df_train["Conjunto"] = "Entrenamiento"

    
        df_test = X_test.copy()
        df_test["costo_total"] = y_test
        df_test["Conjunto"] = "Prueba"

        self.datos_grafico_split = pd.concat([df_train, df_test])

        ruta_modelo = "modelo_costos.pkl"
        try:
            joblib.dump(modelo, ruta_modelo)
        except Exception as error:
            raise RuntimeError("No se pudo guardar el modelo.") from error

        return modelo

    def hacer_prediccion(self, datos_paciente):
        """Carga el modelo entrenado y devuelve una estimacion de costo."""
        ruta_modelo = "modelo_costos.pkl"

        try:
            modelo_cargado = joblib.load(ruta_modelo)
        except FileNotFoundError as error:
            raise FileNotFoundError("No se encontro el archivo del modelo entrenado.") from error
        except Exception as error:
            raise RuntimeError("No se pudo cargar el modelo.") from error

        datos = pd.DataFrame([datos_paciente])
        datos = datos[[
            "peso_kg",
            "edad_meses",
            "dias_internacion",
            "es_raza_peligrosa",
        ]]

        datos["peso_kg"] = datos["peso_kg"].apply(lambda valor: float(valor))
        datos["edad_meses"] = datos["edad_meses"].apply(lambda valor: int(valor))
        datos["dias_internacion"] = datos["dias_internacion"].apply(lambda valor: int(valor))
        datos["es_raza_peligrosa"] = datos["es_raza_peligrosa"].apply(lambda valor: int(valor))

        prediccion = modelo_cargado.predict(datos)
        return float(prediccion[0])
