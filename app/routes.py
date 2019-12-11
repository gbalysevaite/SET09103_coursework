from flask import  render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.models import User, Game
from app.forms import  SignupForm, LoginForm, UpdateForm, NewGameForm, UpdateGameForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            nextPage = request.args.get('next')
            return redirect(nextPage) if nextPage else redirect(url_for('home'))
        else:
            flash("Can't log in with provided credentials. Please check and try again.", 'warning')
    return render_template('login.html', title="Login", form=form), 200

@app.route('/newaccount', methods=['GET', 'POST'])
def newaccount():
    if current_user.is_authenticated:
            return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_pw, 
                phoneNo=form.phoneNo.data, nokName=form.nokName.data, nokNumber=form.nokNumber.data, stripNo=form.stripNo.data)
        db.session.add(user)
        db.session.commit()
        flash('New account created. You can log in now!', 'success')
        return redirect(url_for('login'))
    return render_template('newaccount.html', title="New account", form=form), 200

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    games2 = Game.query.all()
    return render_template('home.html', title="Home", games=games2), 200

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form=UpdateForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.name = form.name.data
        current_user.phoneNo = form.phoneNo.data
        current_user.nokName = form.nokName.data
        current_user.nokNumber = form.nokNumber.data
        current_user.stripNo = form.stripNo.data
        db.session.commit()
        flash('Account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.phoneNo.data = current_user.phoneNo
        form.nokName.data = current_user.nokName
        form.nokNumber.data = current_user.nokNumber
        form.stripNo.data = current_user.stripNo
    return render_template('account.html', title='My account', form=form), 200

@app.route('/games/newgame', methods=['GET', 'POST'])
@login_required
def newgame():
    form=NewGameForm()
    if form.validate_on_submit():
        game = Game(date=form.date.data, location=form.location.data, opposition=form.opposition.data)
        db.session.add(game)
        db.session.commit()
        flash("New game has been added", 'success')
        return redirect(url_for('home'))
    return render_template('newgame.html', title='New game', form=form), 200

@app.route('/game/<int:game_id>')
@login_required
def game(game_id):
    game = Game.query.get_or_404(game_id)
    return render_template('game.html', title=game.opposition, game=game)

@app.route('/game/<int:game_id>/update', methods=['GET', 'POST'])
@login_required
def updateGame(game_id):
    form = UpdateGameForm()
    game = Game.query.get_or_404(game_id)
    if form.validate_on_submit():
        game.date = form.date.data
        game.location = form.location.data
        game.opposition = form.opposition.data
        game.result = form.result.data
        db.session.commit()
        flash('The game has been updated', 'success')
        return redirect(url_for('game', game_id=game.id))
    elif request.method == 'GET':
        form.date.data = game.date
        form.location.data = game.location
        form.opposition.data = game.opposition
        form.result.data = game.result
    return render_template('updateGame.html', title=game.opposition, game=game, form=form)

@app.route('/game/<int:game_id>/delete', methods=['POST'])
@login_required
def deleteGame(game_id):
    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    flash('The game has been deletes', 'success')
    return redirect(url_for('home'))

@app.route('/game/<int:game_id>/attend', methods=['GET', 'POST'])
@login_required
def attend(game_id):
    game = Game.query.get_or_404(game_id)
    game.players.append(current_user)
    db.session.commit()
    flash('You have been added to the game', 'success')
    return redirect(url_for('home'))

@app.route('/game/<int:game_id>/leave', methods=['GET', 'POST'])
@login_required
def leave(game_id):
    game = Game.query.get_or_404(game_id)
    game.players.remove(current_user)
    db.session.commit()
    flash('You have been removed from the game', 'success')
    return redirect(url_for('home'))

