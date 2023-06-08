import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from pmdarima.arima import auto_arima

# Load your DataFrame into a Pandas DataFrame object
df = pd.read_csv(r"E:\GITHUB\Project_2_F\data\Historico_velocidad_internet_provincia.csv")

def main():
    # Add a title to your Streamlit app
    st.title("Line Graph with ARIMA Projections")

    # Select a column (range) from a dropdown menu
    selected_column = st.sidebar.selectbox("Select Column", df.columns[4:])

    # Get unique provinces and trimestres
    unique_provinces = df['Provincia'].unique()
    unique_trimestres = df['Trimestre'].unique()

    # Sidebar selectors for province and trimestre
    selected_province = st.sidebar.selectbox("Select Province", unique_provinces)
    selected_trimestre = st.sidebar.selectbox("Select Trimestre", unique_trimestres)

    # Filter the DataFrame based on selected province and trimestre
    filtered_df = df[(df['Provincia'] == selected_province) & (df['Trimestre'] == selected_trimestre)]

    # Group the filtered DataFrame by year
    grouped_df = filtered_df.groupby('Anio')[selected_column].sum().reset_index()

    # Filter the data for the year 2022 and remove the 4th trimesters
    filtered_df_2022 = grouped_df[grouped_df['Anio'] == 2022].iloc[:3]
    
    # Perform ARIMA model fitting and forecasting
    model = auto_arima(filtered_df_2022[selected_column], seasonal=False)
    forecast, conf_interval = model.predict(n_periods=4, return_conf_int=True)

    # Create the x-values for the observed data
    observed_x = grouped_df['Anio']

    # Create the x-values for the forecasted data
    forecast_x = np.repeat(2022, 4)

    # Plot the line graph with ARIMA projections
    fig, ax = plt.subplots()

    # Plot the observed values
    ax.plot(observed_x, grouped_df[selected_column], label="Observed")

    # Plot the forecasted values
    ax.plot(forecast_x, forecast, linestyle='--', label="Forecast")

    # Customize the plot
    ax.set_xlabel('Year and Trimester')
    ax.set_ylabel('Values')
    ax.set_title(f"{selected_province} - Trimestre {selected_trimestre} - {selected_column}")
    ax.legend()

    # Display the plot using Streamlit
    st.pyplot(fig)

if __name__ == '__main__':
    main()
