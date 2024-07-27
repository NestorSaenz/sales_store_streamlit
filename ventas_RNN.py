import pandas as pd
import streamlit as st
import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError


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
st.title('Predicción de Ingreso Neto')

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
    
    st.write(f"Predicción de ingreso neto para los nuevos datos: ${prediccion[0][0]:,.2f}")
