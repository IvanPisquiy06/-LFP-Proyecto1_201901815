import tkinter as tk
from tkinter import filedialog
import json
import math
from graphviz import Digraph
import re

contenido_json = None

def example():
    print("Hola")

#Seleccionar un archivo JSON
def abrir_archivo():
    global contenido_json
    # Abre el diálogo de buscar archivo y retorna la ruta del archivo seleccionado
    ruta_archivo = filedialog.askopenfilename(filetypes=[('Archivos JSON', '*.json')])

    # Verifica si se seleccionó un archivo y si es así, lo lee y lo devuelve como un diccionario de Python
    if ruta_archivo:
        with open(ruta_archivo, 'r') as archivo_json:
            contenido_json = json.load(archivo_json)
        return contenido_json
    else:
        return None
    

#funcion para traducir el nombre de los colores    
def colores(color):
    if color == 'Amarillo':
        return 'yellow'
    if color == 'Rojo':
        return 'red'
    if color == 'Azul':
        return 'blue'
    if color == 'Negro':
        return 'black'
    if color == 'Blanco':
        return 'white'
    if color == 'Verde':
        return 'green'
    
    
#Guarda archivo actual (actualizar)    
def actualizar_archivo():
    global contenido_json
    
    # Abre el diálogo de abrir archivo y retorna la ruta del archivo seleccionado
    ruta_archivo = filedialog.askopenfilename(filetypes=[('Archivos JSON', '*.json')])
    
    # Verifica si se seleccionó un archivo y si es así, actualiza el contenido_json en el archivo
    if ruta_archivo:
        with open(ruta_archivo, 'r+') as archivo_json:
            contenido_existente = json.load(archivo_json)
            contenido_existente.update(contenido_json)
            archivo_json.seek(0)
            json.dump(contenido_existente, archivo_json, indent=4)
            archivo_json.truncate()
        print(f"Archivo actualizado en {ruta_archivo}")
    else:
        print("No se ha seleccionado un archivo válido.")

#Guarda un archivo nuevo
def guardar_archivo():
    global contenido_json
    
    # Abre el diálogo de guardar archivo y retorna la ruta del archivo seleccionado
    ruta_archivo = filedialog.asksaveasfilename(filetypes=[('Archivos JSON', '*.json')])
    
    # Verifica si se seleccionó un archivo y si es así, escribe el contenido_json en el archivo
    if ruta_archivo:
        with open(ruta_archivo + '.json', 'w') as archivo_json:
            json.dump(contenido_json, archivo_json)
        print(f"Archivo guardado en {ruta_archivo}")
    else:
        print("No se ha seleccionado un archivo válido.")

def analizar_operaciones():
    global contenido_json
    no_operacion = 0
    operaciones = contenido_json["operaciones"]
    bg_color = colores(contenido_json["Color-Fondo-Nodo"])
    font_color = colores(contenido_json["Color-Fuente-Nodo"])
    dot = Digraph(comment=contenido_json["Texto"])
    nodos = {}
    bordes = {}
    for op in operaciones:
        print(op['Operacion'])
        tipo_operacion = op["Operacion"]
        valor1 = op["Valor1"]
        valor2 = op["Valor2"]
        resultado = 0
        no_operacion = 1 + no_operacion
        
        if isinstance(valor1, dict):
            nodo_anidado, borde_anidado, valor1 = resolver_operacion_anidada(valor1)
            nodos.update(nodo_anidado)
            bordes.update(borde_anidado)
        if isinstance(valor2, dict):
            nodo_anidado, borde_anidado, valor2 = resolver_operacion_anidada(valor2)
            nodos.update(nodo_anidado)
            bordes.update(borde_anidado)
        
        if tipo_operacion == "Suma":
            resultado = valor1 + valor2
            nodos[str(valor1)] = str(valor1)
            nodos[str(valor2)] = str(valor2)
            nodos[tipo_operacion+str(no_operacion)] = tipo_operacion+str(no_operacion)
            nodos[str(resultado)] = str(resultado)
            bordes[str(valor1), tipo_operacion+str(no_operacion)] = (str(valor1), tipo_operacion+str(no_operacion))
            bordes[str(valor2), tipo_operacion+str(no_operacion)] = (str(valor2), tipo_operacion+str(no_operacion))
            bordes[tipo_operacion+str(no_operacion), str(resultado)] = (tipo_operacion+str(no_operacion), str(resultado))
            
        elif tipo_operacion == "Resta":
            resultado = valor1 - valor2
            nodos[str(valor1)] = str(valor1)
            nodos[str(valor2)] = str(valor2)
            nodos[tipo_operacion+str(no_operacion)] = tipo_operacion+str(no_operacion)
            nodos[str(resultado)] = str(resultado)
            bordes[str(valor1), tipo_operacion+str(no_operacion)] = (str(valor1), tipo_operacion+str(no_operacion))
            bordes[str(valor2), tipo_operacion+str(no_operacion)] = (str(valor2), tipo_operacion+str(no_operacion))
            bordes[tipo_operacion+str(no_operacion), str(resultado)] = (tipo_operacion+str(no_operacion), str(resultado))

        elif tipo_operacion == "Multiplicacion":
            resultado = valor1 * valor2
            nodos[str(valor1)] = str(valor1)
            nodos[str(valor2)] = str(valor2)
            nodos[tipo_operacion+str(no_operacion)] = tipo_operacion+str(no_operacion)
            nodos[str(resultado)] = str(resultado)
            bordes[str(valor1), tipo_operacion+str(no_operacion)] = (str(valor1), tipo_operacion+str(no_operacion))
            bordes[str(valor2), tipo_operacion+str(no_operacion)] = (str(valor2), tipo_operacion+str(no_operacion))
            bordes[tipo_operacion+str(no_operacion), str(resultado)] = (tipo_operacion+str(no_operacion), str(resultado))

        elif tipo_operacion == "Division":
            resultado = valor1 / valor2
            nodos[str(valor1)] = str(valor1)
            nodos[str(valor2)] = str(valor2)
            nodos[tipo_operacion+str(no_operacion)] = tipo_operacion+str(no_operacion)
            nodos[str(resultado)] = str(resultado)
            bordes[str(valor1), tipo_operacion+str(no_operacion)] = (str(valor1), tipo_operacion+str(no_operacion))
            bordes[str(valor2), tipo_operacion+str(no_operacion)] = (str(valor2), tipo_operacion+str(no_operacion))
            bordes[tipo_operacion+str(no_operacion), str(resultado)] = (tipo_operacion+str(no_operacion), str(resultado))

        elif tipo_operacion == "Potencia":
            resultado = valor1 ** valor2
            nodos[str(valor1)] = str(valor1)
            nodos[str(valor2)] = str(valor2)
            nodos[tipo_operacion+str(no_operacion)] = tipo_operacion+str(no_operacion)
            nodos[str(resultado)] = str(resultado)
            bordes[str(valor1), tipo_operacion+str(no_operacion)] = (str(valor1), tipo_operacion+str(no_operacion))
            bordes[str(valor2), tipo_operacion+str(no_operacion)] = (str(valor2), tipo_operacion+str(no_operacion))
            bordes[tipo_operacion+str(no_operacion), str(resultado)] = (tipo_operacion+str(no_operacion), str(resultado))

        elif tipo_operacion == "Raiz":
            resultado = valor1 ** (1/valor2)
            nodos[str(valor1)] = str(valor1)
            nodos[str(valor2)] = str(valor2)
            nodos[tipo_operacion+str(no_operacion)] = tipo_operacion+str(no_operacion)
            nodos[str(resultado)] = str(resultado)
            bordes[str(valor1), tipo_operacion+str(no_operacion)] = (str(valor1), tipo_operacion+str(no_operacion))
            bordes[str(valor2), tipo_operacion+str(no_operacion)] = (str(valor2), tipo_operacion+str(no_operacion))
            bordes[tipo_operacion+str(no_operacion), str(resultado)] = (tipo_operacion+str(no_operacion), str(resultado))

        elif tipo_operacion == "Inverso":
            resultado = 1/valor1
            nodos[str(valor1)] = str(valor1)
            nodos[tipo_operacion+str(no_operacion)] = tipo_operacion+str(no_operacion)
            nodos[str(resultado)] = str(resultado)
            bordes[str(valor1), tipo_operacion+str(no_operacion)] = (str(valor1), tipo_operacion+str(no_operacion))
            bordes[tipo_operacion+str(no_operacion), str(resultado)] = (tipo_operacion+str(no_operacion), str(resultado))

        elif tipo_operacion == "Seno":
            resultado = math.sin(math.radians(valor1))
            nodos[str(valor1)] = str(valor1)
            nodos[tipo_operacion+str(no_operacion)] = tipo_operacion+str(no_operacion)
            nodos[str(resultado)] = str(resultado)
            bordes[str(valor1), tipo_operacion+str(no_operacion)] = (str(valor1), tipo_operacion+str(no_operacion))
            bordes[tipo_operacion+str(no_operacion), str(resultado)] = (tipo_operacion+str(no_operacion), str(resultado))

        elif tipo_operacion == "Coseno":
            resultado = math.cos(math.radians(valor1))
            nodos[str(valor1)] = str(valor1)
            nodos[tipo_operacion+str(no_operacion)] = tipo_operacion+str(no_operacion)
            nodos[str(resultado)] = str(resultado)
            bordes[str(valor1), tipo_operacion+str(no_operacion)] = (str(valor1), tipo_operacion+str(no_operacion))
            bordes[tipo_operacion+str(no_operacion), str(resultado)] = (tipo_operacion+str(no_operacion), str(resultado))

        elif tipo_operacion == "Tangente":
            resultado = math.tan(math.radians(valor1))
            nodos[str(valor1)] = str(valor1)
            nodos[tipo_operacion+str(no_operacion)] = tipo_operacion+str(no_operacion)
            nodos[str(resultado)] = str(resultado)
            bordes[str(valor1), tipo_operacion+str(no_operacion)] = (str(valor1), tipo_operacion+str(no_operacion))
            bordes[tipo_operacion+str(no_operacion), str(resultado)] = (tipo_operacion+str(no_operacion), str(resultado))

        elif tipo_operacion == "Mod":
            resultado = valor1 % valor2
            nodos[str(valor1)] = str(valor1)
            nodos[str(valor2)] = str(valor2)
            nodos[tipo_operacion+str(no_operacion)] = tipo_operacion+str(no_operacion)
            nodos[str(resultado)] = str(resultado)
            bordes[str(valor1), tipo_operacion+str(no_operacion)] = (str(valor1), tipo_operacion+str(no_operacion))
            bordes[str(valor2), tipo_operacion+str(no_operacion)] = (str(valor2), tipo_operacion+str(no_operacion))
            bordes[tipo_operacion+str(no_operacion), str(resultado)] = (tipo_operacion+str(no_operacion), str(resultado))

    for key in nodos:
        dot.node(key, style='filled', fillcolor=bg_color, fontcolor=font_color)
    for key in bordes:
        dot.edge(key[0], key[1])
        
    dot.render('operaciones', view=True)
            
def resolver_operacion_anidada(op_anidada):
    tipo_operacion = op_anidada["Operacion"]
    valor1 = op_anidada["Valor1"]
    nodos= {}
    bordes = {}
    
    if isinstance(valor1, dict):
        nodo_anidado, borde_anidado, valor1 = resolver_operacion_anidada(valor1)
        nodos.update(nodo_anidado)
        bordes.update(borde_anidado)
    if tipo_operacion == 'Potencia' or 'Suma' or 'Potencia' or 'Multiplicación' or 'Division' or 'Raiz':
        valor2 = op_anidada["Valor2"]
        if isinstance(valor2, dict):
            nodo_anidado, borde_anidado, valor2 = resolver_operacion_anidada(valor2)
            nodos.update(nodo_anidado)
            bordes.update(borde_anidado)
    
    if tipo_operacion == "Suma":
        resultado = valor1 + valor2
        nodos[str(valor1)] = str(valor1)
        nodos[str(valor2)] = str(valor2)
        nodos[tipo_operacion] = tipo_operacion
        nodos[str(resultado)] = str(resultado)
        bordes[str(valor1), tipo_operacion] = (str(valor1), tipo_operacion)
        bordes[str(valor2), tipo_operacion] = (str(valor2), tipo_operacion)
        bordes[tipo_operacion, str(resultado)] = (tipo_operacion, str(resultado))
        
    elif tipo_operacion == "Resta":
        resultado = valor1 - valor2
        nodos[str(valor1)] = str(valor1)
        nodos[str(valor2)] = str(valor2)
        nodos[tipo_operacion] = tipo_operacion
        nodos[str(resultado)] = str(resultado)
        bordes[str(valor1), tipo_operacion] = (str(valor1), tipo_operacion)
        bordes[str(valor2), tipo_operacion] = (str(valor2), tipo_operacion)
        bordes[tipo_operacion, str(resultado)] = (tipo_operacion, str(resultado))

    elif tipo_operacion == "Multiplicacion":
        resultado = valor1 * valor2
        nodos[str(valor1)] = str(valor1)
        nodos[str(valor2)] = str(valor2)
        nodos[tipo_operacion] = tipo_operacion
        nodos[str(resultado)] = str(resultado)
        bordes[str(valor1), tipo_operacion] = (str(valor1), tipo_operacion)
        bordes[str(valor2), tipo_operacion] = (str(valor2), tipo_operacion)
        bordes[tipo_operacion, str(resultado)] = (tipo_operacion, str(resultado))

    elif tipo_operacion == "Division":
        resultado = valor1 / valor2
        nodos[str(valor1)] = str(valor1)
        nodos[str(valor2)] = str(valor2)
        nodos[tipo_operacion] = tipo_operacion
        nodos[str(resultado)] = str(resultado)
        bordes[str(valor1), tipo_operacion] = (str(valor1), tipo_operacion)
        bordes[str(valor2), tipo_operacion] = (str(valor2), tipo_operacion)
        bordes[tipo_operacion, str(resultado)] = (tipo_operacion, str(resultado))

    elif tipo_operacion == "Potencia":
        resultado = valor1 ** valor2
        nodos[str(valor1)] = str(valor1)
        nodos[str(valor2)] = str(valor2)
        nodos[tipo_operacion] = tipo_operacion
        nodos[str(resultado)] = str(resultado)
        bordes[str(valor1), tipo_operacion] = (str(valor1), tipo_operacion)
        bordes[str(valor2), tipo_operacion] = (str(valor2), tipo_operacion)
        bordes[tipo_operacion, str(resultado)] = (tipo_operacion, str(resultado))

    elif tipo_operacion == "Raiz":
        resultado = valor1 ** (1/valor2)
        nodos[str(valor1)] = str(valor1)
        nodos[str(valor2)] = str(valor2)
        nodos[tipo_operacion] = tipo_operacion
        nodos[str(resultado)] = str(resultado)
        bordes[str(valor1), tipo_operacion] = (str(valor1), tipo_operacion)
        bordes[str(valor2), tipo_operacion] = (str(valor2), tipo_operacion)
        bordes[tipo_operacion, str(resultado)] = (tipo_operacion, str(resultado))

    elif tipo_operacion == "Inverso":
        resultado = 1/valor1
        nodos[str(valor1)] = str(valor1)
        nodos[tipo_operacion] = tipo_operacion
        nodos[str(resultado)] = str(resultado)
        bordes[str(valor1), tipo_operacion] = (str(valor1), tipo_operacion)
        bordes[tipo_operacion, str(resultado)] = (tipo_operacion, str(resultado))

    elif tipo_operacion == "Seno":
        resultado = math.sin(math.radians(valor1))
        nodos[str(valor1)] = str(valor1)
        nodos[tipo_operacion] = tipo_operacion
        nodos[str(resultado)] = str(resultado)
        bordes[str(valor1), tipo_operacion] = (str(valor1), tipo_operacion)
        bordes[tipo_operacion, str(resultado)] = (tipo_operacion, str(resultado))

    elif tipo_operacion == "Coseno":
        resultado = math.cos(math.radians(valor1))
        nodos[str(valor1)] = str(valor1)
        nodos[tipo_operacion] = tipo_operacion
        nodos[str(resultado)] = str(resultado)
        bordes[str(valor1), tipo_operacion] = (str(valor1), tipo_operacion)
        bordes[tipo_operacion, str(resultado)] = (tipo_operacion, str(resultado))

    elif tipo_operacion == "Tangente":
        resultado = math.tan(math.radians(valor1))
        nodos[str(valor1)] = str(valor1)
        nodos[tipo_operacion] = tipo_operacion
        nodos[str(resultado)] = str(resultado)
        bordes[str(valor1), tipo_operacion] = (str(valor1), tipo_operacion)
        bordes[tipo_operacion, str(resultado)] = (tipo_operacion, str(resultado))

    elif tipo_operacion == "Mod":
        resultado = valor1 % valor2
        nodos[str(valor1)] = str(valor1)
        nodos[str(valor2)] = str(valor2)
        nodos[tipo_operacion] = tipo_operacion
        nodos[str(resultado)] = str(resultado)
        bordes[str(valor1), tipo_operacion] = (str(valor1), tipo_operacion)
        bordes[str(valor2), tipo_operacion] = (str(valor2), tipo_operacion)
        bordes[tipo_operacion, str(resultado)] = (tipo_operacion, str(resultado))

    return nodos, bordes, resultado

def verificar_errores():
    # cargar el archivo JSON
    global contenido_json
    
    # expresión regular para verificar si una cadena es un número válido
    regex_numero = re.compile(r'^-?(0|[1-9]\d*)(\.\d+)?([eE][-+]?\d+)?$')
    
    # expresión regular para verificar si una cadena es un booleano válido
    regex_booleano = re.compile(r'^(true|false)$', re.IGNORECASE)
    
    # expresión regular para verificar si una cadena es nula
    regex_nulo = re.compile(r'^null$', re.IGNORECASE)
    
    errores = []
    no_error = 0
    
    for fila, registro in enumerate(contenido_json):
        for columna, valor in registro.items():
            if isinstance(valor, str):
                # verificar si la cadena es un número válido
                if regex_numero.match(valor):
                    continue
                
                # verificar si la cadena es un booleano válido
                if regex_booleano.match(valor):
                    continue
                
                # verificar si la cadena es nula
                if regex_nulo.match(valor):
                    continue
                
                # si no es ninguno de los anteriores, es un error
                errores.append({
                    "No.": no_error + 1,
                    "Descripcion-Token": {
                        "Lexema": valor,
                        "Tipo": "Error",
                        "Columna": columna,
                        "Fila": fila + 1
                    }
                })
                no_error += 1
    
    # si no hubo errores, retornar un mensaje
    if no_error == 0:
        errores.append({"mensaje": "No se encontraron errores léxicos."})

    with open('errores.json', 'w') as f:
            json.dump(errores, f)


#Cierra el programa
def cerrar_programa():
    root.destroy()
    exit()

def temas_ayuda():
    root2 = tk.Tk()
    root2.title("Temas de Ayuda")
    nombre = tk.Label(root2,text="Ivan de Jesus Pisquiy Escobar")
    nombre.grid(row=0, column=0, padx=10, pady=10)
    carne = tk.Label(root2, text="201901815")
    carne.grid(row=1, column=0, padx=10, pady="10")
    curso = tk.Label(root2, text="Lenguajes Formales y de Programación A-")
    curso.grid(row=2, column=0, padx=10, pady=10)

# Creamos una ventana principal
root = tk.Tk()
root.title("Analizador Léxico")

#Etiquetas
titulo1 = tk.Label(root,text="Archivo")
titulo1.grid(row=0, column=0, padx=10, pady=10)
titulo1.config(fg='black',
               bg='yellow',
               font=('Open sans', 17))

titulo2 = tk.Label(root,text="Ayuda")
titulo2.grid(row=0, column=1, padx=10, pady=10)
titulo2.config(fg='black',
               bg='yellow',
               font=('Open sans', 17))

#Creamos botones
button1 = tk.Button(root, text="Abrir", command=abrir_archivo, fg="black", bg="#98FB98", bd=0)
button1.grid(row=1, column=0, padx=10, pady=10)
button2 = tk.Button(root, text="Guardar", command=actualizar_archivo, fg="black", bg="#98FB98", bd=0)
button2.grid(row=2, column=0, padx=10, pady=10)
button3 = tk.Button(root, text="Guardar Como", command=guardar_archivo, fg="black", bg="#98FB98", bd=0)
button3.grid(row=3, column=0, padx=10, pady=10)
button4 = tk.Button(root, text="Analizar", command=analizar_operaciones, fg="black", bg="#98FB98", bd=0)
button4.grid(row=4, column=0, padx=10, pady=10)
button5 = tk.Button(root, text="Errores", command=verificar_errores, fg="black", bg="#98FB98", bd=0)
button5.grid(row=5, column=0, padx=10, pady=10)
button6 = tk.Button(root, text="Salir", command=cerrar_programa, fg="black", bg="#98FB98", bd=0)
button6.grid(row=6, column=0, padx=10, pady=10)
button7 = tk.Button(root, text="Manual de Usuario", command=example, fg="black", bg="#98FB98", bd=0)
button7.grid(row=1, column=1, padx=10, pady=10)
button8 = tk.Button(root, text="Manual Técnico", command=example, fg="black", bg="#98FB98", bd=0)
button8.grid(row=2, column=1, padx=10, pady=10)
button9 = tk.Button(root, text="Temas de Ayuda", command=temas_ayuda, fg="black", bg="#98FB98", bd=0)
button9.grid(row=3, column=1, padx=10, pady=10)

# Ejecutamos el bucle principal de la aplicación
root.mainloop()
