from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import firebase_admin

from config import Config
from extensions import limiter

from resources.video import VideoResource

def register_extensions(app):

    cred = firebase_admin.credentials.Certificate("introskipper-45df4-firebase-adminsdk-5l8o7-34c2238832.json")
    firebaseApp = firebase_admin.initialize_app(cred, {
        'databaseURL': "https://introskipper-45df4-default-rtdb.firebaseio.com/"
    })

    limiter.init_app(app)
    CORS(app)

def create_app():
    app = Flask("aE5tSQPC51AFDUzOE3U3t5Ddz")
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    return app

def register_resources(app):
    api = Api(app)

    api.add_resource(VideoResource, "/api/videos/<vid>")

if __name__ == '__main__':
    app = create_app()
    app.run()


