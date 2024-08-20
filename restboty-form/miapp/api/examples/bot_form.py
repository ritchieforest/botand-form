import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.utils import class_weight
from models import TrainData
# Preparar datos

class TrainTransformData2:
    def __init__(self):
        self._data = None
        self._word2idx=None
        self._max_len=None
        self._label2idx=None
        self._name_model="ner_model.keras"
        self._max_len=None
        self._X=None
        self._Y=None
        self._model=None
        self._load_data()
    def _load_data(self):
        todos_los_registros = TrainData.objects.all()
        # Consultar todos los registros
        # Convertir los registros a una lista de diccionarios
        registros_dict = [registro.to_mongo().to_dict() for registro in todos_los_registros]
        self._data=registros_dict
    def _load_model(self):
        self.initializate_config()
        self._model = tf.keras.models.load_model('ner_model.keras')
    def initializate_config(self):
        texts, word_labels = self.preprocess_data()
        # Crear vocabulario y codificar etiquetas
        word_set = {word for sentence in texts for word in sentence}
        label_set = {label for labels in word_labels for label in labels}

        self._word2idx = {word: idx + 1 for idx, word in enumerate(word_set)}
        self._label2idx = {label: idx for idx, label in enumerate(label_set)}
        X, y = self.convert_to_indices(texts, word_labels)
        # Padding
        max_len = max(len(sentence) for sentence in X)
        self._X = pad_sequences(X, maxlen=max_len, padding='post')
        self._Y = pad_sequences(y, maxlen=max_len, padding='post')
        # Configuración del modelo
        input_dim = len(self._word2idx) + 1
        output_dim = len(self._label2idx)

        self._model = tf.keras.Sequential([
            tf.keras.layers.Embedding(input_dim=input_dim, output_dim=64, input_length=max_len),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
            tf.keras.layers.Dense(output_dim, activation='softmax')
        ])

    def saveModel(self):
        try:
            self.initializate_config()
            self._Y = np.expand_dims(self._Y, -1)  # Añadir dimensión para la etiqueta
            self._model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
            # Entrenamiento del modelo
            self._model.fit(self._X, self._Y, epochs=10, batch_size=1, validation_split=0.1)
            # Guardar el modelo
            self._model.save('ner_model.keras')
        except Exception as err:
            print(str(err))
            pass
    
    def predict(self):
        self._load_model()
        # Uso del modelo para hacer predicciones en un nuevo texto
        new_text = "Me gustaria añadir un producto AFINADOR CROMATICO PINZA MCT6 MAGMA de categoria MAGMA, que tenga el precio 5909.3 y el proveedor sea ALEYMAR, con un stock 383, con un codigo de proveedor 20 y el codigo interno para el producto 120500 para la marca MAGMA"
        new_words = new_text.lower().replace(",","").split()

        # Convertir a índices
        new_X = [[self._word2idx.get(word, 0) for word in new_words]]
        new_X = pad_sequences(new_X, maxlen=self._max_len, padding='post')

        # Predecir etiquetas
        predictions = self._model.predict(new_X)
        predicted_labels = np.argmax(predictions, axis=-1)[0]
        print(self._label2idx.keys())
        # Convertir índices de etiquetas a nombres
        predicted_labels = [list(self._label2idx.keys())[idx] for idx in predicted_labels if idx != 0]

        # Extraer entidades
        entities = self.extract_entities(new_words, predicted_labels)
        print("##############################################")
        #print(predictions)
        print("##############################################")
        print(predicted_labels)
        print("##############################################")
        print(entities)
        print("##############################################")
        print(new_words)

        # Salida esperada: {"PRODUCTO": "Camara Nikon", "PRECIO": "125"}


    #Probar alineacion de etiquetas con los datos
    def aligment_labels_text(self):
        texts, word_labels = self.preprocess_data(self._data)
        for text, labels in zip(texts, word_labels):
            print(f"Texto: {' '.join(text)}")
            print(f"Texto: {text}")
            print(f"Etiquetas: {labels}")
            break
    # Función de preprocesamiento
    def preprocess_data(self):
        texts = []
        word_labels = []

        for item in self._data:
            text = item["text"].lower().replace(",","")
            text_labels = item["labels"]

            # Tokenizamos el texto en palabras
            words = text.split()
            word_labels_current = ["O"] * len(words)

            # Asignamos etiquetas a las palabras
            for label in text_labels:
                position_array = label["position_array"]
                label_type = label["label"].replace(" ", "_").lower()  # Reemplazamos espacios por guiones bajos
                # Recorrer cada palabra para ver si se superpone con el rango de la etiqueta
                
                        #end_word_index=i
                # Si la palabra está en el rango de la etiqueta, asignar la etiqueta
                if len(position_array)>0:
                    word_labels_current[position_array[0]] = f"B-{label_type}"                
                    if position_array[1]>1:
                        for i in range(0,position_array[1]):
                            indice=position_array[0]+i
                            if i!=0:
                                word_labels_current[indice] = f"I-{label_type}"            
            texts.append(words)
            word_labels.append(word_labels_current)
        return texts, word_labels
    # Convertir datos a índices
    def convert_to_indices(self,texts, word_labels):
        X = [[self._word2idx.get(word, 0) for word in sentence] for sentence in texts]
        y = [[self._label2idx.get(label, -1) for label in labels] for labels in word_labels]
        return X, y
    # Función para extraer entidades
    def extract_entities(self,words, labels):
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

class TrainTransformData:
    def __init__(self):
        self._data = None
        self._word2idx = None
        self._max_len = None
        self._label2idx = None
        self._model = None
        self._X = None
        self._Y = None
        self._name_model = "ner_model.keras"
        self._initialize()

    def _initialize(self):
        self._load_data()
        self.initializate_config()

    def _load_data(self):
        todos_los_registros = TrainData.objects.all()
        registros_dict = [registro.to_mongo().to_dict() for registro in todos_los_registros]
        self._data = registros_dict

    def _load_model(self):
        if self._model is None:
            self._model = tf.keras.models.load_model(self._name_model)

    def initializate_config(self):
        texts, word_labels = self.preprocess_data()
        word_set = {word for sentence in texts for word in sentence}
        label_set = {label for labels in word_labels for label in labels}

        self._word2idx = {word: idx + 1 for idx, word in enumerate(word_set)}
        self._label2idx = {label: idx for idx, label in enumerate(label_set)}

        X, y = self.convert_to_indices(texts, word_labels)
        self._max_len = max(len(sentence) for sentence in X)

        self._X = pad_sequences(X, maxlen=self._max_len, padding='post')
        self._Y = pad_sequences(y, maxlen=self._max_len, padding='post')

        if self._model is None:
            input_dim = len(self._word2idx) + 1
            output_dim = len(self._label2idx)

            self._model = tf.keras.Sequential([
                tf.keras.layers.Embedding(input_dim=input_dim, output_dim=128, input_length=self._max_len),
                tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
                tf.keras.layers.Dropout(0.5),
                tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(len(self._label2idx), activation='softmax'))
            ])

    def save_model(self):
        try:
            if self._model is None:
                self.initializate_config()

            self._Y = np.expand_dims(self._Y, -1)
            classes = np.unique(self._Y.flatten())
            class_weights = class_weight.compute_class_weight('balanced', classes=classes, y=self._Y.flatten())
            class_weights_dict = dict(enumerate(class_weights))

            self._model.compile(optimizer='adam', 
                                loss='sparse_categorical_crossentropy', 
                                metrics=['accuracy']
                                )
            #self._model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
            # Entrenar el modelo con class_weight
            self._model.fit(
                self._X, 
                self._Y, 
                epochs=10, 
                batch_size=1, 
                validation_split=0.1,
                #class_weight=class_weights_dict  # Añadir los pesos de clase aquí
            )
            self._model.save(self._name_model)
        except Exception as err:
            print(f"Error al guardar el modelo: {str(err)}")

    def predict(self, text):
        self._load_model()

        new_words = text.lower().replace(",", "").split()
        new_X = [[self._word2idx.get(word, 0) for word in new_words]]
        new_X = pad_sequences(new_X, maxlen=self._max_len, padding='post')

        predictions = self._model.predict(new_X)
        predicted_labels = np.argmax(predictions, axis=-1)[0]
        predicted_labels = [list(self._label2idx.keys())[idx] for idx in predicted_labels if idx != 0]

        entities = self.extract_entities(new_words, predicted_labels)
        print(entities)
        return entities

    def preprocess_data(self):
        texts = []
        word_labels = []

        for item in self._data:
            text = item["text"].lower().replace(",", "")
            text_labels = item["labels"]

            words = text.split()
            word_labels_current = ["O"] * len(words)

            for label in text_labels:
                position_array = label["position_array"]
                label_type = label["label"].replace(" ", "_").lower()
                if len(position_array) > 0:
                    word_labels_current[position_array[0]] = f"B-{label_type}"
                    for i in range(1, position_array[1]):
                        indice = position_array[0] + i
                        word_labels_current[indice] = f"I-{label_type}"

            texts.append(words)
            word_labels.append(word_labels_current)

        return texts, word_labels

    def convert_to_indices(self, texts, word_labels):
        X = [[self._word2idx.get(word, 0) for word in sentence] for sentence in texts]
        y = [[self._label2idx.get(label, -1) for label in labels] for labels in word_labels]
        return X, y
    def analyze_specific_prediction(self, text):
        self._load_model()
        words = text.lower().replace(",", "").split()
        new_X = [[self._word2idx.get(word, 0) for word in words]]
        new_X = pad_sequences(new_X, maxlen=self._max_len, padding='post')
        predictions = self._model.predict(new_X)
        predicted_labels = np.argmax(predictions, axis=-1)[0]
        predicted_labels = [list(self._label2idx.keys())[idx] for idx in predicted_labels if idx != 0]
        entities = self.extract_entities(words, predicted_labels)

        print(f"Texto: {text}")
        print(f"Palabras: {words}")
        print(f"Etiquetas Predichas: {predicted_labels}")
        print(f"Entidades Extraídas: {entities}")
    def compare_predictions(self):
        texts, word_labels = self.preprocess_data()
        for i, (text, true_labels) in enumerate(zip(texts, word_labels)):
            if i > 10:  # Limitar a los primeros 10 ejemplos para facilitar la depuración
                break
            
            # Convertir texto a índices y hacer predicción
            text_indices = [self._word2idx.get(word, 0) for word in text]
            padded_text_indices = pad_sequences([text_indices], maxlen=self._max_len, padding='post')
            predictions = self._model.predict(padded_text_indices)
            predicted_labels = np.argmax(predictions, axis=-1)[0]
            predicted_labels = [list(self._label2idx.keys())[idx] for idx in predicted_labels if idx != 0]
            
            print(f"Texto: {' '.join(text)}")
            print(f"Etiquetas Reales: {true_labels}")
            print(f"Etiquetas Predichas: {predicted_labels}")
            print(f"{'-'*40}")
    def error_analysis(self):
        errors = []
        texts, word_labels = self.preprocess_data()
        
        for i, (text, true_labels) in enumerate(zip(texts, word_labels)):
            # Convertir texto a índices y hacer predicción
            text_indices = [self._word2idx.get(word, 0) for word in text]
            padded_text_indices = pad_sequences([text_indices], maxlen=self._max_len, padding='post')
            predictions = self._model.predict(padded_text_indices)
            predicted_labels = np.argmax(predictions, axis=-1)[0]
            predicted_labels = [list(self._label2idx.keys())[idx] for idx in predicted_labels if idx != 0]
            
            if predicted_labels != true_labels:
                errors.append({
                    "text": ' '.join(text),
                    "true_labels": true_labels,
                    "predicted_labels": predicted_labels
                })
        
        # Guardar o imprimir errores para análisis
        for error in errors:
            print(f"Texto: {error['text']}")
            print(f"Etiquetas Reales: {error['true_labels']}")
            print(f"Etiquetas Predichas: {error['predicted_labels']}")
            print(f"{'-'*40}")
    def extract_entities(self, words, labels):
        entities = {}
        entity_name = None
        entity_type = None

        for word, label in zip(words, labels):
            if label.startswith("B-"):
                if entity_name:
                    entities[entity_type.replace("_", " ")] = entity_name.strip()
                entity_name = word
                entity_type = label[2:]
            elif label.startswith("I-") and entity_type == label[2:]:
                entity_name += f" {word}"
            else:
                if entity_name:
                    entities[entity_type.replace("_", " ")] = entity_name.strip()
                    entity_name = None
                    entity_type = None

        if entity_name:
            entities[entity_type.replace("_", " ")] = entity_name.strip()

        return entities
class TrainTransformData3:
    def __init__(self):
        self._data = None
        self._word2idx = None
        self._max_len = None
        self._label2idx = None
        self._name_model = "ner_model.keras"
        self._X = None
        self._Y = None
        self._model = None
        self._load_data()

    def _load_data(self):
        todos_los_registros = TrainData.objects.all()
        registros_dict = [registro.to_mongo().to_dict() for registro in todos_los_registros]
        self._data = registros_dict

    def _load_model(self):
        self.initializate_config()
        self._model = tf.keras.models.load_model(self._name_model)

    def initializate_config(self):
        # Preprocesamiento con segmentación
        texts, word_labels = self.preprocess_data(segmentar=True)
        
        # Crear vocabulario y codificar etiquetas
        word_set = {word for sentence in texts for word in sentence}
        label_set = {label for labels in word_labels for label in labels}

        self._word2idx = {word: idx + 1 for idx, word in enumerate(word_set)}
        self._label2idx = {label: idx for idx, label in enumerate(label_set)}
        
        # Convertir a índices y padding
        X, y = self.convert_to_indices(texts, word_labels)
        max_len = max(len(sentence) for sentence in X)
        self._X = pad_sequences(X, maxlen=max_len, padding='post')
        self._Y = pad_sequences(y, maxlen=max_len, padding='post')

        # Configuración del modelo
        input_dim = len(self._word2idx) + 1
        output_dim = len(self._label2idx)

        self._model = tf.keras.Sequential([
            tf.keras.layers.Embedding(input_dim=input_dim, output_dim=64, input_length=max_len),
            tf.keras.layers.Conv1D(64, 5, activation='relu'),  # Capa Convolucional
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
            tf.keras.layers.Dense(output_dim, activation='softmax')
        ])

    def saveModel(self):
        try:
            self.initializate_config()
            self._Y = np.expand_dims(self._Y, -1)
            self._model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
            
            # Calcular class_weights
            classes = np.unique(self._Y.flatten())
            class_weights = class_weight.compute_class_weight('balanced', classes=classes, y=self._Y.flatten())
            class_weights_dict = dict(enumerate(class_weights))

            # Entrenamiento del modelo con class_weights
            self._model.fit(self._X, self._Y, epochs=10, batch_size=16, validation_split=0.1, class_weight=class_weights_dict)

            # Guardar el modelo
            self._model.save(self._name_model)
        except Exception as err:
            print(str(err))
            pass

    def preprocess_data(self, segmentar=False):
        texts = []
        word_labels = []

        for item in self._data:
            text = item["text"].lower().replace(",", "")
            text_labels = item["labels"]

            # Segmentación del texto
            if segmentar:
                # Aquí segmentas el texto en frases más pequeñas
                segments = self.segment_text(text)
            else:
                segments = [text]

            for segment in segments:
                words = segment.split()
                word_labels_current = ["O"] * len(words)

                for label in text_labels:
                    position_array = label["position_array"]
                    label_type = label["label"].replace(" ", "_").lower()
                    
                    if len(position_array) > 0:
                        word_labels_current[position_array[0]] = f"B-{label_type}"                
                        if position_array[1] > 1:
                            for i in range(1, position_array[1]):
                                indice = position_array[0] + i
                                if indice < len(word_labels_current):
                                    word_labels_current[indice] = f"I-{label_type}"

                texts.append(words)
                word_labels.append(word_labels_current)

        return texts, word_labels

    def segment_text(self, text):
        # Segmentación simple basada en palabras clave
        segments = text.split(". ")  # Divide el texto en oraciones
        return segments

    def convert_to_indices(self, texts, word_labels):
        X = [[self._word2idx.get(word, 0) for word in sentence] for sentence in texts]
        y = [[self._label2idx.get(label, 0) for label in labels] for labels in word_labels]
        return X, y
 
# obj=TrainTransformData()
# #obj.save_model()
# text="Me gustaria añadir un producto AFINADOR CROMATICO PINZA MCT6 de categoria MAGMA, que tenga el precio 5909.3 y el proveedor sea ALEYMAR, con un stock 383, con un codigo de proveedor 20 y el codigo interno para el producto 120500 para la marca MAGMA"
# obj.predict(text=text)
# # obj.analyze_specific_prediction(text=text)
# # obj.error_analysis()