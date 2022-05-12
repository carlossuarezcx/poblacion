import tkinter
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np

root = tkinter.Tk()
root.geometry("800x600")
root.wm_title("Calculo de población")

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
def calcular():
    fig = Figure(figsize=(5, 4), dpi=100)
    archivo = pd.read_csv('API_SP.POP.TOTL_DS2_es_csv_v2_4004971.csv', header=2, keep_default_na=False)

    paisabuscar = "México"
    anio = 2025

    index = archivo.index
    pais = archivo["Country Name"] == paisabuscar
    indice = 0
    indices = index[pais].tolist()
    for i in indices:
        indice = i
    if (indice != 0):
        anios = np.array(list(archivo.columns.values[4:65]))
        poblacion = np.array(archivo.iloc[indice, 4:65])
        anios = anios.astype(int)
        poblacion = poblacion.astype(int)
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

    fig.add_subplot(111).plot(anios,poblacion)
    ay = fig.gca()
    ay.get_xaxis().get_major_formatter().set_useOffset(False)
    ay.get_xaxis().get_major_formatter().set_scientific(False)
    ay.get_yaxis().get_major_formatter().set_useOffset(False)
    ay.get_yaxis().get_major_formatter().set_scientific(False)
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

button = tkinter.Button(master=root, text="Salir", command=_quit)
button.pack(side=tkinter.BOTTOM)

button1 = tkinter.Button(master=root, text="Calcular", command=calcular)
button1.pack(side=tkinter.BOTTOM)
tkinter.mainloop()
# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.