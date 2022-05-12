import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
archivo = pd.read_csv('API_SP.POP.TOTL_DS2_es_csv_v2_4004971.csv', header=2, keep_default_na=False)

paisabuscar="México"
anio = 2025

index = archivo.index
pais = archivo["Country Name"] == paisabuscar
indice = 0
indices = index[pais].tolist()
for i in indices:
    indice = i
if (indice != 0):
    anios = np.array(list(archivo.columns.values[4:65]))
    poblacion=np.array(archivo.iloc[indice, 4:65])
    anios = anios.astype(int)
    poblacion= poblacion.astype(int)
    X = anios[:, np.newaxis]
    poblacion = (poblacion)
    while True:
        X_train, Xtest, y_train, y_test = train_test_split(X, poblacion)
        mlr = MLPRegressor(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(3, 3), random_state=1)
        mlr.fit(X_train, y_train)
        if (mlr.score(X_train, y_train) > 0.98):
            print("Score: ", mlr.score(X_train, y_train))
            break
    prediccion = mlr.predict([[anio]])
    print(f"Poblacion en {paisabuscar} en el año: {anio}:", int(prediccion))
else:
    print("País no encontrado")