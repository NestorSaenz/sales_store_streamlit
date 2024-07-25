import pandas as pd
import plotly.express as px

def crear_grafico(df):
    df = df.groupby('nombre_vendedor')['cantidad'].sum().reset_index()
    df = df[df['nombre_vendedor']!= 'Unknown']
    
    #crear grafico
    color=['#0077b6', '#1A4D83', '#063970', '#2f567D', '#4B6A92']
    fig = px.pie(df,
                 values='cantidad',
                 names= 'nombre_vendedor',
                 color_discrete_sequence=color
                 )
    
    fig.update_layout(yaxis_title = 'Vendedor', xaxis_title = 'Cantidad de ventas', showlegend = False)
    fig.update_traces(textposition = 'inside', textinfo = 'percent+label', insidetextfont=dict(size=13))
    
    fig.update_layout(
    title={
        'text': 'Cantidad de ventas por vendedor',
        'y':0.95,
        'x':0.31,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'color': '#cfae48',
            'size': 22
        }
    }
    )
     
    return fig