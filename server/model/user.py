# -*- coding: utf-8 -*-
"""
	User model
"""
import server.database as DB

def create(name, pwd_hash=None):
	query = 'INSERT INTO user (name, pwd_hash) VALUES (?, ?)'
	DB.execute_query(query, (name, pwd_hash))
	query = 'SELECT last_insert_rowid()'
	return DB.execute_query(query, one=True)[0]

def set_email(user_id, email):
	query = 'INSERT INTO user_email (email, user_id) VALUES (?, ?)'
	DB.execute_query(query, (email, user_id))

def set_facebook(user_id, facebook_id):
	query = 'INSERT INTO user_facebook (user_id, facebook_id) VALUES (?, ?)'
	DB.execute_query(query, (user_id, facebook_id))

def set_twitter(user_id, twitter_id):
	query = 'INSERT INTO user_twitter (user_id, twitter_id) VALUES (?, ?)'
	DB.execute_query(query, (user_id, twitter_id))

def find_email(email):
	query = 'SELECT user_id, name, email, pwd_hash FROM user NATURAL JOIN user_email WHERE email=?'
	result = DB.execute_query(query, (email,), one=True)
	return dict(zip(('user_id', 'name', 'email', 'pwd_hash'), result)) if result else None

def find_facebook(facebook_id):
	query = 'SELECT user_id, name, facebook_id FROM user NATURAL JOIN user_facebook WHERE facebook_id=?'
	result = DB.execute_query(query, (facebook_id,), one=True)
	return dict(zip(('user_id', 'name', 'facebook_id'), result)) if result else None

def find_twitter(twitter_id):
	query = 'SELECT user_id, name, twitter_id FROM user NATURAL JOIN user_twitter WHERE twitter_id=?'
	result = DB.execute_query(query, (twitter_id,), one=True)
	return dict(zip(('user_id', 'name', 'twitter_id'), result)) if result else None

def get_profile(user_id):
	query = 'SELECT user_id, name, email, pwd_hash FROM user NATURAL LEFT JOIN user_email WHERE user_id=?'
	result = DB.execute_query(query, (user_id,), one=True)
	return dict(zip(('user_id', 'name', 'email', 'pwd_hash'), result)) if result else None

def update_name(user_id, name):
	query = 'UPDATE user SET name=? WHERE user_id=?'
	DB.execute_query(query, (name, user_id))

def update_email(user_id, email):
	if email:
		query = 'INSERT OR REPLACE INTO user_email (email, user_id) VALUES (?, ?)'
		DB.execute_query(query, (email, user_id))
	else:
		query = 'DELETE FROM user_email WHERE user_id=?'
		DB.execute_query(query, (user_id,))

def update_password(user_id, pwd_hash):
	query = 'UPDATE user SET pwd_hash=? WHERE user_id=?'
	DB.execute_query(query, (pwd_hash, user_id))

def delete_user(user_id):
	query = 'DELETE FROM user_email WHERE user_id=?'
	DB.execute_query(query, (user_id,))
	query = 'DELETE FROM user_facebook WHERE user_id=?'
	DB.execute_query(query, (user_id,))
	query = 'DELETE FROM user_twitter WHERE user_id=?'
	DB.execute_query(query, (user_id,))
