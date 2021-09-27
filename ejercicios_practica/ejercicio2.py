# JSON ETL [Python]
# Ejercicios de práctica

# Autor: Inove Coding School
# Version: 2.0

# IMPORTANTE: NO borrar los comentarios
# que aparecen en verde con el hashtag "#"

import json
import requests

import matplotlib.pyplot as plt





def title_x_user(url:str)->dict:
    dic_alumnos = {}
    response = requests.get(url)
    data = response.json()
     
    for dic in data:
        
        user = str(dic.get("userId"))
        if f"User{user}" not in dic_alumnos.keys():
            dic_alumnos[f"User{user}"] = {}
            dic_alumnos[f"User{user}"]["cant_titulos"] = 0
            dic_alumnos[f"User{user}"]["titulos"] = []
            
        if dic.get("completed") == True:
            dic_alumnos[f"User{user}"]["cant_titulos"] += 1
            dic_alumnos[f"User{user}"]["titulos"].append(dic.get("title"))  
        
    return dic_alumnos


if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    
    # Ejercicio de consumo de datos por API
    url = "https://jsonplaceholder.typicode.com/todos"
    
    
    
    # El primer paso es que copien esa URL en su explorador web
    # y analicen los datos en general:
    # 1) Observando la URL se puede ver que en total hay 200 entradas,
    # del id=1 al id=200
    # 2) Observando la URL se puede ver que en total hay 10 usuarios,
    # del userId=1 al userId=10
    # 3) En cada entrada se especifica si el usuario completó ese título,
    # mediante el campo "completed".
    
    dic_alumnos = title_x_user(url)
    print(dic_alumnos)
    json_alumnos = json.dumps(dic_alumnos, indent=4)
    print(json_alumnos)
    
    # Alumno, de cada usuario en el total de las 200 entradas
    # debe contar cuantos títulos completó cada usuario (de los 10 posibles)
    # y armar un gráfico de barras resumiendo la información.
    # gráfico en el eje "x" está cada uno de los 10 usuarios y en el eje
    # "y" la cantidad de títulos completados
    
    # Para poder ir haciendo esto debe ir almacenando la información
    # de cada usuario a medida que "itera" en un bucle los datos
    # del JSON recolectado. Al finalizar el bucle deberá tener la data
    # de los 10 usuarios con cuantos títulos completó cada uno.

    # Debe poder graficar dicha información en un gráfico de barras.
    # En caso de no poder hacer el gráfico comience por usar print
    # para imprimir cuantos títulos completó cada usuario
    # y verifique si los primeros usuarios (mirando la página a ojo)
    # los datos recolectados son correctos.

    usuarios = [x for x in dic_alumnos.keys()]
    cantidad_titulos = [valor.get("cant_titulos") for user,valor in dic_alumnos.items()]
    fig = plt.figure()
    fig.suptitle('Titulos por usuario', fontsize=14)
    ax = fig.add_subplot()
    ax.bar(usuarios, cantidad_titulos, label='usuarios',color='green')
    ax.set_facecolor('whitesmoke')
    ax.legend()
    plt.show()
    

    
    print("terminamos")
