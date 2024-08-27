import logging
from flask import Flask
from flask_pymongo import PyMongo
from .routes import init_routes

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://mongo:27017/trivia_db"
    
    # Initialize MongoDB
    mongo = PyMongo(app)

    # Set up logging
    setup_logging(app)

    # Register routes
    init_routes(app, mongo)

    return app

def setup_logging(app):
    # Set up the logger
    handler = logging.FileHandler('app.log')  # Log to a file named 'app.log'
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(message)s'
    )
    handler.setFormatter(formatter)
    
    # Add the file handler to the app logger
    app.logger.addHandler(handler)
    
    # Set log level (INFO, DEBUG, WARNING, ERROR, CRITICAL)
    app.logger.setLevel(logging.INFO)
    
    # Also log to the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)
