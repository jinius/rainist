# -*- coding: utf-8 -*-
"""
	User authentication
"""
import server.model.user as User
from flask import session
from werkzeug import generate_password_hash, check_password_hash

class Error(Exception):
	def __str__(self):
		return 'Error'

class UserNotFound(Error):
	def __str__(self):
		return 'User not found'

class WrongPassword(Error):
	def __str__(self):
		return 'Password is incorrect'

class ExistingUser(Error):
	def __str__(self):
		return 'User already exists'

def login_email(email, password):
	user = User.find_email(email)
	if not user:
		raise UserNotFound()
	if not check_password_hash(user.get('pwd_hash') or '', password):
		raise WrongPassword()
	return user

def login_facebook(facebook_id):
	user = User.find_facebook(facebook_id)
	if not user:
		raise UserNotFound()
	return user

def login_twitter(twitter_id):
	user = User.find_twitter(twitter_id)
	if not user:
		raise UserNotFound()
	return user

def register_email(name, email, password=None):
	pwd_hash = generate_password_hash(password) if password else None
	user = User.find_email(email)
	if user:
		raise ExistingUser()

	user_id = User.create(name, pwd_hash)

	User.set_email(user_id, email)

	return user_id

def register_facebook(name, email, facebook_id, user_id=None):
	user = User.find_facebook(facebook_id)
	if user:
		raise ExistingUser()

	if not user_id:	# if not logged in
		user = User.find_email(email) # find user by email
		if user:
			user_id = user.get('user_id')
		else:
			user_id = User.create(name)
			User.set_email(user_id, email)

	User.set_facebook(user_id, facebook_id)
	return user_id

def register_twitter(name, twitter_id, user_id=None):
	user = User.find_twitter(twitter_id)
	if user:
		raise ExistingUser()

	if not user_id:
		user_id = User.create(name)

	User.set_twitter(user_id, twitter_id)
	return user_id

def get_profile(user_id):
	return User.get_profile(user_id)

def set_profile(user, name, email, current_pwd, new_pwd):
	print(current_pwd, new_pwd)
	if current_pwd:
		if not check_password_hash(user.get('pwd_hash') or '', current_pwd):
			raise WrongPassword()
		pwd_hash = generate_password_hash(new_pwd) if password else None
		User.update_password(user_id, pwd_hash)

	user_id = user.get('user_id')

	if user.get('name') != name:
		user['name'] = name
		User.update_name(user_id, name)

	if user.get('email') != email:
		user['email'] = email
		User.update_email(user_id, email)

	return user

def delete_user(user_id):
	User.delete_user(user_id)

