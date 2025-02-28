import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/carpinteria_db')
    MONGODB_NAME = 'carpinteria_db'
    SECRET_KEY = os.getenv('SECRET_KEY', 'clave_secreta_por_defecto')
