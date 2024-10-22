import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Relación entre variables y precio de venta')

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
selected_variable = selected_variable.sort_values(ascending=False)

fig_corr = px.bar(x=selected_variable.index, y=selected_variable, title='Correlación de variables con el precio de venta', labels={'x': 'Variable', 'y': 'Correlación'})

st.plotly_chart(fig_corr)

col1, col2 = st.columns(2)

col1.write(selected_variable.head(5))
col2.write('Entre las variables con la mayor coorelación con el precio de venta se encuentran OverallQual, GrLivArea y GarageCars')

# Graph relationship between SalePrice and OverallQual
fig_rel = px.box(numeric, 
            x='OverallQual', 
            y='SalePrice', 
            title='Precio de Venta por Calidad de la Casa', 
            labels={'OverallQual': 'Calidad de la Casa', 'SalePrice': 'Precio de Venta'}
        )

st.plotly_chart(fig_rel)

col3, col4 = st.columns(2)

col3.write('La calidad de la casa es una variable que influye en el precio de venta. A :blue[mayor calidad ↑], :green[mayor precio de venta ↑].')

col4.write('Sin embargo, podemos observar que en este caso, aunque las casas más caras poseen una buena calidad, existen casas que con una alta calidad no se vendieron tan bien. Al igual que existen casas que sin una buena calidad se vendieron a un precio alto.')