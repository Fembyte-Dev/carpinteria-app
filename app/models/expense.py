from datetime import datetime
from mongoengine import Document, fields

class GeneralExpense(Document):
    CATEGORY_CHOICES = [
        ('Mantenimiento'),
        ('Electricidad'),
        ('Agua'),
        ('Servicios'),
        ('Otros'),
        ('Alquiler'),
        ('Seguro'),
        ('Transporte'),
        ('Impuestos'),
        ('Reparaciones'),
    ]
    category = fields.StringField(choices=CATEGORY_CHOICES, required=True)
    amount = fields.FloatField(required=True)
    date = fields.DateTimeField(default=datetime.utcnow)
    description = fields.StringField()