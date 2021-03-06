import click
from apscheduler.schedulers.background import BackgroundScheduler
from app import create_app, db
from app.auth.auth_dao import AuthDao
from app.models import Golfers, UsersGolfers, Users
from app.golfers.golfers import GolfersGenerator
from app.profile.profiles import Profiles
from app.scraper.scheduler.jobs.scraper_job import ScraperJob

app = create_app()
app.logger.info("Created app")
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=ScraperJob.scrape, trigger="interval", hours=1, coalesce=True,
)
try:
    app.logger.info("Scheduler running: " + str(scheduler.running))
    if not scheduler.running:
        scheduler.start()
        app.logger.info("Scheduler running: " + str(scheduler.running))
        jobs = scheduler.get_jobs()
        if jobs:
            app.logger.info("Scheduler jobs: " + str(jobs))
            for job in jobs:
                app.logger.info(
                    "Job: "
                    + str(job.name)
                    + "("
                    + str(job.func)
                    + ")"
                    + " will run next at: "
                    + str(job.next_run_time)
                    + " on trigger: "
                    + str(job.trigger)
                )
except KeyboardInterrupt as e:
    app.logger.info("Job failed, keyboard interrupt")
    scheduler.shutdown()
except SystemExit as e:
    app.logger.info("Job failed, system exit")
    scheduler.shutdown()


@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app,
        db=db,
        Users=Users,
        Golfers=Golfers,
        UsersGolfers=UsersGolfers,
        GolfersGenerator=GolfersGenerator,
        Profiles=Profiles,
        Scraper=ScraperJob,
        AuthDao=AuthDao,
    )


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


@app.cli.command("reset-pw")
@click.argument("team")
@click.argument("password")
def reset_pw(team, password):
    AuthDao.update_password(team, password)
