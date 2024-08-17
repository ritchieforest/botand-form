import json
import requests

file="C:/Users/rvillalba/Desktop/Ricardo V/botand-form/restboty-form/miapp/api/data_initial/articulos.json"


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
        print(f"Error en la petición, código de estado: {response.status_code}")

# Abre y lee el archivo JSON
with open(file, 'r', encoding='utf-8') as file:
    data = json.load(file)

schemasByContest=loadDataRequest("http://127.0.0.1:8000/api/esquema-por-contexto/")
etiquetas=loadDataRequest("http://127.0.0.1:8000/api/etiquetas/")
listDataCreate=[]
for aux in schemasByContest:
    descripcion=aux["descripcion"]
    listDataCreate.append({
        "contexto":aux["contexto"],
        "text":"",
        "labels":[]
    })
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
        descripcion = "Descripción del artículo: {0}, Marca: {1}, Precio: {2}, Proveedor: {3}, Código: {4}, Código Proveedor: {5}, Marca: {6}"
        auxDes = descripcion.format(NOMARTICULO, MARCA, PCOMPRA, PROVE, CODIGO, 20, CODPROVE, MARCA_FIJO)

        # Asigna la descripción formateada al primer elemento de la lista
        listDataCreate[0]["text"] = auxDes

        # Función auxiliar para encontrar y manejar índices
        def safe_index(phrase, substring):
            try:
                return phrase.index(substring)
            except ValueError:
                return -1  # Devuelve -1 si no se encuentra el substring

        # Lista de etiquetas y su configuración correspondiente
        labels_config = [
            ("{0", NOMARTICULO, "PRODUCTO"),
            ("{1", MARCA, "Cateogoria"),
            ("{2", PCOMPRA, "Precio"),
            ("{3", PROVE, "Proveedor"),
            ("{4", CODIGO, "CODIGO INTERNO"),
            ("{5", CODPROVE, "CODPROVE"),
            ("{6", MARCA_FIJO, "MARCA")
        ]

        # Agrega las etiquetas a la lista
        for placeholder, value, label in labels_config:
            start_index = safe_index(auxDes, placeholder)
            if start_index != -1:
                listDataCreate[0]["labels"].append({
                    "end": start_index + 2 + len(value),
                    "start": start_index + 1,
                    "label": label
                })
        print(listDataCreate)

#print(schemasByContest)

#print(schemasByContest)