from flask import Blueprint, current_app, render_template
from flask_login import current_user, login_required

from app.email.email import Email
from app.email.email_forms import SendEmailForm

bp = Blueprint("email", __name__, url_prefix="/email")


@bp.route("/contact", methods=["POST", "GET"])
@login_required
def contact():
    form = SendEmailForm()
    if form.validate_on_submit():
        html = "<p>" + form.body.data + "</p>"
        Email.send_email(
            subject="Message from: " + current_user.email,
            sender=current_app.config["MAIL_USERNAME"],
            recipients=[current_app.config["MAIL_USERNAME"]],
            text_body=form.body.data,
            html_body=html,
        )
        return render_template("contact.html", title="Contact admins", success=True)
    return render_template("contact.html", title="Contact admins", form=form)
