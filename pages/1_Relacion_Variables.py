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

# Graph relationship between SalePrice and OverallQual
fig_rel = px.box(numeric, 
            x='OverallQual', 
            y='SalePrice', 
            title='Precio de Venta por Calidad de la Casa', 
            labels={'OverallQual': 'Calidad de la Casa', 'SalePrice': 'Precio de Venta'}
        )

st.plotly_chart(fig_rel)