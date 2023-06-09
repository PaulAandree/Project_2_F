import streamlit as st
import pandas as pd
import pandas_profiling
import numpy as np
import plotly.express as px

# Load the data
port = pd.read_csv(r'data/Portabilidad_movil.csv', sep=',')

# Replace ',' with '' in the portability numbers
port = port.replace('\,', '', regex=True)

# Replace null values with 0
port = port.fillna(0)

# Convert columns to integer type
port[['Año','Mes','Personal','Claro','Nextel','Movistar','Otros']] = port[['Año','Mes','Personal','Claro','Nextel','Movistar','Otros']].astype(int)

# Sidebar selection for operators
operators = ['Claro', 'Movistar', 'Personal']
selected_operators = st.sidebar.multiselect("Select Operators", operators, default=operators)

# Define line colors for each operator
line_colors = {'Claro': 'red', 'Movistar': 'green', 'Personal': 'blue'}

# Filter data by selected operators
filtered_data = port[['Año', 'Mes'] + selected_operators]

# Group data by year and month
grouped_data = filtered_data.groupby(['Año', 'Mes']).sum().reset_index()

# Concatenate year and month columns
grouped_data['YearMonth'] = grouped_data['Año'].astype(str) + '-' + grouped_data['Mes'].astype(str)

# Sort data by year and month
grouped_data = grouped_data.sort_values(['Año', 'Mes'])

# Plot the mobile portability by operators using Plotly Express
fig = px.line(grouped_data, x='YearMonth', y=selected_operators,
              color_discrete_map=line_colors,
              labels={'YearMonth': 'Year-Month', 'value': 'Cantidad de Portabilidad'},
              title='Portabilidad Móvil por Operador')

# Display the plot using Streamlit
st.plotly_chart(fig)

# Calculate the correlation matrix
correlation_matrix = grouped_data[selected_operators].corr()

# Display the correlation table using Streamlit
st.write("Correlation Table:")
st.dataframe(correlation_matrix)
