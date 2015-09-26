# -*- coding: utf-8 -*-
from flask import Flask, session, render_template, redirect, url_for

app = Flask(__name__)
# TODO: config setting
# app.config.from_object(config.py)

# TODO: Connect to database

# TODO: Populate DB with sample data

# TODO: Seprate to module
@app.route('/')
def index():
	return render_template('index.html');

@app.route('/login')
def login():
	return render_template('login.html');

@app.route('/logout')
def logout():
	return redirect(url_for('.index'));

@app.route('/register')
def register():
	return render_template('register.html');
