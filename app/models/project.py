from datetime import datetime
from mongoengine import Document, EmbeddedDocument, fields
from app.models.client import Client

class Advance(EmbeddedDocument):
    amount = fields.FloatField()
    date = fields.DateTimeField()

class Cost(EmbeddedDocument):
    amount = fields.FloatField()
    description = fields.StringField()
    date = fields.DateTimeField()

class Project(Document):
    client_id = fields.ReferenceField(Client, required=True)
    name = fields.StringField(required=True)
    description = fields.StringField()
    start_date = fields.DateTimeField()
    estimated_end_date = fields.DateTimeField()
    actual_end_date = fields.DateTimeField()
    status = fields.StringField(choices=['in_progress', 'completed', 'cancelled'], default='in_progress')
    budget = fields.FloatField()
    advances = fields.EmbeddedDocumentListField(Advance)
    costs = fields.EmbeddedDocumentListField(Cost)