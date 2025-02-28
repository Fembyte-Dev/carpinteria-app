from datetime import datetime
from mongoengine import Document, fields
from werkzeug.security import generate_password_hash, check_password_hash

class User(Document):
    username = fields.StringField(required=True, unique=True)
    email = fields.EmailField(required=True, unique=True)
    password_hash = fields.StringField(required=True)
    is_admin = fields.BooleanField(default=False)
    active = fields.BooleanField(default=True)
    created_at = fields.DateTimeField(default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        print("se asede a verify password")
        """
        Verifica si la contraseña proporcionada coincide con el hash almacenado.
        :param password: Contraseña en texto plano.
        :return: True si la contraseña es correcta, False en caso contrario.
        """
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_user_by_email(cls, email):
        print("revisando usuario")
        return cls.objects(email=email).first()
    
    @property
    def is_active(self):
        """
        Flask-Login requiere este atributo para verificar si la cuenta está activa.
        """
        return self.active
    
    def get_id(self):
        return str(self.id)