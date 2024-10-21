import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

st.title('Modelos Predictivos')

data = pd.read_csv('data.csv')

numeric_columns = ['MSSubClass', 'LotArea', 'OverallQual', 'OverallCond', 'YearBuilt',
    'YearRemodAdd', 'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF', 'TotalBsmtSF',
    '1stFlrSF', '2ndFlrSF', 'LowQualFinSF', 'GrLivArea', 'BsmtFullBath',
    'BsmtHalfBath', 'FullBath', 'HalfBath', 'BedroomAbvGr', 'KitchenAbvGr',
    'TotRmsAbvGrd', 'Fireplaces', 'GarageCars', 'GarageArea', 'WoodDeckSF',
    'OpenPorchSF', 'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea',
    'MiscVal', 'MoSold', 'YrSold', 'SalePrice']

numeric = data[numeric_columns]


#Modelos predictivos
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

