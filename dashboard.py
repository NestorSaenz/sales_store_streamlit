import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
import streamlit as st
import pandas as pd
import grafico_mapa as graf1 # type: ignore
import grafico_lineas as graf2
import grafico_barras_horizontal as graf3
import grafico_pie as graf4

st.set_page_config(layout='wide') # configurando la paginna para que siempre se vea en modo ancho
st.markdown(
    """
        <h1 style='color:#cfae48; text-align: center; margin-top: -60px; margin-bottom: 80px;'>
        Dashboard de Ventas 🛒
    </h1>
    """, 
    unsafe_allow_html=True
)

#st.title('Dashboard de Ventas :shopping_trolley:') # agregando titulo con un emoji de carrito de compra

# Función páara ajustar los valores de las metricas con su respectivo prefijo
def formato_metrica(valor, prefijo = ''):
    for unidad in ['', 'k']:
        if valor < 1000:
            return f'{prefijo} {valor:.2f} {unidad}'
        else:
            valor /= 1000
    return f'{prefijo} {valor:.2f}'

# Se abre la base de datos 
df= pd.read_csv('https://raw.githubusercontent.com/NestorSaenz/sales_store_streamlit/main/df_final.csv')
                 
# antes de github agregar raw. y despues de github agregar usercontent, blob se borra


# Configuración de los filtros, se asigna un espacio a la izquierda para los filtros, y se agrega el logo
#st.sidebar.image('D:/bootcamp_experience/visualizacion/logo_sin_fonfo.png')
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
anios = st.sidebar.checkbox('Todo el Periodo', value = True)
if anios == False:
    anio =  st.sidebar.slider('Año',df['anio'].min(), df['anio'].max())

# Dando interactividad a los filtros
# Ciudades
if estados_seleccionados:
    df = df[df['ciudad'].isin(estados_seleccionados)]
    
# Productos
if producto_seleccionado != 'Todos':
    df = df[df['tipo_producto'] == producto_seleccionado]
    
# Anios
if anios == False:
    df = df[df['anio']==anio]

# llamada a los graficos
grafico_mapa = graf1.crear_grafico(df)
grafico_lineas = graf2.crear_grafico(df)
grafico_barras_horizontal = graf3.crear_grafico(df)
grafico_pie = graf4.crear_grafico(df)

# Separación de las metricas en dos columnas
col1, col2 = st.columns(2) # se instancia el objeto
with col1:
    st.markdown("<h4 style='color:#cfae48;'>Valor Total de Ingresos</h4>", unsafe_allow_html=True)
    st.metric(" ", formato_metrica(df['valor_total'].sum(), '$')+'M')
    st.plotly_chart(grafico_mapa, use_container_width=True)
    st.plotly_chart(grafico_barras_horizontal, use_container_width=True)
with col2:
    df['ingreso_neto'] = df['ingreso_neto'].astype(int) # Se transforma el tipo de dato a entero
    st.markdown("<h4 style='color:#cfae48;'>Cantidad de Ventas</h4>", unsafe_allow_html=True)
    st.metric('', formato_metrica(df['cantidad'].sum()))
    st.plotly_chart(grafico_lineas, use_container_width=True)
    st.plotly_chart(grafico_pie, use_container_width=True)

#st.metric('**Valor Total de Ingresos Brutos**', formato_metrica(df['valor_total'].sum(), '$'))
    
#st.dataframe(df)

# Color gris rgb(37 40 47)

#Carga del modelo ML

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
st.write("DataFrame completo:")
st.dataframe(df)
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
    
