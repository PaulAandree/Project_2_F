import pandas as pd
import plotly.express as px
import streamlit as st

# Read the data
df2 = pd.read_csv("E:\GITHUB\Project_2_F\data\Internet_Penetracion.csv")

# Reemplazar las comas por puntos en la columna "Accesos por cada 100 hogares"
df2['Accesos por cada 100 hogares'] = df2['Accesos por cada 100 hogares'].str.replace(',', '.')

# Convertir los valores a tipo numérico
df2['Accesos por cada 100 hogares'] = pd.to_numeric(df2['Accesos por cada 100 hogares'])

# Filtrar los datos para el año 2022
df_2022 = df2[df2['Año'] == 2022]

# Calcular la media del acceso por cada 100 hogares por provincia en el año 2022
media_por_provincia = df_2022.groupby('Provincia')['Accesos por cada 100 hogares'].mean().round(2)

fig_bar_media = px.bar(media_por_provincia, x=media_por_provincia.index, y='Accesos por cada 100 hogares',
                       labels={'Accesos por cada 100 hogares': 'Media por cada 100 hogares'},
                       title='Media de accesos por cada 100 hogares por provincia en 2022')

## Grafico de barras con Plotly Express
df_promedio = df2.groupby('Provincia')['Accesos por cada 100 hogares'].mean().reset_index()

# Create the bar chart using Plotly Express
fig_bar = px.bar(df_promedio, x='Provincia', y='Accesos por cada 100 hogares',
                 labels={'Accesos por cada 100 hogares': 'Promedio por cada 100 hogares'},
                 title='Promedio de accesos por cada 100 hogares por provincia en 2022')

# Rotate the x-axis labels for better readability
fig_bar.update_xaxes(tickangle=90)

# Display the bar chart using Streamlit
st.plotly_chart(fig_bar)

## Analisis bivariado

# Create the scatter plot using Plotly Express
fig_scatter = px.scatter(df2, x='Accesos por cada 100 hogares', y='Provincia',
                         title='Gráfico de Dispersión')

# Display the scatter plot using Streamlit
st.plotly_chart(fig_scatter)

## OUTLIERS

Q1 = df2['Accesos por cada 100 hogares'].quantile(0.25)
Q3 = df2['Accesos por cada 100 hogares'].quantile(0.75)
IQR = Q3 - Q1

# Definir los límites para detectar outliers
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df2[(df2['Accesos por cada 100 hogares'] < lower_bound) | (df2['Accesos por cada 100 hogares'] > upper_bound)]

# Display the outliers using Streamlit
st.title("Outliers")
st.write(outliers)
