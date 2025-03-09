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
    active = fields.BooleanField(default=True)  # Add this field
    created_at = fields.DateTimeField(default=datetime.now)  # Add timestamp for creation date