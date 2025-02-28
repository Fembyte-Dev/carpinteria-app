from datetime import datetime
from mongoengine import Document, fields
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin  # Importa UserMixin para simplificar la implementación

class User(Document, UserMixin):  # Hereda de UserMixin
    username = fields.StringField(required=True, unique=True)
    email = fields.EmailField(required=True, unique=True)
    password_hash = fields.StringField(required=True)
    is_admin = fields.BooleanField(default=False)
    active = fields.BooleanField(default=True)
    created_at = fields.DateTimeField(default=datetime.utcnow)

    def set_password(self, password):
        """
        Genera un hash de la contraseña proporcionada y lo almacena en el campo password_hash.
        :param password: Contraseña en texto plano.
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Verifica si la contraseña proporcionada coincide con el hash almacenado.
        :param password: Contraseña en texto plano.
        :return: True si la contraseña es correcta, False en caso contrario.
        """
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_user_by_email(cls, email):
        """
        Busca un usuario por su dirección de correo electrónico.
        :param email: Dirección de correo electrónico del usuario.
        :return: Instancia del usuario encontrado o None si no existe.
        """
        return cls.objects(email=email).first()

    @property
    def is_active(self):
        """
        Flask-Login requiere este atributo para verificar si la cuenta está activa.
        """
        return self.active

    def get_id(self):
        """
        Flask-Login requiere este método para obtener el ID único del usuario.
        """
        return str(self.id)  # Asegúrate de que el ID sea una cadena