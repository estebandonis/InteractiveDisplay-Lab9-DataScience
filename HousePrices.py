from calendar import c
from tabnanny import check
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

numeric_columns = ['MSSubClass', 'LotArea', 'OverallQual', 'OverallCond', 'YearBuilt',
    'YearRemodAdd', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF',
    '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea', 'BsmtFullBath',
    'BsmtHalfBath', 'FullBath', 'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr',
    'TotRmsAbvGrd', 'Fireplaces', 'GarageCars', 'GarageArea', 'WoodDeckSF',
    'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea',
    'MiscVal', 'MoSold', 'YrSold', 'SalePrice']

numeric = data[numeric_columns]

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

col4.write("Podemos observar que desde el 2006 al 2010 el precio, a pesar de lo que se podría pensar, ha disminuido en un 0.03%")


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

#Modelos predictivos
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

X = numeric.drop("SalePrice", axis=1)
y = numeric["SalePrice"]

# Dividir los datos en conjunto de entrenamiento y prueba (80% entrenamiento, 20% prueba)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Añadir una constante para el término de intercepción
X_train_const = sm.add_constant(X_train)

# Modelo de regresión lineal
model1 = sm.OLS(y_train, X_train_const).fit()

y_pred1 = model1.predict(sm.add_constant(X_test))

fig_pred1 = px.scatter(x=y_test, y=y_pred1, title='Regresion Lineal', labels={'x': 'Precio Real', 'y': 'Precio Predicho'})

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
model2 = RandomForestRegressor(n_estimators=100, random_state=42)

# Use cross-validation
scores = cross_val_score(model2, X_train, y_train, cv=5, scoring='neg_mean_squared_error')

model2.fit(X_train, y_train)
y_pred2 = model2.predict(X_test)

fig_pred2 = px.scatter(x=y_test, y=y_pred2, title='Random Forest', labels={'x': 'Precio Real', 'y': 'Precio Predicho'})

from sklearn.neural_network import MLPRegressor
model3 = MLPRegressor(hidden_layer_sizes=(100, 200), max_iter=500, random_state=42)

model3.fit(X_train, y_train)
y_pred3 = model3.predict(X_test)

fig_pred3 = px.scatter(x=y_test, y=y_pred3, title='Red Neuronal', labels={'x': 'Precio Real', 'y': 'Precio Predicho'})

# Show the results
st.write('## Predicciones de Precio de Venta')
col5, col6, col7 = st.columns(3)

check_rl = col5.checkbox('Regresión Lineal', value=True)
check_rf = col6.checkbox('Random Forest')
check_rn = col7.checkbox('Red Neuronal')

column_num = check_rl + check_rf + check_rn
results = []
if check_rl:
    results.append({"fig": fig_pred1, "MSE": np.mean((y_test - y_pred1)**2), "R2": r2_score(y_test, y_pred1)})
if check_rf:
    results.append({"fig": fig_pred2, "MSE": np.mean((y_test - y_pred2)**2), "R2": r2_score(y_test, y_pred2)})
if check_rn:
    results.append({"fig": fig_pred3, "MSE": np.mean((y_test - y_pred3)**2), "R2": r2_score(y_test, y_pred3)})

cols = st.columns(column_num)
for i, x in enumerate(cols):
    if results[i] is not None:
        cols[i].plotly_chart(results[i]["fig"])
        cols[i].write(f'Error cuadrático medio: {results[i]["MSE"]}')
        cols[i].write(f'R2: {results[i]["R2"]}')

