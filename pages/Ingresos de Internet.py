import pandas as pd
import plotly.express as px
import streamlit as st

# Read the data
Int_movil = pd.read_csv(r'data\Ingresos_Internet_Movil_CD.csv')
Int_fijo = pd.read_csv(r'data\Ingresos_Internet_Fijo_CD.csv')

# Create a Streamlit app

st.header('Ingresos de Internet fijo y telefonía Móvil')

# Concatenate the data
df = pd.concat([Int_movil, Int_fijo], axis=0)

# Plot the line graph using plotly.express
fig = px.line(df, x='Año', y=['Ingresos (miles de $)', 'Ingresos (miles de pesos)'],
              color_discrete_sequence=['blue', 'red'],
              labels={'value': 'Ingresos (miles de $)', 'Año': 'año'})

# Display the line graph in Streamlit
st.plotly_chart(fig)
