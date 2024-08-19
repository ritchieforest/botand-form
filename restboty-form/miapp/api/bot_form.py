import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from models import TrainData
from datasets import load_dataset
# Preparar datos
todos_los_registros = TrainData.objects.all()
# Consultar todos los registros

# Convertir los registros a una lista de diccionarios
registros_dict = [registro.to_mongo().to_dict() for registro in todos_los_registros]

# # Convertir la lista de diccionarios a JSON
# registros_json = json.dumps(registros_dict, default=str)  # default=str para manejar tipos de datos no serializables

# with open('./data_initial/registros.json', 'w',encoding='utf-8',errors="ignore") as archivo:
#     archivo.write(registros_json)
 

# Datos de ejemplo
#data = load_dataset("json", data_files={"train": "./data_initial/registros.json"})
data=registros_dict

# Datos de entrenamiento
# data = [
#     {
#         "text": "Añadir producto Camara Nikon con precio 125.",
#         "labels": [
#             {"start": 15, "end": 27, "label": "PRODUCTO"},
#             {"start": 37, "end": 40, "label": "PRECIO"}
#         ]
#     },
#     {
#         "text": "Añadir producto Camara sssNikon con precio 125.",
#         "labels": [
#             {"start": 15, "end": 30, "label": "PRODUCTO"},
#             {"start": 37, "end": 40, "label": "PRECIO"}
#         ]
#     },
#     {
#         "text": "Añadir producto Camara Nikonssss con precio 125.",
#         "labels": [
#             {"start": 15, "end": 30, "label": "PRODUCTO"},
#             {"start": 37, "end": 40, "label": "PRECIO"}
#         ]
#     },
# ]

# Función de preprocesamiento
def preprocess_data(data):
    texts = []
    word_labels = []

    for item in data:
        text = item["text"].lower()
        text_labels = item["labels"]

        # Tokenizamos el texto en palabras
        words = text.split()
        word_labels_current = ["O"] * len(words)

        # Asignamos etiquetas a las palabras
        for label in text_labels:
            label_start = label["start"]
            label_end = label["end"]
            label_type = label["label"].replace(" ", "_").lower()  # Reemplazamos espacios por guiones bajos
            auxword=""
            list_indice=[]
            # Recorrer cada palabra para ver si se superpone con el rango de la etiqueta
            for i, word in enumerate(words):
                word_start = text.find(word)
                word_end = word_start + len(word)
                auxword=auxword+" "+word
                total=len(auxword)
                if total==label_start:
                    list_indice.append(i)
                elif label_start<total<=label_end:
                    if i not in list_indice:
                        list_indice.append(i)
                elif total>label_end:                    
                    break
                    #end_word_index=i
            # Si la palabra está en el rango de la etiqueta, asignar la etiqueta
            
            if len(list_indice)>0:
                print(list_indice)
                word_labels_current[list_indice[0]] = f"B-{label_type}"                
                for i,indice in enumerate(list_indice):
                    if i!=0:
                        word_labels_current[indice] = f"I-{label_type}"
                list_indice=[]                
        texts.append(words)
        word_labels.append(word_labels_current)
    return texts, word_labels
def aligment_labels_text():
    global data
    texts, word_labels = preprocess_data(data)
    for text, labels in zip(texts, word_labels):
        print(f"Texto: {' '.join(text)}")
        print(f"Texto: {text}")
        print(f"Etiquetas: {labels}")
        break
# Preprocesamiento de los datos de entrenamiento

texts, word_labels = preprocess_data(data)
# Crear vocabulario y codificar etiquetas
word_set = {word for sentence in texts for word in sentence}
label_set = {label for labels in word_labels for label in labels}

word2idx = {word: idx + 1 for idx, word in enumerate(word_set)}
label2idx = {label: idx for idx, label in enumerate(label_set)}

# Convertir datos a índices
def convert_to_indices(texts, word_labels, word2idx, label2idx):
    X = [[word2idx.get(word, 0) for word in sentence] for sentence in texts]
    y = [[label2idx.get(label, -1) for label in labels] for labels in word_labels]
    return X, y

X, y = convert_to_indices(texts, word_labels, word2idx, label2idx)

# Padding
max_len = max(len(sentence) for sentence in X)
X = pad_sequences(X, maxlen=max_len, padding='post')
y = pad_sequences(y, maxlen=max_len, padding='post')

# Configuración del modelo
input_dim = len(word2idx) + 1
output_dim = len(label2idx)

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=input_dim, output_dim=64, input_length=max_len),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
    tf.keras.layers.Dense(output_dim, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Entrenamiento del modelo
y = np.expand_dims(y, -1)  # Añadir dimensión para la etiqueta
model.fit(X, y, epochs=30, batch_size=1, validation_split=0.1)

# Guardar el modelo
model.save('ner_model.keras')

# Función para extraer entidades
def extract_entities(words, labels):
    entities = {}
    entity_name = None
    entity_type = None
    for word, label in zip(words, labels):
        if label.startswith("B-"):
            if entity_name is not None:
                entities[entity_type.replace("_", " ")] = entity_name.strip()
            entity_name = word
            entity_type = label[2:]
        elif label.startswith("I-") and entity_type == label[2:]:
            entity_name += " " + word
        else:
            if entity_name is not None:
                entities[entity_type.replace("_", " ")] = entity_name.strip()
                entity_name = None
                entity_type = None
    if entity_name is not None:
        entities[entity_type.replace("_", " ")] = entity_name.strip()
    return entities


# Uso del modelo para hacer predicciones en un nuevo texto
new_text = "Me gustaria añadir un producto AFINADOR CROMATICO PINZA MCT6 MAGMA de categoria MAGMA, que tenga el precio 5909.3 y el proveedor sea ALEYMAR, con un stock 383, con un codigo de proveedor 20 y el codigo interno para el producto 120500 para la marca MAGMA"
new_words = new_text.split()

# Convertir a índices
new_X = [[word2idx.get(word, 0) for word in new_words]]
new_X = pad_sequences(new_X, maxlen=max_len, padding='post')

# Predecir etiquetas
predictions = model.predict(new_X)
predicted_labels = np.argmax(predictions, axis=-1)[0]

# Convertir índices de etiquetas a nombres
predicted_labels = [list(label2idx.keys())[idx] for idx in predicted_labels if idx != 0]

# Extraer entidades
entities = extract_entities(new_words, predicted_labels)
print(entities)
# Salida esperada: {"PRODUCTO": "Camara Nikon", "PRECIO": "125"}
