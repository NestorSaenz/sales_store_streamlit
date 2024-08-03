import plotly.express as px


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