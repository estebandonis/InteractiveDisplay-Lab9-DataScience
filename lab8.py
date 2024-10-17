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


## ---- Sidebar ---- ##

st.sidebar.title('Years')
years = st.sidebar.slider('Select a range of years', year_min, year_max, (years_unique.min(), years_unique.max()))


## ---- Main page ---- ##

st.title('House Prices from 2006 to 2010')

salePrice_year = salePrice_year[salePrice_year['YrSold'].between(years[0], years[1])]

# st.write(data)

saleprice_min = print("Min",salePrice_year['YrSold'].min())
saleprice_max = print("Max",salePrice_year['YrSold'].max())

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

col4.write("Podemos observar que desde el 2006 al 2010 el precio, a pesar de lo que se podría pensar, ha disminuido en un 0.03%")


# Calculate distributions of houses in categories
st.subheader('Distribución de casas por categoría')
