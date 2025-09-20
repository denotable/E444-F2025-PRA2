from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

EMAIL_ALLOWED_DOMAINS = {"mail.utoronto.ca", "utoronto.ca", "eecg.toronto.edu", "eecg.utoronto.ca", "ece.utoronto.ca"}

def _domain_of(email: str) -> str:
    return email.strip().lower().rsplit("@", 1)[-1]

def _is_allowed(domain: str) -> bool:
    return domain in EMAIL_ALLOWED_DOMAINS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap5(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT email address?', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!', 'warning')
        
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!', 'warning')
        
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    
    email_message = None
    saved_email = session.get('email')
    if saved_email:
        domain = _domain_of(saved_email)
        if _is_allowed(domain):
            email_message = f"Your UofT email is {saved_email}"
        else:
            allowed_str = ", ".join(sorted(EMAIL_ALLOWED_DOMAINS))
            email_message = f"Please use your UofT email."
    
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'), email_message=email_message)

