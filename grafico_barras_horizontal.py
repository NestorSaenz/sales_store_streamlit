import pandas as pd
import plotly.express as px

def crear_grafico(df):
    df = df.groupby('producto')['ingreso_neto'].sum().sort_values(ascending = True).reset_index()
    
    # Se crea la grafica
    fig = px.bar(df.tail(10),
                 x = 'ingreso_neto',
                 y = 'producto',
                 text = 'ingreso_neto',
                 color_discrete_sequence=['#0077B6']
              )
    
    fig.update_layout(yaxis_title = 'Productos', 
                      xaxis_title = 'Ingresos ($)', 
                      showlegend = False,
                      title={
                        'text': 'Top de productos que generan mas ingresos ($)',
                        'y':0.95,
                        'x':0.43,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'font': {
                            'color': '#cfae48',
                            'size': 22
                        }
    })
    
    fig.update_traces(texttemplate = '%{text:.3s}',
                      textfont=dict(color="white"),
                      #textposition='outside', 
                      )

    return fig