from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import db, bcrypt
from app.forms import RegistrationForm, LoginForm, VoteForm
from app.models import User, Candidate, Vote
from flask_login import login_user, current_user, logout_user, login_required

bp = Blueprint('routes', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    candidates = Candidate.query.all()
    return render_template('index.html', candidates=candidates)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('routes.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

@bp.route('/candidate/<int:candidate_id>', methods=['GET', 'POST'])
def candidate(candidate_id):
    candidate = Candidate.query.get_or_404(candidate_id)
    form = VoteForm()
    if form.validate_on_submit():
        vote = Vote(adjective=form.adjective.data, voter=current_user, candidate=candidate)
        db.session.add(vote)
        db.session.commit()
        flash(f'You voted for {candidate.name} as {form.adjective.data}!', 'success')
        return redirect(url_for('routes.candidate', candidate_id=candidate_id))
    votes = Vote.query.filter_by(candidate_id=candidate.id).all()
    return render_template('candidate.html', title=candidate.name, candidate=candidate, form=form, votes=votes)
