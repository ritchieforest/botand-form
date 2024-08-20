# -*- coding: utf-8 -*-

import json
import requests
from models import TrainData

file="./data_initial/articulos.json"

def insert_data(data):
    try:
        insert=TrainData(
            context=data["context"],
            text=data["text"],
            labels=data["labels"]
        )
        insert.save()
        print(insert)
        return True 
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def loadDataRequest(url):
    # Especifica la URL a la que quieres hacer la petición GET
    # Realiza la petición GET
    response = requests.get(url)
    # Verifica si la petición fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Imprime el contenido de la respuesta (normalmente en formato JSON)
        data = response.json()  # Si la respuesta es JSON, puedes convertirla directamente a un diccionario
        #print(data)
        return data
    else:
        print("Error en la petición, código de estado: {response.status_code}")

# Abre y lee el archivo JSON
with open(file, 'r', encoding='utf-8',errors="ignore") as file:
    data = json.load(file)

schemasByContest=loadDataRequest("http://127.0.0.1:8000/api/esquema-por-contexto/")
etiquetas=loadDataRequest("http://127.0.0.1:8000/api/etiquetas/")
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}
listDataCreate=dict({})
for aux in schemasByContest:
    descripcion=aux["descripcion"]
    auxDescripcion=descripcion
    listDataCreate={
        "context":aux["contexto"],
        "text":"",
        "labels":[]
    }
    for item in data:
        # Define las variables a partir del diccionario 'item'
        NOMARTICULO = item.get("NOMARTICULO", "Producto desconocido")
        MARCA = item.get("MARCA", "Marca desconocida")
        PCOMPRA = str(item.get("PCOMPRA", "Precio desconocido"))
        PROVE = item.get("PROVE", "Proveedor desconocido")
        CODIGO = str(item.get("CODIGO", "Código desconocido"))
        CODPROVE = item.get("CODPROVE", "Código proveedor desconocido")

        # Aquí el valor fijo
        MARCA_FIJO = MARCA  # Para usarlo más tarde en el formato
       
        # Formatea la descripción usando las variables
        auxDes = descripcion.format(NOMARTICULO, MARCA, PCOMPRA, PROVE, CODIGO, 20, CODPROVE, MARCA_FIJO)
        auxDesAux=auxDescripcion
        # Asigna la descripción formateada al primer elemento de la lista
        listDataCreate["text"] = auxDes

        # Función auxiliar para encontrar y manejar índices
 
        def safe_index(phrase, substring):
            try:
                return phrase.index(substring)
            except ValueError:
                return -1  # Devuelve -1 si no se encuentra el substring

        # Lista de etiquetas y su configuración correspondiente
        labels_config = [
            ("{0", NOMARTICULO, "PRODUCTO",0),
            ("{1", MARCA, "Cateogoria",1),
            ("{2", PCOMPRA, "Precio",2),
            ("{3", PROVE, "Proveedor",3),
            ("{4", CODIGO, "CODIGO INTERNO",4),
            ("{5", CODPROVE, "CODPROVE",5),
            ("{6", MARCA_FIJO, "MARCA",6)
        ]

        # Agrega las etiquetas a la lista
        list_arr=auxDesAux.replace(",",'').split(" ")
        print(list_arr)
        for placeholder, value, label,index in labels_config:
            start_index = safe_index(auxDesAux, placeholder)
            indice="{"+str(index)+"}"
            auxDesAux=auxDesAux.replace(indice,value)
            if start_index != -1:
                listDataCreate["labels"].append({
                    "end": start_index + 2 + len(value),
                    "start": start_index + 1,
                    "label": label,
                    "position_array":[safe_index(list_arr,indice),len(value.split(" "))]
                })
        print(listDataCreate)
        print("#####################################")
        insert_data(listDataCreate)
        listDataCreate["labels"]=[]
        
    
        #send_post_request("http://127.0.0.1:8000/api/datos-enterenamiento/",data=listDataCreate,headers=headers)
        
    

#print(schemasByContest)

#print(schemasByContest)