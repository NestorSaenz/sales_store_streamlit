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
df= pd.read_csv('https://raw.githubusercontent.com/NestorSaenz/sales_dashboard_streamlit/main/df_final.csv')
# antes de github agregar raw. y despues de github agregar usercontent, blob se borra


# Configuración de los filtros, se asigna un espacio a la izquierda para los filtros, y se agrega el logo
st.sidebar.image('D:/bootcamp_experience/visualizacion/logo_sin_fonfo.png')
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