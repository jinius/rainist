# -*- coding: utf-8 -*-
from flask import Flask, request, session, render_template, redirect, url_for

app = Flask(__name__)
# TODO: config setting
# app.config.from_object(config.py)
app.secret_key = 'test secrect key'

# TODO: Connect to database

# TODO: Populate DB with sample data

# TODO: Seprate to module
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		""" Auth.login """
		if request.form['password'] == '1234':
			session['user_id'] = request.form['email']
			redirect(url_for('.index'))
		else:
			error = 'password not match'

	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session.pop('user_id', None)
	return redirect(url_for('.index'))

@app.route('/register')
def register():
	return render_template('register.html')
