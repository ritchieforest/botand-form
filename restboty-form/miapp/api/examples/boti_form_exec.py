import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Cargar el modelo
model = tf.keras.models.load_model('ner_model.keras')

# Ejemplo de texto para predecir
text = "Añadir producto Camara Nikon con precio 125."

# Tokenizar el texto
words = text.lower().split()

# Convertir palabras a índices
word2idx = {'camara': 1, 'nikon': 2, 'precio': 3, '125': 4}  # Reemplaza con el vocabulario real usado en el entrenamiento
X = [word2idx.get(word, 0) for word in words]

# Padding
max_len = 50  # Usa el mismo max_len que usaste durante el entrenamiento
X = pad_sequences([X], maxlen=max_len, padding='post')

# Realizar la predicción
predictions = model.predict(X)
predictions = np.argmax(predictions, axis=-1)  # Obtener la clase con la máxima probabilidad

# Convertir índices a etiquetas
label2idx = {'O': 0, 'B-producto': 1, 'I-producto': 2, 'B-precio': 3, 'I-precio': 4}  # Reemplaza con el diccionario real usado en el entrenamiento
idx2label = {idx: label for label, idx in label2idx.items()}

predicted_labels = [idx2label[idx] for idx in predictions[0]]

# Mostrar las palabras con sus etiquetas
result = list(zip(words, predicted_labels))
print(result)
