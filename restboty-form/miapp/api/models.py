# api/models.py

from mongoengine import Document, EmbeddedDocument,connect,ReferenceField
from mongoengine.fields import StringField,  EmbeddedDocumentField,ListField

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
class LabelByContext(Document):
    nombre = StringField(required=True)
    descripcion = StringField()
    contexto = ReferenceField(Context, required=True)

    def __str__(self):
        return f'{self.nombre}'
    
class LabelsRefs(EmbeddedDocument):
    refString=StringField()
    labelByContext_id=ReferenceField(LabelByContext)

class SchemeByContext(Document):
    descripcion = StringField()
    contexto = ReferenceField(Context, required=True)
    labels=ListField(EmbeddedDocumentField(LabelsRefs),default=list)
    def __str__(self):
        return self.descripcion


 
 
# {
#     "descripcion": "Me gustaria añadir un producto {0} de categoria {1}, que tenga el precio {2} y el proveedor sea {3}, con un stock {4}, con un codigo de proveedor {5} y el codigo interno para el producto {6} para la marca {7}",
#     "contexto": "66bfff2f8fdcc6e0fa23713b",
#     "labels": [
#         {
#             "refString": "{0}",
#             "labelByContext_id": "66c48e0b5b0bf637f28a5f6a"
#         },
#         {
#             "refString": "{1}",
#             "labelByContext_id": "66c48e1d5b0bf637f28a5f6b"
#         },
#         {
#             "refString": "{2}",
#             "labelByContext_id": "66c48e3c5b0bf637f28a5f6c"
#         },
#         {
#             "refString": "{3}",
#             "labelByContext_id": "66c4c760391ddd257becb343"
#         },
#         {
#             "refString": "{4}",
#             "labelByContext_id": "66c48e5d5b0bf637f28a5f6d"
#         },
#         {
#             "refString": "{5}",
#             "labelByContext_id": "66c48e705b0bf637f28a5f6e"
#         },
#         {
#             "refString": "{6}",
#             "labelByContext_id": "66c48eef5b0bf637f28a5f6f"
#         },
#         {
#             "refString": "{7}",
#             "labelByContext_id": "66c48f015b0bf637f28a5f70"
#         }
#     ]
# }


