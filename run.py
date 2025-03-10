from flask import Flask
from flask_pymongo import PyMongo
from config import Config  # Importa la configuración
from app import *



app = create_app()
print(app.url_map)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')