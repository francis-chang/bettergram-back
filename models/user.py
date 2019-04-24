import os
from db import db
from requests import Response
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import request, url_for

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    activated = db.Column(db.Boolean, nullable=False, default=False)

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.filter_by(id=_id).first()

    def send_confirmation_email(self) -> Response:
        link = "http://www.google.com"
        #     request.url_root[:-1] + url_for(
        #     "confirmation"
        # )

        message = Mail(
            from_email='fc373745@gmail.com',
            to_emails= self.email,
            subject='Please verify your registration with Bettergram',
            html_content='<html>Please click the link to confirm your registration: <a href={link}>link</a></html>')
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            sg.send(message)
        except Exception as e:
            print(e.message)

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
