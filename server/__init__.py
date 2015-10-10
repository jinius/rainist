# -*- coding: utf-8 -*-
import server.database as DB
import server.controller.user as User
from flask import Flask, request, render_template, redirect, url_for, session
from flask_oauthlib.client import OAuth, OAuthException

app = Flask(__name__)
app.config.from_object('config')

# DB init
with app.app_context():
	with app.open_resource(app.config['DATABASE_SCHEMA']) as f:
		DB.init(f.read().decode())

@app.teardown_appcontext
def close_db(exception):
	DB.close()

# OAuth init
oauth = OAuth(app)
facebook = oauth.remote_app('facebook',
	base_url = 'https://graph.facebook.com',
	request_token_url = None,
	access_token_url = '/oauth/access_token',
	authorize_url = 'https://www.facebook.com/dialog/oauth',
	consumer_key = app.config['FACEBOOK_APP_ID'],
	consumer_secret = app.config['FACEBOOK_APP_SECRET'],
	request_token_params = {'scope': 'email'}
)

twitter = oauth.remote_app('twitter',
	base_url = 'https://api.twitter.com/1/',
	request_token_url = 'https://api.twitter.com/oauth/request_token',
	access_token_url = 'https://api.twitter.com/oauth/access_token',
	authorize_url = 'https://api.twitter.com/oauth/authenticate',
	consumer_key = app.config['TWITTER_APP_ID'],
	consumer_secret = app.config['TWITTER_APP_SECRET']
)

# TODO: Seprate to module
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		try:
			user = User.login_email(request.form['email'], request.form['password'])
			session['user_id'] = user.get('user_id')
			session['user_name'] = user.get('name')
			return redirect(url_for('.index'))
		except User.Error as e:
			error = str(e)

	return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	if request.method == 'POST':
		name = request.form.get('name')
		email = request.form.get('email')
		password = request.form.get('password')
		try:
			User.register_email(name, email, password)
			user = User.login_email(email, password)
			session['user_id'] = user.get('user_id')
			session['user_name'] = user.get('name')
			return redirect(url_for('.index'))
		except User.Error as e:
			error = str(e)

	return render_template('register.html', error=error)

@app.route('/logout')
def logout():
	session.pop('user_id', None)
	session.pop('user_name', None)
	session.pop('facebook_token', None)
	session.pop('twitter_token', None)
	return redirect(url_for('.index'))

@app.route('/auth/facebook')
def facebook_login():
	return facebook.authorize(callback = app.config['DOMAIN'] + url_for('facebook_callback'))

@app.route('/auth/facebook/callback')
def facebook_callback():
	res = facebook.authorized_response()
	if res is None:
		return redirect(url_for('.index'))
	if isinstance(res, OAuthException):
		return redirect(url_for('.index'))

	session['facebook_token'] = res['access_token']
	me = facebook.get('/me?fields=id,email,name').data
	if me.get('error'):
		return redirect(url_for('.index'))

	try:
		user = User.login_facebook(me.get('id'))
		session['user_id'] = user.get('user_id')
		session['user_name'] = user.get('name')
	except User.UserNotFound:
		name = me.get('name')
		email = me.get('email')
		facebook_id = me.get('id')
		user_id = User.register_facebook(name, email, facebook_id, session.get('user_id'))
		session['user_id'] = user_id
		session['user_name'] = name
	except Exception:
		return redirect(url_for('.index'))

	return redirect(url_for('.index'))

@facebook.tokengetter
def get_facebook_token():
	return (session.get('facebook_token'), '')

@app.route('/auth/twitter')
def twitter_login():
	return twitter.authorize(callback = url_for('twitter_callback'))

@app.route('/auth/twitter/callback')
def twitter_callback():
	res = twitter.authorized_response()
	if res is None:
		return redirect(url_for('.index'))

	session['twitter_token'] = res
	try:
		user = User.login_twitter(res.get('user_id'))
		session['user_id'] = user.get('user_id')
		session['user_name'] = user.get('name')
	except User.UserNotFound:
		name = res.get('screen_name')
		twitter_id = res.get('user_id')
		user_id = User.register_twitter(name, twitter_id, session.get('user_id'))
		session['user_id'] = user_id
		session['user_name'] = name
	except Exception:
		return redirect(url_for('.index'))

	return redirect(url_for('.index'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
	error = None
	name = None
	email = None
	password = False
	message = None
	user_id = session.get('user_id')
	if not user_id:
		return redirect(url_for('.index'))

	try:
		user = User.get_profile(user_id)
		password = True if user.get('pwd_hash') else False
		if request.method == 'POST':
			name = request.form.get('name')
			email = request.form.get('email')
			current_pwd = request.form.get('current_pwd')
			new_pwd = request.form.get('new_pwd')
			new_pwd2 = request.form.get('new_pwd_confirm')

			if current_pwd and new_pwd != new_pwd2:
				error='New passwords do not match'
				return render_template('profile.html', user=user, error=error)

			user = User.set_profile(user, name, email, current_pwd, new_pwd)
			session['user_name'] = user.get('name')
			message = 'Updated your user profile'

		name = user.get('name') if user else None
		email = user.get('email') if user else None
	except User.Error as e:
		error = str(e)

	return render_template('profile.html',
			name=name, email=email, password=password, message=message)

@app.route('/profile/delete')
def delete_user():
	user_id = session.get('user_id')
	if not user_id:
		return redirect(url_for('.index'))

	User.delete_user(user_id)
	return redirect(url_for('.logout'))

