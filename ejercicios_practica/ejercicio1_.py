# JSON ETL [Python]
# Ejercicios de práctica

# Autor: Inove Coding School
# Version: 2.0

# IMPORTANTE: NO borrar los comentarios
# que aparecen en verde con el hashtag "#"

import json


data_persona = {
    "nombre": "Andres",
    "apellido": "De Innocentiis",
    "DNI": "36.487.599",
    "prendas": [
        {
            "prenda": "remera rota",
            "cantidad": 2
        },
        {
            "prenda": "pantufla vieja",
            "cantidad": 1
        },
        {
            "prenda": "jeans",
            "cantidad": 3
        },
    ],
    "edad": 29,
    "profesion": "abogado"
}


def serializar(hash:dict)->None:
    print("Funcion que genera un archivo JSON")
    # JSON Serialize
    # Armar un JSON que represente los datos personales
    # de su persona (puede invitar los datos sino quiere exponer
    # información confidencial)

    # Debe armar un JSON que tenga como datos
    # nombre, apellido, DNI
    # Dentro debe tener una lista donde coloque cantidad de elementos de vestir
    # ejemplo -->
    #  { "prenda": "zapatilla", "cantidad": 4 }
    #  { "prenda": "remeras", "cantidad": 12 }
    # Que su lista de prendas dentro del JSON tenga al menos 2 prendas
    
    """
    /// NOTA:
    En realidad, el diccionario lo armé afuera para que tenga más sentido pasarlo como parámetro 
    y que la función se pueda usar para convertir a json 
    cualquier diccionario que se le pase como parámetro.
    """
    
    # json_data = {...}

    # Una vez que finalice el JSON realice un "dump" para almacenarlo en
    # un archivo que usted defina

    # Observe el archivo y verifique que se almaceno lo deseado
    
    with open('mi_json.json', 'w') as jsonfile:
        data = [hash]
        json.dump(data, jsonfile, indent=4)
    


def deserializar(nombre_archivo:str)->str:
    print("Funcion que lee un archivo JSON")
    # JSON Deserialize
    # Basado en la función  anterior debe abrir y leer el contenido
    # del archivo y guardarlo en un objeto JSON utilizando el método
    # load()
    with open(f"{nombre_archivo}.json", 'r') as jsonfile:
        data = json.load(jsonfile)
    # Luego debe convertir ese JSON data en json_string utilizando
    # el método "dumps" y finalmente imprimir en pantalla el resultado
    # Recuerde utilizar indent=4 para poder observar mejor el resultado
    # en pantalla y comparelo contra el JSON que generó en la función anterior
    
    dic_json = json.dumps(data, indent=4)
    
    return dic_json

if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    
    serializar(data_persona)
    json_str = deserializar("mi_json")

    print(json_str)
    print("terminamos")
