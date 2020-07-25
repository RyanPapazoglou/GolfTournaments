from apscheduler.schedulers.background import BackgroundScheduler
from app import create_app, db
from app.models import Golfers, UsersGolfers, Users
from app.golfers.golfers import GolfersGenerator
from app.profile.profiles import Profiles
from app.scraper.scheduler.jobs.scraper_job import ScraperJob

app = create_app()
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=ScraperJob.scrape,
    trigger="interval",
    hours=1,
    coalesce=True,
)
try:
    scheduler.start()
except KeyboardInterrupt as e:
    scheduler.shutdown()
except SystemExit as e:
    scheduler.shutdown()

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Users=Users, Golfers=Golfers, UsersGolfers=UsersGolfers, GolfersGenerator=GolfersGenerator, Profiles=Profiles, Scraper=ScraperJob)

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

@app.cli.command("scrape")
def scrape_esp():
    ScraperJob.scrape()