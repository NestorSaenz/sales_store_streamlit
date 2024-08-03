import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
import streamlit as st
import pandas as pd
import grafico_mapa as graf1  # type: ignore
import grafico_lineas as graf2
import grafico_barras_horizontal as graf3
import grafico_pie as graf4
import grafico_barras_agrupadas as graf5

st.set_page_config(layout='wide')  # Configurando la página para que siempre se vea en modo ancho


# Crear las pestañas
tab1, tab2 = st.tabs(["Dashboard de Ventas", "Predicción de Ingreso Neto"])


with tab1:
    st.markdown(
    """
    <h1 style='color:#cfae48; text-align: center; margin-top: 40px; margin-bottom: 80px;'>
    Dashboard de Ventas 🛒
    </h1>
    """,
    unsafe_allow_html=True
)
    
    # Función para ajustar los valores de las métricas con su respectivo prefijo
    def formato_metrica(valor, prefijo=''):
        for unidad in ['', 'k']:
            if valor < 1000:
                return f'{prefijo} {valor:.2f} {unidad}'
            else:
                valor /= 1000
        return f'{prefijo} {valor:.2f}'
    # Se abre la base de datos 
    df = pd.read_csv('https://raw.githubusercontent.com/NestorSaenz/sales_store_streamlit/main/df_final.csv')
    
    #st.dataframe(df)
    # Configuración de los filtros en la barra lateral
    st.sidebar.image('https://raw.githubusercontent.com/NestorSaenz/sales_store_streamlit/main/logo_sin_fonfo.png')
    st.sidebar.title('Filtros')

    # Filtro de las ciudades
    estados = sorted(list(df['ciudad'].unique()))
    estados_seleccionados = st.sidebar.multiselect('Estados', estados)

    # Filtro de tipo de producto
    producto = sorted(list(df['tipo_producto'].unique()))
    producto.insert(0, 'Todos')
    producto_seleccionado = st.sidebar.selectbox('Productos', producto)

    # Filtro de años
    anios = st.sidebar.checkbox('Todo el Periodo', value=True)
    if anios == False:
        anio = st.sidebar.slider('Año', df['anio'].min(), df['anio'].max())

    # Dando interactividad a los filtros
    if estados_seleccionados:
        df = df[df['ciudad'].isin(estados_seleccionados)]
    
    if producto_seleccionado != 'Todos':
        df = df[df['tipo_producto'] == producto_seleccionado]
    
    if anios == False:
        df = df[df['anio'] == anio]

    # Llamada a los gráficos
    grafico_mapa = graf1.crear_grafico(df)
    grafico_lineas = graf2.crear_grafico(df)
    grafico_barras_horizontal = graf3.crear_grafico(df)
    grafico_pie = graf4.crear_grafico(df)
    grafico_barras_agrupadas = graf5.crear_grafico(df)

    # Separación de las métricas en dos columnas
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h4 style='color:#cfae48;'>Valor Total de Ingresos</h4>", unsafe_allow_html=True)
        st.metric(" ", formato_metrica(df['valor_total'].sum(), '$')+'M')
        st.plotly_chart(grafico_mapa, use_container_width=True)
        st.plotly_chart(grafico_barras_horizontal, use_container_width=True)
    with col2:
        df['ingreso_neto'] = df['ingreso_neto'].astype(int)
        st.markdown("<h4 style='color:#cfae48;'>Cantidad de Ventas</h4>", unsafe_allow_html=True)
        st.metric('', formato_metrica(df['cantidad'].sum()))
        st.plotly_chart(grafico_lineas, use_container_width=True)
        st.plotly_chart(grafico_pie, use_container_width=True)
    
    # Graficando las barras agrupadas    
    st.plotly_chart(grafico_barras_agrupadas)

with tab2:
    #Carga del modelo ML
    st.sidebar.empty()
    # Cargar el modelo y los scalers
    loss_fn = MeanSquaredError()
    model = load_model('model_new.h5', custom_objects={'mse': loss_fn})
    scaler_X = joblib.load('scaler_X.pkl')
    scaler_y = joblib.load('scaler_y.pkl')

    # Cargar y preprocesar datos
    @st.cache_data
    def load_data():
        df = pd.read_csv('https://raw.githubusercontent.com/NestorSaenz/sales_store_streamlit/main/df_final.csv')
        df['fecha_compra'] = pd.to_datetime(df['fecha_compra'])
        df = df[df['anio'] != 2021]
        df = df.loc[:, ['cantidad', 'valor_unitario', 'anio', 'fecha_compra', 'tipo_producto', 'marca', 'estacion', 'ingreso_neto']]
        df = df.groupby(['anio', 'tipo_producto', 'estacion', 'fecha_compra'])['ingreso_neto'].sum().reset_index()
        df['tipo_producto_encoded'] = df['tipo_producto'].astype('category').cat.codes
        df['estacion_encoded'] = df['estacion'].astype('category').cat.codes
        return df
        


    df = load_data()
    # Streamlit app
    # Titulo
    st.markdown(
        """
            <h1 style='color:#cfae48; text-align: center; margin-top: 40px; margin-bottom: 40px;'>
            Predicción de Ingreso Neto 💰
        </h1>
        """, 
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        .stSelectbox div[data-baseweb="select"] {
            font-size: 18px; /* Tamaño de la opción seleccionada */
        }
        .etiqueta-selectbox {  /* Clase para las etiquetas */
            font-size: 20px;  /* Tamaño de la etiqueta */
            color: red;       /* Color de la etiqueta (puedes cambiarlo) */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )



    # Selección de año
    anio = st.selectbox('Selecciona el año', ['2021', '2022'])

    # Selección de tipo de producto
    tipo_producto = st.selectbox('Selecciona el tipo de producto', df['tipo_producto'].unique())

    # Selección de estación
    estacion = st.selectbox('Selecciona la estación', df['estacion'].unique())

    # Convertir selecciones a formato adecuado
    tipo_producto_encoded = df['tipo_producto_encoded'][df['tipo_producto'] == tipo_producto].values[0]
    estacion_encoded = df['estacion_encoded'][df['estacion'] == estacion].values[0]

    # Realizar la predicción
    if st.button('Predecir'):
        nuevos_datos = pd.DataFrame({
            'anio': [anio],
            'tipo_producto_encoded': [tipo_producto_encoded],
            'estacion_encoded': [estacion_encoded]
        })

        nuevos_datos_scaled = scaler_X.transform(nuevos_datos)
        prediccion_scaled = model.predict(nuevos_datos_scaled)
        prediccion = scaler_y.inverse_transform(prediccion_scaled)
        
        st.write(f'<span style="font-size:24px;">Predicción de Ingreso Neto : ${int(prediccion[0][0])/1000} k 💸</span>', unsafe_allow_html=True)
        