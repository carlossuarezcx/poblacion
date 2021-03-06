import tkinter
from tkinter import ttk
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import numpy as np

root = tkinter.Tk()
ancho_ventana = 1280
alto_ventana = 900
x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2
posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
root.geometry(posicion)
root.resizable(0,0)
root.wm_title("Calculo de población")
archivo = pd.read_csv('API_SP.POP.TOTL_DS2_es_csv_v2_4004971.csv', header=2, keep_default_na=False)
paises = archivo['Country Name'].tolist()
paises = [l for l in paises if l != ""]
fig = Figure(figsize=(5, 5), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
ax = fig.add_subplot(111)

def calcular():
    ax.clear()
    paisabuscar = str(combo.get())
    if (len(entry.get())==0 or int(entry.get()) < 0 ):
        label2.config(text="Ingrese un año correcto",font=("Courier", 15) ,fg= "red")
    else:
        anio = int(entry.get())
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
            score = 0
            i = 0
            while i<1000:
                X_train, Xtest, y_train, y_test = train_test_split(X, poblacion)
                mlr = MLPRegressor(solver='lbfgs', alpha=1e-8, hidden_layer_sizes=(3, 3), random_state=1, max_iter=1000)
                mlr.fit(X_train, y_train)
                score = mlr.score(X_train, y_train)
                #print(score)
                i+=1
                if (score > 0.85):
                    break
            if score < 0.85:
                label2.config(text="No se cuenta con la información suficiente, porcentaje muy bajo:" + str("{:.2f}".format(score*100))+"%",font=("Courier", 15),fg= "black")
            else:
                prediccion = mlr.predict([[anio]])
                numero = "{:,}".format(int(prediccion))
                #entry.delete(0, "end")
                ax.scatter(anios, poblacion)
                ax.scatter(anio, prediccion, c="red")
                ax.annotate(numero, (anio, prediccion))
                ax.set_xlabel('Años')
                ax.set_ylabel('Poblacion')
                ax.get_xaxis().get_major_formatter().set_useOffset(False)
                ax.get_xaxis().get_major_formatter().set_scientific(False)
                ax.get_yaxis().get_major_formatter().set_useOffset(False)
                ax.get_yaxis().get_major_formatter().set_scientific(False)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
                #"{:.2f}".format(3.1415926)
                #print (score)
                label2.config(text="La poblacion estimada para el año: "+str(anio)+" en: "+paisabuscar+" será de: "+str(numero) + " con un porcentaje de: " +str("{:.6f}".format(score*100))+"%",font=("Courier", 15),fg= "black")
        else:
            print("País no encontrado")

button1 = tkinter.Button(master=root, text="Calcular", command=calcular, font=("Courier", 15))
button1.pack(side=tkinter.BOTTOM)
label2 = tkinter.Label(master=root,text="")
label2.pack(side=tkinter.BOTTOM)
entry = tkinter.Entry(master=root,font=("Courier", 15))
entry.pack(side=tkinter.BOTTOM)
label = tkinter.Label(master=root,text="Ingrese el año a calcular la predicción: ",font=("Courier", 15))
label.pack(side=tkinter.BOTTOM)
combo = ttk.Combobox(master=root,font=("Courier", 15), values=paises)
combo.pack(side=tkinter.BOTTOM)
label = tkinter.Label(master=root,text="Seleccione el país a calcular la predicción: ",font=("Courier", 15))
label.pack(side=tkinter.BOTTOM)
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
tkinter.mainloop()
