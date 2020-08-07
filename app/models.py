import uuid
from time import time
import jwt
from sqlalchemy import String, ForeignKey, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from app import login
from flask import current_app


@login.user_loader
def load_user(id):
    return Users.query.get(id)


class Users(UserMixin, db.Model):
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
    points = db.Column(Integer)
    golfers = db.relationship("UsersGolfers", back_populates="user")

    def __init__(self, first_name, last_name, email, password, team_name, points):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.team_name = team_name
        self.points = points

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "team_name": self.team_name,
            "points": self.points,
        }

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": str(self.id), "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )["reset_password"]
        except:
            return
        return Users.query.get(id)


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
    odds = db.Column(Integer)
    odds_ratio = db.Column(String())
    current_standing = db.Column(Integer)
    current_points = db.Column(Integer)
    picture_url = db.Column(String())
    updated_at = db.Column(DateTime())
    users = db.relationship("UsersGolfers", back_populates="golfer")

    def __init__(
        self,
        first_name,
        last_name,
        world_rank,
        odds,
        odd_ratio,
        current_standing,
        picture_url,
        updated_at,
        current_points,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.world_rank = world_rank
        self.odds = odds
        self.odds_ratio = odd_ratio
        self.current_standing = current_standing
        self.picture_url = picture_url
        self.current_points = current_points
        self.updated_at = updated_at

    def to_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "world_rank": self.world_rank,
            "odds": self.odds,
            "odds_ratio": self.odds_ratio,
            "current_standing": self.current_standing,
            "updated_at": str(self.updated_at),
            "picture_url": self.picture_url,
            "current_points": self.current_points,
        }


class UsersGolfers(db.Model):
    __tablename__ = "users_golfers"

    golfer_id = db.Column(
        UUID(as_uuid=True), ForeignKey("golfers.id"), primary_key=True,
    )
    user_id = db.Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    golfer = db.relationship(
        Golfers,
        back_populates="users",
        order_by="desc(Golfers.odds),desc(Golfers.world_rank)",
    )
    user = db.relationship(Users, back_populates="golfers")

    def __init__(self, golfer_id, user_id):
        self.golfer_id = golfer_id
        self.user_id = user_id
