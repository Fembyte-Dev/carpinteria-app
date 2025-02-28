from flask import Flask
from flask_pymongo import PyMongo
from config import Config  # Importa la configuración
from app import *



app = create_app()

if __name__ == '__main__':
    app.run(debug=True)