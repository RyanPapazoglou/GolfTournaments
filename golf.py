import click
from app import create_app, db
from app.models import Golfers, UsersGolfers, Users
from app.golfers.golfers import GolfersGenerator
from app.profile.profiles import Profiles


app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Users=Users, Golfers=Golfers, UsersGolfers=UsersGolfers, GolfersGenerator=GolfersGenerator, Profiles=Profiles)

@app.cli.command("populate")
def populate():
    GolfersGenerator.read_golfer_data()

@app.cli.command("reset-standings")
def reset_standing():
    GolfersGenerator.reset_standings()

@app.cli.command("calculate-points")
def calculate_points():
    Profiles.calculate_points()

@app.cli.command("reset-points")
def reset_points():
    Profiles.reset_points()