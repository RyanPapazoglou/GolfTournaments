from flask import request, Blueprint, render_template, flash, redirect

from app.auth.auth_forms import LoginForm

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/login", methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.email.data, form.remember_me.data))
        return redirect('/app/index')
    return render_template('login.html', title='Sign In', form=form)
