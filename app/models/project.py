from datetime import datetime
import re
from mongoengine import Document, EmbeddedDocument, fields
from app.models.client import Client

class Advance(EmbeddedDocument):
    id = fields.ObjectIdField()
    concept = fields.StringField(required=True)
    amount = fields.FloatField(required=True)
    date = fields.DateTimeField(required=True)

class Cost(EmbeddedDocument):
    id = fields.ObjectIdField()
    amount = fields.FloatField(required=True)
    description = fields.StringField(required=True)
    date = fields.DateTimeField(required=True)

class Project(Document):
    client = fields.ReferenceField(Client, required=True)
    name = fields.StringField(required=True)
    description = fields.StringField()
    start_date = fields.DateTimeField(required=True)
    end_date = fields.DateTimeField(required=True)
    estimated_cost = fields.FloatField(required=True)
    status = fields.StringField(choices=['pending', 'in_progress', 'completed', 'cancelled'], default='pending')
    budget = fields.FloatField()
    advances = fields.EmbeddedDocumentListField(Advance)
    costs = fields.EmbeddedDocumentListField(Cost)
    active = fields.BooleanField(default=True)  
    created_at = fields.DateTimeField(default=datetime.now)  