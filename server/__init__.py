# -*- coding: utf-8 -*-
import server.database as DB
import server.controller.auth as Auth
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
app.config.from_object('config')

with app.open_resource(app.config['DATABASE_SCHEMA']) as f:
	DB.init(f.read().decode())

# TODO: Seprate to module
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None

	if request.method == 'POST':
		try:
			Auth.login(request.form['email'], request.form['password'])
			return redirect(url_for('.index'))
		except Auth.Error as e:
			error = str(e)

	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	Auth.logout()
	return redirect(url_for('.index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	if request.method == 'POST':
		try:
			Auth.register(request.form['name'], request.form['email'], request.form['password'])
			return redirect(url_for('.index'))
		except Auth.Error as e:
			error = str(e)

	return render_template('register.html', error=error)
