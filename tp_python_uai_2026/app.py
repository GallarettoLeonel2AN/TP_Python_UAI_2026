import streamlit as st
import os
import altair as alt
from modelo_ia import ValidadorGastoVeterinario


st.set_page_config(
    page_title="Gestion de costos clinicos veterinarios",
    page_icon="🐾",
    layout="wide",
)

if "consulta_id" not in st.session_state:
    st.session_state.consulta_id = 0
    

if "validador_etr" not in st.session_state:
    st.session_state.validador_etr = None


st.sidebar.header("⚙️ Entorno del Sistema")
modo_sistema = st.sidebar.radio(
    "Seleccionar modo:", 
    ["1. Entrenar", "2. Modo Prueba"]
)
st.sidebar.markdown("---")

# ==========================================
# MODO: Entrenar
# ==========================================
if modo_sistema == "1. Entrenar":
    st.title("Entrenamiento del Modelo Predictivo")
    st.markdown("Analisis historico y entrenamiento del modelo predictivo.")

    st.sidebar.header("Carga de datos")
    archivo_csv = st.sidebar.file_uploader("Subir archivo CSV", type=["csv"])

    
    if archivo_csv is not None:
        ruta_temporal = "datos_veterinarios.csv"
        with open(ruta_temporal, "wb") as archivo:
            archivo.write(archivo_csv.getvalue())

        validador_temporal = ValidadorGastoVeterinario(ruta_temporal)

        try:
            validador_temporal.procesar_datos_pandas()
            validador_temporal.entrenar_modelo()
            
            st.session_state.validador_etr = validador_temporal
        except Exception as error:
            st.error(f"Error al procesar los datos o entrenar el modelo: {error}")

    
    if st.session_state.validador_etr is not None:
        
        st.sidebar.success("Modelo en memoria listo para analizar!")
        

        validador = st.session_state.validador_etr
        
        # --- PESTAÑAS DE DATOS ---
        st.subheader("Vista previa de datos")
        
        alias_columnas = {
            "peso_kg": "Peso mascota (kg)",
            "edad_meses": "Edad (meses)",
            "dias_internacion": "Dias de internacion",
            "es_raza_peligrosa": "Raza peligrosa",
            "costo_total": "Costo total ($)"
        }
        
        datos_split_visuales = validador.datos_grafico_split.copy()
        datos_split_visuales["es_raza_peligrosa"] = datos_split_visuales["es_raza_peligrosa"].map({1: "Si", 0: "No"})
        datos_split_visuales = datos_split_visuales.rename(columns=alias_columnas)
        
        df_entrenamiento = datos_split_visuales[datos_split_visuales["Conjunto"] == "Entrenamiento"]
        df_prueba = datos_split_visuales[datos_split_visuales["Conjunto"] == "Prueba"]
        
        df_entrenamiento = df_entrenamiento.drop(columns=["Conjunto"])
        df_prueba = df_prueba.drop(columns=["Conjunto"])
        
        tab1, tab2 = st.tabs(["📚 Datos de Entrenamiento (70%)", "📝 Datos de Prueba (30%)"])
        
        with tab1:
            st.dataframe(df_entrenamiento.head(10), use_container_width=True, hide_index=True)
        with tab2:
            st.dataframe(df_prueba.head(10), use_container_width=True, hide_index=True)

        # --- METRICAS ---
        st.subheader("Resumen General")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Pacientes procesados", len(datos_split_visuales))
        with col2:
            promedio_costo = datos_split_visuales["Costo total ($)"].mean()
            st.metric("Costo Promedio", f"${promedio_costo:,.0f}")
        with col3:
            porcentaje_precision = validador.precision_modelo * 100
            st.metric("Precision del Modelo", f"{porcentaje_precision:.1f}%")
        with col4:
            st.metric("Margen de Error", f"+/-  ${validador.error_promedio:,.0f}")

        # --- GRAFICO ---
       
        st.subheader("Análisis interactivo de variables (Entrenamiento vs Prueba)")
        opciones_grafico = {
            "Peso de la mascota (kg)": "peso_kg",
            "Edad de la mascota (meses)": "edad_meses",
            "Días de internación": "dias_internacion"
        }
        
        eleccion_usuario = st.selectbox(
            "Seleccioná qué variable querés comparar contra el Costo Total:",
            list(opciones_grafico.keys())
        )
        
        variable_x_tecnica = opciones_grafico[eleccion_usuario]
        datos_originales_split = validador.datos_grafico_split
        datos_visuales_grafico = datos_originales_split[[variable_x_tecnica, "costo_total", "Conjunto"]].rename(
            columns={variable_x_tecnica: eleccion_usuario, "costo_total": "Costo Total ($)"}
        )
        
        
        grafico_puntos = alt.Chart(datos_visuales_grafico).mark_circle(size=60).encode(
            x=alt.X(eleccion_usuario, scale=alt.Scale(zero=False)),
            y=alt.Y("Costo Total ($)", scale=alt.Scale(zero=False)),
            color="Conjunto",
            tooltip=[eleccion_usuario, "Costo Total ($)", "Conjunto"] # Agrega carteles al pasar el mouse
        )

        
        linea_tendencia = alt.Chart(datos_visuales_grafico).mark_line(color='black', size=2).encode(
            x=eleccion_usuario,
            y="Costo Total ($)"
        ).transform_regression(
            eleccion_usuario, "Costo Total ($)"
        )

        
        st.altair_chart((grafico_puntos + linea_tendencia).interactive(), use_container_width=True)

    else:
        st.info("Sube un archivo CSV historico para comenzar a entrenar el modelo.")


# ==========================================
# MODO: Prueba
# ==========================================
elif modo_sistema == "2. Modo Prueba":
    st.title("Pruebas de prediccion")
    
    
    if os.path.exists("modelo_costos.pkl"):
        st.success("🟢 Sistema online. Motor predictivo cargado en memoria.")
        

        validador_prod = ValidadorGastoVeterinario()
        
        st.subheader("Calcular presupuesto para nuevo paciente")
        
        with st.form("formulario_prediccion_prod"):
            peso = st.number_input("Peso en kg", min_value=0.0, step=0.1, key=f"peso_prod_{st.session_state.consulta_id}")
            edad_meses = st.number_input("Edad en meses", min_value=0, step=1, key=f"edad_prod_{st.session_state.consulta_id}")
            dias_internacion = st.number_input("Dias estimados de internacion", min_value=0, step=1, key=f"dias_prod_{st.session_state.consulta_id}")
            opcion_raza = st.selectbox("Es una raza peligrosa?", ["Si", "No"], key=f"raza_prod_{st.session_state.consulta_id}")

            enviado = st.form_submit_button("Calcular Costo Estimado")

        if enviado:
            if peso <= 0 or edad_meses <= 0:
                st.warning("⚠️ Por favor, ingresa valores mayores a 0 para el peso y la edad de la mascota.")
            else:
                valor_raza_numerico = 1 if opcion_raza == "Si" else 0
                try:
                    costo_estimado = validador_prod.hacer_prediccion(
                        {
                            "peso_kg": peso,
                            "edad_meses": edad_meses,
                            "dias_internacion": dias_internacion,
                            "es_raza_peligrosa": valor_raza_numerico,
                        }
                    )
                except Exception as error:
                    st.error(f"No se pudo calcular el costo: {error}")
                else:
                    st.success(f"Costo estimado: ${costo_estimado:,.2f}")

        if st.button("Nueva Consulta"):
            st.session_state.consulta_id += 1
            st.rerun()
            
    else:
        st.error("⚠️ No se encontro el (modelo_costos.pkl). Por favor, volve al Modo Entrenar y subi un CSV.")