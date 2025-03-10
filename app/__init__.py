# Importaciones necesarias para la aplicación Flask
from flask import Flask  # Framework principal para crear la aplicación web
from mongoengine import connect  # Extensión para integrar Flask con MongoDB
from flask_login import LoginManager  # Extensión para manejar la autenticación de usuarios
from config import Config  # Archivo de configuración externo
from bson import ObjectId  # Clase para manejar IDs de documentos en MongoDB

# Crea la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# Función factory para crear y configurar la aplicación Flask
def create_app():
    # Inicializa el administrador de login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Conexión a MongoDB usando mongoengine
    connect(
        db=app.config['MONGODB_NAME'],
        host=app.config['MONGO_URI']
    )


    from app.models.user import User
    from .routes.auth import auth_bp  # Rutas relacionadas con autenticación
    from .routes.clients import clients_bp  # Rutas relacionadas con clientes
    from .routes.projects import projects_bp  # Rutas relacionadas con proyectos
    from .routes.expenses import expenses_bp  # Rutas relacionadas con gastos
    from .routes.reports import reports_bp  # Rutas relacionadas con reportes
    from .routes.dashboard import dashboard_bp  # Rutas relacionadas con el panel de control

    # Registra los Blueprints en la aplicación
    app.register_blueprint(auth_bp)  # Autenticación
    app.register_blueprint(clients_bp)  # Clientes
    app.register_blueprint(projects_bp)  # Proyectos
    app.register_blueprint(expenses_bp)  # Gastos
    app.register_blueprint(reports_bp)  # Reportes
    app.register_blueprint(dashboard_bp)  # Panel de control

    # Cargador de usuarios para Flask-Login
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.objects(id=ObjectId(user_id)).first()

    return app  # Retorna la aplicación configurada


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)