# api/models.py

from mongoengine import Document, StringField, ReferenceField, connect

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

class Label(Document):
    nombre = StringField(required=True)
    descripcion = StringField()
    contexto = ReferenceField(Context, required=True)

    def __str__(self):
        return f'{self.nombre} - {self.contexto.nombre}'
