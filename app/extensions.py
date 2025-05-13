from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize extensions
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

# MongoDB connection
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
mongo_db = mongo_client.get_default_database()