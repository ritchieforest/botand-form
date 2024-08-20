# api/models.py

from mongoengine import Document, EmbeddedDocument,connect,ReferenceField
from mongoengine.fields import StringField, IntField, ListField, EmbeddedDocumentField

# Conectar a MongoDB
connect(
        db='boti-form',
        username='root',
        password='password',
        host='localhost',
        port=27017,
        authentication_source='admin'
    )
class Context(Document):
    nombre = StringField(required=True, unique=True)
    descripcion = StringField()
    def __str__(self):
        return self.nombre

class SchemeByContext(Document):
    descripcion = StringField()
    contexto = ReferenceField(Context, required=True)
    def __str__(self):
        return self.descripcion

class Label(Document):
    nombre = StringField(required=True)
    descripcion = StringField()
    contexto = ReferenceField(Context, required=True)

    def __str__(self):
        return f'{self.nombre} - {self.contexto.nombre}'

class LabelTrain(EmbeddedDocument):
    start=IntField(required=True)
    end=IntField(required=True)
    label=StringField(required=True)
    position_array=ListField(IntField(),default=list)

class TrainData(Document):
    context=StringField(required=True)
    text=StringField(required=True)
    labels=ListField(EmbeddedDocumentField(LabelTrain),default=list)



