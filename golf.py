import click
from app import create_app, db
from app.models import Golfers, UsersGolfers, Users
from app.golfers.golfers import GolfersGenerator


app = create_app()

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Users=Users, Golfers=Golfers, UsersGolfers=UsersGolfers, GolfersGenerator=GolfersGenerator)

@app.cli.command("populate")
def populate():
    GolfersGenerator.read_golfer_data()