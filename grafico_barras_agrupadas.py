import streamlit as st
import matplotlib.pyplot as plt
import plotly.tools as tls
import plotly.express as px

#def crear_grafico(df):
    # df= df[df['fecha_compra'].dt.year != 2021]
    # df = df.groupby(['estacion', 'anio'])[ 'ingreso_neto'].sum().reset_index()
    # df.sort_values(by= 'anio', ascending=False, inplace=True)
    #     # Crear el gráfico de barras agrupadas
    # plt.figure(figsize=(14, 6))  # Tamaño de la figura

    # # Ancho de las barras y posiciones
    # bar_width = 0.4
    # r1 = range(len(df['estacion'].unique()))
    # r2 = [x + bar_width for x in r1]

    # # Barras para cada año
    # plt.bar(r1, df[df['anio'] == 2019]['ingreso_neto'], color='skyblue', width=bar_width, edgecolor='white', label='2019')
    # plt.bar(r2, df[df['anio'] == 2020]['ingreso_neto'], color='salmon', width=bar_width, edgecolor='white', label='2020')

    # # Personalizar el gráfico
    # plt.xlabel('Estación', fontsize=16, fontweight='bold', color= 'white')
    # plt.ylabel('Ingreso Neto', fontsize=16, fontweight='bold', color= 'white')
    # plt.title('Comparación de Ingresos Netos por Estación y Año', fontsize=23, fontweight='bold', color= '#cfae48', loc='center')
    # plt.xticks([r + bar_width/2 for r in range(len(df['estacion'].unique()))], df['estacion'].unique(), rotation=45, color= 'white')
    # plt.legend()
    # plt.grid(axis='y', alpha=0.99)
   
    # # Convertir el gráfico de Matplotlib a Plotly
    # plotly_fig = tls.mpl_to_plotly(plt.gcf())  # Obtén la figura actual de Matplotlib y conviértela
    
    # return plotly_fig

def crear_grafico(df):
    df = df[df['fecha_compra'].dt.year != 2021]
    df = df.groupby(['estacion', 'anio'])['ingreso_neto'].sum().reset_index()
    df.sort_values(by='anio', ascending=False, inplace=True)
    df['anio'] = df['anio'].astype(str)  # Convertir la columna 'anio' a tipo string

    colores_personalizados = ['#0077B6', '#4C93B9']
    fig = px.bar(
        df, 
        x='estacion', 
        y='ingreso_neto', 
        text='ingreso_neto',
        color='anio', 
        color_discrete_sequence=colores_personalizados,
        barmode='group' , 
        #title='Comparación de Ingresos Netos por Estación y Año',
        labels={'ingreso_neto': 'Ingreso Neto', 'anio':'Año'},
        category_orders={'estacion': ['Invierno', 'Primavera', 'Verano', 'Otoño']}  # Orden personalizado de las estaciones
    )

    fig.update_layout(
        xaxis_title='Estación', 
        yaxis_title='Ingreso Neto',
        font=dict(color='white'),
        plot_bgcolor='#333333',
        paper_bgcolor='#222222',
        height = 600,
        legend=dict(
        title=None,  # Elimina el título de la leyenda (opcional)
        traceorder="reversed",
        font=dict(
            family="sans-serif",
            size=18,
            color="white"
        ),
        bgcolor="#333333",
        bordercolor="Black",
        borderwidth=2,
        
       
    )
   
)
    fig.update_layout(
                      title={
                        'text': 'Comparación de Ingresos Netos por Estación y Año',
                        'y':1,
                        'x':0.50,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': {
                            'color': '#cfae48',
                            'size': 22
                        }
    },yaxis=dict(
        showgrid=True,             # Mostrar la cuadrícula
        gridwidth=1,               # Grosor de las líneas
        gridcolor='white',         # Color blanco
        zeroline=True,             # Mostrar la línea del cero
        zerolinewidth=2,           # Grosor de la línea del cero
        zerolinecolor='white',     # Color de la línea del cero
        showline=True,             # Mostrar el eje Y
        linewidth=2,               # Grosor del eje Y
        linecolor='white',         # Color del eje Y
        tickfont=dict(color='white') # Color de las etiquetas del eje Y
    ),
    xaxis=dict(
        showgrid=False,             # Ocultar la cuadrícula en el eje X
        showline=True,             # Mostrar el eje X
        linewidth=2,               # Grosor del eje X
        linecolor='white',         # Color del eje X
        tickfont=dict(color='white') # Color de las etiquetas del eje X
    )
                      
)
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside', textfont_color='white')

    return fig