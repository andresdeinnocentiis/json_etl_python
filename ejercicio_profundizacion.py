"""
EJERCICIO DE PROFUNDIZACIÓN:
API MERCADO LIBRE
"""

import json
import requests

import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import seaborn as sns
from seaborn.matrix import heatmap


# GENERAMOS UN JSON A PARTIR DE LA RESPONSE DE LA URL:
def convert_to_json(url:str)->json:
    response = requests.get(url)
    data = response.json()

    return data

def fetch(json_data:json,filtro:str="moneda",moneda:str="ARS", ciudad:str=None, provincia:str=None,precio:str=None)->list: 
    # El ejercicio pedía solo condición y precio, pero tomé otros valores para poder quizas hacer una medición que muestre la variación del precio en base a los atributos de cada departamento
    
    filtros = {"moneda":"currency_id",
               "ciudad":"address",
               "provincia":"address",
               "precio":"price"
               }
    
    
    if filtro not in filtros.keys():
        raise ValueError("Filtro inválido. Filtros válidos: 'moneda','ciudad','provincia','precio'.")
            
    valor_filtro = filtrar(filtro,moneda,ciudad,provincia,precio)
    
        
    lista_items = ["id","title", "price","address","attributes","condition"]
    dataset = []
    clave = ""
    
    
    for resultado in json_data["results"]:
        if valor_filtro[0] == "ciudad":
            clave = resultado["address"].get("city_name")
        elif valor_filtro[0] == "provincia":
            clave = resultado["address"].get("state_name")
        elif valor_filtro[0] == "precio":
            clave = resultado["price"]
        elif valor_filtro[0] == "moneda":
            clave = resultado["currency_id"]
        
        if str(clave) == valor_filtro[1]:
        
            dic = {}
            for i in lista_items:
                if i != "attributes" and i != "address":
                    dic[i] = resultado.get(i)
                elif i == "address":
                    dic["state_name"] = resultado["address"].get("state_name")
                    dic["city_name"] = resultado["address"].get("city_name")
                elif i == "attributes":
                    for x in resultado["attributes"]:
                        
                        if x.get("id") == "TOTAL_AREA":
                            dic["superficie_m2"] = x.get("value_name").replace(x.get("value_name")[-3:],"")
                        elif x.get("id") == "PROPERTY_TYPE":
                            dic["prop_type"] = x.get("value_name")
                        elif x.get("id") == "BEDROOMS":
                            dic["dorms"] = x.get("value_name")
                        elif x.get("id") == "ROOMS":
                            dic["ambientes"] = x.get("value_name", dic["dorms"])
                        elif x.get("id") == "FULL_BATHROOMS":
                            dic["baths"] = x.get("value_name")

                        tiene_aire = [resultado["attributes"][x].get("value_name") for x in range(len(resultado["attributes"])) if resultado["attributes"][x].get("id") == "HAS_AIR_CONDITIONING" and resultado["attributes"][x].get("value_name") == "Sí"]
                        if "Sí" in tiene_aire:
                            dic["aire_acond"] = "Si"
                
                        else:
                            dic["aire_acond"] = "No"           
            if not "ambientes" in dic.keys():
                dic["ambientes"] = dic.get("dorms")          
            dataset.append(dic)
            
           
    return dataset


def transform(dataset:list, min:int, max:int)->list:
    lista_parametros = []
    lista_max = [x["price"] for x in dataset if x["price"] > max]
    lista_min = [x["price"] for x in dataset if x["price"] < min]
    lista_minmax = [x["price"] for x in dataset if x["price"] <= max and x["price"] >= min] 
    
    min_count = len(lista_min)
    lista_parametros.append(min_count)
    min_max_count = len(lista_minmax)
    lista_parametros.append(min_max_count)
    max_count = len(lista_max)
    lista_parametros.append(max_count)
    
    # print(f"LISTA MIN MAX: \n{lista_minmax}\nLISTA MIN: \n{lista_min}\nLISTA MAX: \n{lista_max}")
    # (El print era solo para testear, y lo dejo por si también lo quieren testear)
    return lista_parametros    


def report(data:list)->None:
    min = data[0]
    max = data[2]
    fig = plt.figure()
    fig.suptitle('Precios Min & Max', fontsize=16)
    ax = fig.add_subplot()
    explode = (0.1, 0) 

    ax.pie([min,max], labels=("Precios Mínimos","Precios Máximos"),
           explode=explode, autopct='%1.1f%%', shadow=True, startangle=90
           )
    ax.axis('equal')
    plt.show()
    
    
    
# ============================================================   
# --------------------- OPCIONALES: --------------------------
# ============================================================

# 1. Crea un archivo json por si quiero leer los datos de forma más ordenada o por si lo necesito después (en este ejercicio no lo necesité trabajar).

def convert_to_jsonfile(dataset)->None: 
    with open('deptos_baires.json', 'w', encoding='utf-8') as jsonfile: 
        json.dump(dataset, jsonfile, indent=4,ensure_ascii=False) #encoding y ensure_ascii es para que salgan los caracteres especiales que en formato unicode no se muestran.

# 2. Creo función para filtrar (un filtro simple de un solo filtro para probar experimentar).

def filtrar(filtro:str, moneda, ciudad, provincia, precio)->list:
    filtros = {"moneda":"currency_id",
               "ciudad":"address",
               "provincia":"address",
               "precio":"price"
               }
    parametro = []
    if filtro not in filtros.keys():
        raise ValueError("Filtro inválido. Filtros válidos: 'moneda','ciudad','provincia','precio'.")
        #parametro[filtros.get("moneda")] = moneda
    elif filtro == "moneda" and (moneda != "ARS" and moneda !="USD"):
        raise ValueError("Se esperaban los valores 'ARS' o 'USD' para el filtro 'moneda'.")
    elif filtro == "ciudad" and not ciudad:
        raise ValueError("Se esperaba un valor ciudad para el filtro 'ciudad'.")
    elif filtro == "provincia" and not provincia:
        raise ValueError("Se esperaba un valor provincia para el filtro 'provincia'.")
    elif filtro == "precio" and not precio:
        raise ValueError("Se esperaba un valor INT precio para el filtro 'precio'.")
    else:
        if filtro == "moneda":
            if not moneda:
                parametro.append("moneda")
                parametro.append("ARS")
            else:
                parametro.append("moneda")
                parametro.append(moneda)
            
        elif filtro == "ciudad":
            parametro.append("ciudad")
            parametro.append(ciudad)
            
        elif filtro == "provincia":
            parametro.append("provincia")
            parametro.append(provincia)
            
        elif filtro == "precio":
            parametro.append("precio")
            parametro.append(precio)
                       
    return parametro

# 3. Uso los parámetros extra que tomé y los uso para ver la correlación que hay entre los distintos atributos de cada departamento con el precio.

def get_correlation(deptos_filtro_original, plot)->None:
    df = pd.DataFrame(deptos_filtro_original)
    
    df = df.drop(["id","title"], axis=1) # Eliminé estas 2 columnas porque no aportan a la medición
    
    # Convierto los valores de las columnas en categóricos (y luego numéricos) o numéricos según corresponda (antes eran de tipo object.)
    
    df["dorms"] = pd.to_numeric(df.dorms)
    df["baths"] = pd.to_numeric(df.baths)
    df["ambientes"] = pd.to_numeric(df.ambientes)
    df["superficie_m2"] = pd.to_numeric(df.superficie_m2)
    df['state_name']=df['state_name'].astype('category').cat.codes
    df['city_name']=df['city_name'].astype('category').cat.codes
    df['aire_acond']=df['aire_acond'].astype('category').cat.codes
    df['prop_type']=df['prop_type'].astype('category').cat.codes
    df['condition']=df['condition'].astype('category').cat.codes
    
    
    
    # correlacion = df.corr().loc["price", :].sort_values(ascending=False)
    # print(correlacion) # Descomentar para ver la correlación por consola.
    if plot == "pairplot":
        sns.pairplot(df[['price', 'prop_type', 'condition','superficie_m2','aire_acond','baths', 'state_name', 'dorms', 'ambientes','city_name']], hue='price',palette="tab10")
        plt.show()
    elif plot == "heatmap":
        sns.heatmap(df[['price', 'prop_type', 'condition','superficie_m2','aire_acond','baths', 'state_name', 'dorms', 'ambientes','city_name']].corr(),annot=True)
        plt.show()
    else:
        raise ValueError("Se esperaban los valores 'pairplot' o 'heatmap' para el parámetro 'plot'.")
    
# Creo una función que aglutina todo el proceso del ejercicio, que hace de "main":
def ejecutar(min:int,max:int): 
  
    print("EJERCICIO API - MERCADO LIBRE - DEPARTAMENTOS EN ALQUILER")
    print("by @andresdeinnocentiis")
    url = 'https://api.mercadolibre.com/sites/MLA/search?category=MLA1459&q=Departamentos%20Alquilers%20Buenos%20Aires%20&limit=50'
    json_deptos = convert_to_json(url) # Contiene TODOS los datos bajados de la url
    deptos_filtro_original = deptos_filtrados = fetch(json_deptos)
    deptos_filtrados = fetch(json_deptos,filtro="provincia",provincia="Buenos Aires Interior") 
    print(deptos_filtrados)
    
    # ==========ESTA PARTE NO ES NECESARIA (SOLO PARA VER EN CONSOLA)=========================================
    json_str_filtrados = json.dumps(deptos_filtrados, indent=4,ensure_ascii=False).encode('utf8')
    # Le puse codificacion UTF-8 para que se pueda ver la ñ y otros caracteres
    json_str_filtrados_utf8 = json_str_filtrados.decode() # Lo decodifiqué para que se vea limpio (sino aparecían "\n" y otros caracteres)
    print(json_str_filtrados_utf8)
    print("\n")
    #=========================================================================================================
    
    convert_to_jsonfile([deptos_filtro_original]) # Creo el archivo json para que sea más cómodo de ver
    
    lista_min_max = transform(deptos_filtro_original, min, max)
    print(f"CANTIDADES SEGÚN VALORES:\nMIN: {lista_min_max[0]}\nMIN-MAX: {lista_min_max[1]}\nMAX: {lista_min_max[2]}")
    report(lista_min_max)
    
    # EXTRA: VISUALIZAMOS LA CORRELACIÓN ENTRE LAS DISTINTAS VARIABLES CON EL PRECIO (CUANTO INFLUYE CADA VARIABLE CON EL VALOR) Y LO MUESTRO EN UN PAIRPLOT:
    
    get_correlation(deptos_filtro_original,plot="heatmap") # opciones de plot = "heatmap" o "pairplot" 
    
    return None



if __name__ == '__main__':

    ejecutar(2700,10000) # A la función le pasamos los valores mínimos y máximos para ver en el gráfico de tortas
    print("\n")
    print("EJERCICIO API - MERCADO LIBRE - DEPARTAMENTOS EN ALQUILER")
    print("by @andresdeinnocentiis")
    print("\n")
    print("terminamos")
