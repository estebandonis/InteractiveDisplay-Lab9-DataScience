import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Precio - Año')

data = pd.read_csv('data.csv')
salePrice_year = data[['SalePrice', 'YearBuilt']]

# Group by YearBuilt and sum SalePrice
grouped_data = salePrice_year.groupby('YearBuilt').sum().reset_index()

# Sort the grouped data by SalePrice in descending order and get the top 10 years
top_10_years = grouped_data.sort_values(by='SalePrice', ascending=False).head(10)

# Create bar chart
fig_corr = px.bar(top_10_years, x='SalePrice', y='YearBuilt', orientation='h',
                  title='Top 10 años de Construcción con la Mayor Suma de Dinero Alcanzada',
                  labels={'YearBuilt': 'Año Construido', 'SalePrice': 'Total Recaudado por Ventas'})

fig_corr.update_yaxes(type='category')

col1, col2 = st.columns(2)

col1.write('Los años con :green[mayor cantidad de dinero recaudado] por ventas son 2006, 2005 y 2004. Lo que podrías significar que las casas construidas en años :green[más recientes] tienden a venderse a un precio :green[más alto].')

col2.write("Aunque, esto no significa que las viviendas antiguas no se vendan, ya que, tenemos de hasta :blue[35 años de diferencia] entre el :red[año más atrás] que se tiene registro y el :green[año más reciente] dentro de nuestro top.")

st.plotly_chart(fig_corr)



salePrice_yearSold = data[['SalePrice', 'YearBuilt']]

print(salePrice_yearSold['YearBuilt'].min())
print(salePrice_yearSold['YearBuilt'].max())
print(salePrice_yearSold['YearBuilt'].max()-salePrice_yearSold['YearBuilt'].min())

# Agrupar por YrSold y contar la cantidad de casas vendidas
houses_sold_per_year = salePrice_year.groupby('YearBuilt').size().reset_index(name='HousesSold')

houses_sold_per_year_top_80 = houses_sold_per_year.sort_values(by='HousesSold', ascending=False).head(5)

houses_sold_per_year = houses_sold_per_year.sort_values(by='HousesSold', ascending=False).head(10)

print(houses_sold_per_year['YearBuilt'].min())
print(houses_sold_per_year['YearBuilt'].max())
print(houses_sold_per_year['YearBuilt'].max()-houses_sold_per_year['YearBuilt'].min())

print(houses_sold_per_year)

# Crear gráfica de barras
fig_houses_sold = px.pie(houses_sold_per_year, values='HousesSold', names='YearBuilt')

# Update x-axis to show only the specific years in top 10
fig_houses_sold.update_xaxes(type='category')

# Mostrar gráfica en Streamlit
st.plotly_chart(fig_houses_sold)

col1, col2 = st.columns(2)

sum_houses_sold_per_year_top_80 = houses_sold_per_year_top_80['HousesSold'].sum()
print(sum_houses_sold_per_year_top_80)

sum_houses_sold_per_year = houses_sold_per_year['HousesSold'].sum()
print(sum_houses_sold_per_year)

col1.metric('Casas Construidas en los últimos 10 años del top 10', f"{((sum_houses_sold_per_year_top_80/sum_houses_sold_per_year)*100).round(1)}%")
