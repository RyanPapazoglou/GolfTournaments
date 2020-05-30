import uuid
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app import db


class Users(db.Model):
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

    def __init__(self, first_name, last_name, world_rank, odds, picture_url):
        self.first_name = first_name
        self.last_name = last_name
        self.world_rank = world_rank
        self.odds = odds
        self.picture_url = picture_url