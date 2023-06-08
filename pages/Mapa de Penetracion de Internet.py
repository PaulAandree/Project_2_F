import pandas as pd
import geopandas as gpd
import plotly.express as px
import streamlit as st

# Set the title
st.title("Penetración de internet por Provincia")

# Read the data
ruta_archivo = 'E:\GITHUB\Project_2_F\Proyecto telecom\Internet_Penetracion(1).csv'
datos = pd.read_csv(ruta_archivo)

# Filter data for 2022
datos_2022 = datos[datos['Año'] == 2022]
datos_2022['Accesos por cada 100 hogares'] = datos_2022['Accesos por cada 100 hogares'].str.replace(',', '.').astype(float)

# Calculate average access per 100 households by province
promedios = datos_2022.groupby(['Provincia'])['Accesos por cada 100 hogares'].mean().reset_index()
promedios = promedios.round(2)

# Load the shapefile into a GeoDataFrame
ruta_shapefile = 'E:\GITHUB\Project_2_F\Proyecto telecom\provincias\provincias.shp'
mapa_provincias = gpd.read_file(ruta_shapefile)

# Replace values in the "Provincia" column of the DataFrame
valores_a_reemplazar = {
    'Santiago Del Estero': 'Santiago del Estero',
    'Capital Federal': 'Ciudad Autónoma de Buenos Aires',
    'Tierra Del Fuego': 'Tierra del Fuego',
    'Santa Cruz': 'Provincia de Santa Cruz'
}
promedios['Provincia'] = promedios['Provincia'].replace(valores_a_reemplazar)

# Merge the average DataFrame with the geospatial file
mapa_promedios = mapa_provincias.merge(promedios, left_on='NAM', right_on='Provincia')

# Sort the provinces by access percentage in ascending order
mapa_promedios = mapa_promedios.sort_values('Accesos por cada 100 hogares')

# Assign colors to the provinces
num_provinces = len(mapa_promedios)
mapa_promedios['color'] = ['Menor porcentage de penetración ' if i < 5 else 'Provincias con mayor porcentage de internet' for i in range(num_provinces)]

# Create the interactive map using Plotly Express
fig = px.choropleth(mapa_promedios,
                    geojson=mapa_promedios.geometry,
                    locations=mapa_promedios.index,
                    color='color',
                    color_continuous_scale='RdYlBu_r',
                    range_color=[ num_provinces-1,0],
                    hover_name='Provincia',
                    hover_data={'Accesos por cada 100 hogares': ':.2f'}
                    )

# Update map layout
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(height=500, margin={"r": 0, "t": 0, "l": 0, "b": 0})


# Display the map using Streamlit
st.plotly_chart(fig, use_container_width=True)
