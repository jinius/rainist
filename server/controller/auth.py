# -*- coding: utf-8 -*-
"""
	Authentication
"""
import server.model.user as User
from flask import session, redirect, url_for
from werkzeug import generate_password_hash, check_password_hash

class Error(Exception):
	def __str__(self):
		return 'Unknown Error'

class UserNotFound(Error):
	def __str__(self):
		return 'User not found'

class WrongPassword(Error):
	def __str__(self):
		return 'Wrong Password'

class ExistingUser(Error):
	def __str__(self):
		return 'User already exists'

def login(email, password):
	try:
		user = User.find(email)
	except Exception:
		raise Error()

	if not user:
		raise UserNotFound()

	if check_password_hash(user.get('pwd_hash', ''), password):
		session['user_id'] = user.get('email', None)
		session['user_name'] = user.get('name', None)
	else:
		raise WrongPassword()

def logout():
	session.pop('user_id', None)
	session.pop('user_name', None)

def register(name, email, password):
	pwd_hash = generate_password_hash(password)
	try:
		User.create(name, email, pwd_hash)
	except Exception:
		raise ExistingUser()
	login(email, password)

