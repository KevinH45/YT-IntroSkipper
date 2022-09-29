from flask_restful import Resource
from flask import request
from extensions import limiter
from http import HTTPStatus

from firebase import getVideoIntroTime, setVideoIntro
from utils import validateVideo, validateIntro

class VideoResource(Resource):
    decorators = [limiter.limit("1/second", methods=["GET", "POST"])]

    def get(self, vid):

        if not validateVideo(vid):
            return {"msg": "Video ID is not in the right format"}, HTTPStatus.BAD_REQUEST

        record = getVideoIntroTime(vid)

        if record is None:
            # We might use ML or something else to predict the intro time
            # For now, we'll just return an error
            return {"msg": "Video does not exist."}, HTTPStatus.NOT_FOUND

        return {"beforeIntro": record[0], "afterIntro": record[1]}, HTTPStatus.OK


    def post(self, vid):

        data = request.get_json()
        try:
            beforeIntro = int(data["beforeIntro"])
            afterIntro = int(data["afterIntro"])
        except KeyError:
            print("BAD BAD BAD")
            return {"msg": "JSON is formatted wrong"}, HTTPStatus.BAD_REQUEST

        if not validateVideo(vid):
            print("NO NO NO!")
            return {"msg": "Video ID is not in the right format"}, HTTPStatus.BAD_REQUEST

        if not validateIntro(beforeIntro) or not validateIntro(afterIntro):
            print("BRO BRO BRO!")
            return {"msg": "Intro is invalid"}, HTTPStatus.BAD_REQUEST

        status = setVideoIntro(vid, beforeIntro, afterIntro)

        if not status:
            return {"msg": "Error occurred"}, HTTPStatus.INTERNAL_SERVER_ERROR

        return {"msg": "Successfully created"}, HTTPStatus.CREATED



