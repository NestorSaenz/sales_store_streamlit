import pandas as pd
import plotly.express as px

def crear_grafico(df):
    # conversion de la fecha a datetime
    df['fecha_compra'] = pd.to_datetime(df['fecha_compra'])
    # debido a que los datos del 2021 parecen estar viciados para esta consulta se filtran y no se toman en cuenta
    #df = df[df['fecha_compra'].dt.year != 2021]
    df = df.groupby(['anio', 'mes', 'num_mes'])['ingreso_neto'].sum().reset_index().sort_values(by=['anio', 'num_mes'])
    #df = df.set_index('fecha_compra').groupby(pd.Grouper(freq='ME'))['ingreso_neto'].sum().reset_index()
   
    # grafica
    fig = px.line(df,
                  x = 'mes',
                  y = 'ingreso_neto',
                  range_y = (0, df.max()),
                  color = 'anio',
                  line_dash = 'anio',
                  labels={'anio': 'Año'},
                  markers=True
                  )
    fig.update_layout(yaxis_title = 'Ingresos ($)')
    fig.update_layout(xaxis_title = 'Mes')
    
    fig.update_layout(
    title={
        'text': 'Ingresos mensuales',
        'y':0.95,
        'x':0.19,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'color': '#cfae48',
            'size': 22
        }
    }
    )

    
    return fig