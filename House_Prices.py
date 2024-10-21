import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

## ---- Data ---- ##

data = pd.read_csv('data.csv')
salePrice_year = data[['SalePrice', 'YrSold']]
year_max = salePrice_year['YrSold'].unique().max()
year_min = salePrice_year['YrSold'].unique().min()
years_unique = salePrice_year['YrSold'].unique()

# Define the number of categories
num_categories = 3

# Define the category names
category_names = ['Economica', 'Intermedia', 'Cara']

# Create a new column in the DataFrame for the categories
salePrice_year['Precio_Categoria'] = pd.qcut(salePrice_year['SalePrice'], q=num_categories, labels=category_names)


## ---- Sidebar ---- ##

st.sidebar.title('Years')
years = st.sidebar.slider('Select a range of years', year_min, year_max, (years_unique.min(), years_unique.max()))

categories_selected = st.sidebar.multiselect('Select a category', options=salePrice_year['Precio_Categoria'].unique(), default=salePrice_year['Precio_Categoria'].unique())


## ---- Main page ---- ##

st.title('House Prices from 2006 to 2010')

salePrice_year = salePrice_year[salePrice_year['YrSold'].between(years[0], years[1])]

salePrice_year = salePrice_year.query("Precio_Categoria in @categories_selected")

# st.write(data)

yearsold_min = salePrice_year['YrSold'].min()
yearsold_max = salePrice_year['YrSold'].max()

col1, col2 = st.columns(2)

# Calculate and format mean sale price
mean_sale_price = salePrice_year['SalePrice'].mean().round(2)
formatted_mean_sale_price = f"$.{mean_sale_price:,}"
col1.write(f'#### Media: :green[{formatted_mean_sale_price}]')

diff_max_mean = salePrice_year['SalePrice'].max() - mean_sale_price
formatted_diff_max_mean = f"$.{diff_max_mean:,}"
col2.write(f'#### Diferencia del Precio Máximo con Media: :red[{formatted_diff_max_mean}]')

scatter_prices = px.histogram(salePrice_year, x='SalePrice', y='YrSold', labels={'SalePrice': 'Precio de Venta', 'YrSold': 'Año de Venta'}, title='Precio de Venta por Año')

st.plotly_chart(scatter_prices)

col3, col4 = st.columns(2)

min_year_prices = salePrice_year[salePrice_year['YrSold'] == yearsold_min]['SalePrice'].mean()
max_year_prices = salePrice_year[salePrice_year['YrSold'] == yearsold_max]['SalePrice'].mean()

max_min_diff = (min_year_prices - max_year_prices).round(3)
formatted_max_min_diff = f"$.{max_min_diff:,}"

percentage_diff = (1 - (min_year_prices/max_year_prices)).round(3)

col3.metric('Price Decline', f"{formatted_max_min_diff}", f"{percentage_diff}%", delta_color='inverse')

col4.write(f"Podemos observar que desde el 2006 al 2010 el precio, a pesar de lo que se podría pensar, ha disminuido en un {percentage_diff}%")


# Calculate distributions of houses in categories

# Obtener la casa más cara y más barata en SalePrice por cada etiqueta en Precio_Categoria
max_prices = salePrice_year.groupby('Precio_Categoria')['SalePrice'].max()
min_prices = salePrice_year.groupby('Precio_Categoria')['SalePrice'].min()

# Calculate the value counts for each category
category_counts = salePrice_year['Precio_Categoria'].value_counts()

# Define the colors for the pie chart
colors = ['#2E4462','#BECDC8','#32A13A']

# Create the pie chart
fig = px.pie(values=category_counts, names=category_counts.index, title='Distribución de casas por categoría', color=category_counts.index, color_discrete_map={category_names[i]: colors[i] for i in range(num_categories)})
st.plotly_chart(fig)