# 🐾 Sistema Predictivo de Costos Veterinarios

Esta aplicación web desarrollada en Python utiliza **Machine Learning** para predecir y estimar los costos clínicos de pacientes veterinarios. El sistema analiza variables históricas (peso, edad, días de internación y clasificación de raza) para asistir a la recepción de la clínica en la generación de presupuestos rápidos y basados en datos reales.

Proyecto académico desarrollado para la **Universidad Abierta Interamericana (UAI)**.

## 👥 Desarrollador
* **Leonel Gallaretto**

---

## 🌐 Acceso a la Aplicación (Desplegada)
¡No es necesario instalar nada para probar el sistema! La aplicación se encuentra desplegada en la nube y está lista para su uso inmediato.

👉 **[Haz clic aquí para ir a la aplicación interactiva](REEMPLAZAR_POR_TU_LINK_DE_STREAMLIT_CLOUD)**

*(Nota: En la plataforma online puedes usar directamente el "Modo Prueba" ya que el modelo se encuentra pre-entrenado y cargado en memoria).*

---

## 🚀 Características Principales

El sistema está dividido en dos entornos de ejecución dinámicos:

### 1. Entrenamiento y Análisis
Diseñado para analistas de datos y administradores:
* **Ingesta de Datos:** Carga de historial clínico mediante archivos `.csv`.
* **Limpieza Automatizada:** Uso de `pandas` para sanear datos inconsistentes (eliminación de nulos y valores en cero).
* **Entrenamiento del Modelo:** División estructural del dataset (`train_test_split` al 70/30) para evitar el sobreajuste (*overfitting*).
* **Métricas en Tiempo Real:** Visualización del porcentaje de precisión ($R^2$) y el Error Absoluto Medio (MAE) en moneda local.
* **Gráficos Interactivos:** Renderizado de gráficos de dispersión con `Altair`, incluyendo líneas de tendencia de regresión matemática.

### 2. Modo Prueba
Diseñado para el uso diario en la atención al cliente:
* **Carga en Caliente:** Recuperación instantánea del modelo pre-entrenado (`.pkl`) mediante `joblib`, sin necesidad de reprocesar bases de datos.
* **Interfaz de Presupuesto:** Formulario robusto y validado para ingresar los datos del nuevo paciente y obtener una estimación de costos en milisegundos.
* **Gestión de Sesión:** Manejo de estados a través de `st.session_state` para limpiar y reiniciar consultas dinámicamente.

---

## 🛠️ Tecnologías y Librerías Utilizadas

* **Python 3.x:** Lenguaje base del proyecto.
* **Streamlit:** Framework para el desarrollo de la interfaz de usuario web (Frontend).
* **Pandas:** Manipulación, estructuración y limpieza de DataFrames.
* **Sk-Learn:** Motor matemático para la Regresión Lineal y métricas de evaluación.
* **Altair:** Gráficos estadísticos interactivos.
* **Joblib:** Serialización y persistencia del modelo predictivo en el disco duro.
* **Pytest:** Framework de pruebas unitarias (*Unit Testing*).

---

## 📂 Estructura del Proyecto

```text
📁 tp_python_uai/
│
├── app.py                  # Interfaz gráfica (Frontend) y orquestación con Streamlit
├── modelo_ia.py            # Lógica de negocio, limpieza de Pandas y entrenamiento ML
├── test_modelo.py          # Pruebas unitarias de limpieza y validación matemática
├── requirements.txt        # Dependencias y librerías necesarias para el proyecto
├── modelo_costos.pkl       # (Autogenerado) Cerebro artificial guardado tras entrenar
├── datos_veterinarios.csv  # Dataset de ejemplo para entrenar el modelo
└── README.md               # Documentación del proyecto

💻 Instrucciones para Ejecución Local

1. Clonar el repositorio
Abre una terminal y ejecuta:


git clone https://github.com/GallarettoLeonel2AN/TP_Python_UAI_2026.git

2. Crear y activar un entorno virtual (Recomendado)
Para mantener las librerías aisladas del resto de tu sistema, crea un entorno virtual:

## En Windows:

python -m venv venv
venv\Scripts\activate

## En macOS / Linux:

python3 -m venv venv
source venv/bin/activate

3. Instalar las dependencias
Con el entorno virtual activado, instala todas las librerías necesarias ejecutando:

pip install -r requirements.txt

4. Levantar la aplicación web
Inicia el servidor local de Streamlit con el siguiente comando:

streamlit run app.py