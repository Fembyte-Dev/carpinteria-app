# Importaciones necesarias para la aplicación Flask
from flask import Flask  # Framework principal para crear la aplicación web
from mongoengine import connect  # Extensión para integrar Flask con MongoDB
from flask_login import LoginManager  # Extensión para manejar la autenticación de usuarios
from config import Config  # Archivo de configuración externo
from bson import ObjectId  # Clase para manejar IDs de documentos en MongoDB

# Crea la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Función factory para crear y configurar la aplicación Flask
def create_app():
    # Importa los Blueprints desde los módulos correspondientes
    # Los Blueprints permiten organizar las rutas de manera modular
    from .routes.auth import auth_bp  # Rutas relacionadas con autenticación
    from .routes.clients import clients_bp  # Rutas relacionadas con clientes
    from .routes.projects import projects_bp  # Rutas relacionadas con proyectos
    from .routes.expenses import expenses_bp  # Rutas relacionadas con gastos
    from .routes.reports import reports_bp  # Rutas relacionadas con reportes

    # Crea una nueva instancia de la aplicación Flask
    app = Flask(__name__)
    # Carga la configuración desde el archivo Config
    app.config.from_object(Config)
    # Conexión a MongoDB usando mongoengine
    connect(
        db=app.config['MONGODB_NAME'],
        host=app.config['MONGO_URI']
    )


    # Inicializa las extensiones necesarias
    login_manager.init_app(app)  # Inicializa Flask-Login
    login_manager.login_view = 'auth.login'  # Ruta para redirigir si no está autenticado

    # Registra los Blueprints en la aplicación
    app.register_blueprint(auth_bp)  # Autenticación
    app.register_blueprint(clients_bp)  # Clientes
    app.register_blueprint(projects_bp)  # Proyectos
    app.register_blueprint(expenses_bp)  # Gastos
    app.register_blueprint(reports_bp)  # Reportes

    return app  # Retorna la aplicación configurada


# Cargador de usuarios para Flask-Login
# Esta función se utiliza para cargar un usuario desde la base de datos
from app.models.user import User
@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()



if __name__ == '__main__':
    create_app()
    app.run(debug=True)