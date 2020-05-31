import uuid
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from app import db
from werkzeug.security import check_password_hash
from flask_login import UserMixin

from app import login

@login.user_loader
def load_user(id):
    return Users.query.get(id)

class Users(UserMixin,db.Model):
    __tablename__ = "users"
    id: UUID = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    first_name = db.Column(String())
    last_name = db.Column(String())
    email = db.Column(String())
    password = db.Column(String())
    team_name = db.Column(String())
    golfers = db.relationship("Golfers", backref="user_id", lazy='dynamic')

    def __init__(self, first_name, last_name, email, password, team_name):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.team_name = team_name

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Golfers(db.Model):
    __tablename__ = "golfers"
    id: UUID = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    first_name = db.Column(String())
    last_name = db.Column(String())
    world_rank = db.Column(String())
    odds = db.Column(String())
    picture_url = db.Column(String())
    user = db.Column(UUID, db.ForeignKey('users.id'))

    def __init__(self, first_name, last_name, world_rank, odds, picture_url):
        self.first_name = first_name
        self.last_name = last_name
        self.world_rank = world_rank
        self.odds = odds
        self.picture_url = picture_url

    def to_json(self):
        return {
            "first_name":self.first_name,
            "last_name":self.last_name,
            "world_rank":self.world_rank,
            "odds":self.odds,
            "picture_url":self.picture_url
        }