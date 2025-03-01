from datetime import datetime
from mongoengine import Document, EmbeddedDocument, fields

class Contact(EmbeddedDocument):
    phone_mobile = fields.StringField()
    phone_landline = fields.StringField()
    email = fields.EmailField()

class Address(EmbeddedDocument):
    street = fields.StringField()
    city = fields.StringField()
    state = fields.StringField()
    zip = fields.StringField()

class FiscalData(EmbeddedDocument):
    rfc = fields.StringField()
    fiscal_name = fields.StringField()
    regimen = fields.StringField()
    fiscal_zip = fields.StringField()
    requires_invoice = fields.BooleanField(default=False)

class Notes(EmbeddedDocument):
    preferences = fields.StringField()
    observations = fields.StringField()

class Client(Document):
    first_name = fields.StringField(required=True)
    last_name = fields.StringField(required=True)
    second_last_name = fields.StringField()
    contact = fields.EmbeddedDocumentField(Contact)
    address = fields.EmbeddedDocumentField(Address)
    fiscal_data = fields.EmbeddedDocumentField(FiscalData)
    notes = fields.EmbeddedDocumentField(Notes)
    active = fields.BooleanField(default=True)
    created_at = fields.DateTimeField(default=datetime.utcnow)