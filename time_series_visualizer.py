import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col = 'date')

# Clean data
# Crear lista a partir de los valores
lista = list(df.value)
# Ordenar la lista de menor a mayor
lista.sort()
# Obtener las posiciones
n = len(lista)
pos_2_5 = round((n * 2.5)/100)
pos_97_5 = round((n * 97.5)/100)

# Definir los límites del percentil 2.5 y 97.5
limite_inferior = lista[pos_2_5] 
limite_superior = lista[pos_97_5]

# Modificamos la dataframe teniendo en cuenta los limites
df_modificado = df[(df > limite_inferior) & (df < limite_superior)]

# Eliminamos aquellas filas vacias (NaN)
df_modificado = df_modificado.dropna()

# Convertir el índice a DatetimeIndex 
df_modificado.index = pd.to_datetime(df_modificado.index)
df = df_modificado


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(df.index, df['value'], color='red')
    
    # Set labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df['value'].resample('ME').mean()

    # Draw bar plot
    df_bart.index = pd.to_datetime(df_bar.index)
    df_bar = df_bar.groupby([df_bar.index.year, df_bar.index.month]).mean().unstack()

    # Mapeo para aplicar meses
    meses_del_año = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 
        5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 
        10: 'October', 11: 'November', 12: 'December'
    }

    # Ingresamos a columnas [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] y aplicamos el diccionario mediante map
    # para aplicar meses_del_año a cada valor
    df_bar.columns = df_bar.columns.map(meses_del_año)

    fig, ax = df_bar.plot(kind='bar', figsize=(10, 6))

    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    # Crear la figura y los ejes
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
    # Diagrama de caja por año (Tendencia)
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Average Page Views')
      
    # Diagrama de caja por mes (Estacionalidad)
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Average Page Views')
        
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
