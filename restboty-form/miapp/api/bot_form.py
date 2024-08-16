from transformers import BertTokenizer, BertForTokenClassification, Trainer, TrainingArguments
from datasets import load_dataset, load_metric

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForTokenClassification.from_pretrained("bert-base-uncased", num_labels=3)

# Preparar datos
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples['text'], truncation=True, padding=True, is_split_into_words=True)
    labels = []
    for i, label in enumerate(examples['labels']):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        label_ids = [-100 if word_id is None else label[word_id] for word_id in word_ids]
        labels.append(label_ids)
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

# Cargar y preparar el dataset
dataset = load_dataset("json", data_files={"train": "data.json"})
tokenized_datasets = dataset.map(tokenize_and_align_labels, batched=True)

# Entrenamiento
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
)

trainer.train()
model.save_pretrained("model_transformers_contexto")


from transformers import BertTokenizer, BertForTokenClassification

tokenizer = BertTokenizer.from_pretrained("model_transformers_contexto")
model = BertForTokenClassification.from_pretrained("model_transformers_contexto")

inputs = tokenizer("En el campo descripción de producto guárdame Camara Nikon precio 125 del proveedor MJ-Music", return_tensors="pt")
outputs = model(**inputs)
predictions = outputs.logits.argmax(-1)

# Procesar y mapear predicciones a entidades


import speech_recognition as sr
import spacy
import json

# Cargar el modelo NLP entrenado
nlp = spacy.load("model_entidades_contexto")

# Configurar el reconocimiento de voz
recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Habla ahora...")
    audio = recognizer.listen(source)
    text = recognizer.recognize_google(audio)

print("Texto reconocido:", text)

# Procesar el texto
doc = nlp(text)
data = {"PRODUCTO": None, "PRECIO": None, "PROVEEDOR": None}

for ent in doc.ents:
    if ent.label_ in data:
        data[ent.label_] = ent.text

# Convertir a JSON
json_data = json.dumps(data, indent=4)
print("Datos en JSON:", json_data)



###########################################################
from transformers import BertTokenizer, BertForTokenClassification, Trainer, TrainingArguments
from datasets import load_dataset

# Preparar datos
dataset = load_dataset("json", data_files={"train": "data_multiclase.json"})
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertForTokenClassification.from_pretrained("bert-base-uncased", num_labels=5)  # Ajustar num_labels

# Tokenización
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples['text'], truncation=True, padding=True)
    labels = [[-100] * len(tokenized_inputs['input_ids'][i]) for i in range(len(examples['labels']))]
    for i, label in enumerate(examples['labels']):
        for j, word_id in enumerate(tokenized_inputs.word_ids(batch_index=i)):
            if word_id is not None:
                labels[i][j] = label[word_id]
    tokenized_inputs["labels"] = labels
    return tokenized_inputs

# Datos tokenizados
tokenized_datasets = dataset.map(tokenize_and_align_labels, batched=True)

# Entrenamiento
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
)

trainer.train()
model.save_pretrained("model_transformers_multiclase")
##############################Clasificacion por contexto previo
{
  "context": "producto",
  "text": "Añadir Camara Nikon con precio 125.",
  "labels": [
    {"start": 12, "end": 26, "label": "PRODUCTO"},
    {"start": 33, "end": 36, "label": "PRECIO"}
  ]
}
