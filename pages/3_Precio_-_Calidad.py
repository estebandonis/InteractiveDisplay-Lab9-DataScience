import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Precio - Calidad')

data = pd.read_csv('data.csv')

numeric_columns = ['MSSubClass', 'LotArea', 'OverallQual', 'OverallCond', 'YearBuilt',
    'YearRemodAdd', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF',
    '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea', 'BsmtFullBath',
    'BsmtHalfBath', 'FullBath', 'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr',
    'TotRmsAbvGrd', 'Fireplaces', 'GarageCars', 'GarageArea', 'WoodDeckSF',
    'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea',
    'MiscVal', 'MoSold', 'YrSold', 'SalePrice']

numeric = data[numeric_columns]

# Correlation graph with SalePrice

corr = numeric.corr()

selected_variable = corr['SalePrice']
selected_variable = selected_variable.drop('SalePrice')
selected_variable = selected_variable.sort_values(ascending=False).head(10)

influential_variables = selected_variable.axes[0].tolist()

saleprice_overallqual = data[['SalePrice', 'OverallQual']]

# Define the number of categories
num_categories = 3

# Define the category names
category_names = ['Economica', 'Intermedia', 'Cara']

# Create a new column in the DataFrame for the categories
saleprice_overallqual['Precio_Categoria'] = pd.qcut(saleprice_overallqual['SalePrice'], q=num_categories, labels=category_names)


# Group by OverallQual to get the count of houses
saleprice_overallqual_top = saleprice_overallqual.groupby('OverallQual').size().reset_index(name='Count')

# Sort by Count in descending order
saleprice_overallqual_top = saleprice_overallqual_top.sort_values(by='Count', ascending=False)

fig = px.bar(saleprice_overallqual_top, x='OverallQual', y='Count', title='Cantidad General por Calidad de Casa', labels={'Precio_Categoria': 'Categoria del precio', 'Count': 'Count'})

fig.update_xaxes(type='category')

st.plotly_chart(fig)

st.write('La mayoría de las casas se encuentran en las categorías de la mitad para arriba (5, 6, 7, 8), indicando que poseen una calidad :orange[aceptable] o :green[superior] a lo normal.')


Qual = data[['OverallQual', 'SalePrice']]

saleprice_overallqual_sorted = Qual.groupby('OverallQual').sum().reset_index()

fig2 = px.pie(saleprice_overallqual_sorted, values="SalePrice", names='OverallQual', title='Total Ganancias por Calidad de la Casa')

st.plotly_chart(fig2)

st.write("Podemos ver que en terminos de ganancias monetarias totales, se muestra lo mismo que en cuando lo hacemos en términos de cantidad de casas vendidas. Las casas de calidad 5, 6, 7 y 8 son las que :green[más se venden] y las que :green[más ganancias generan].")
