# -*- coding: utf-8 -*-
"""
	User model
"""
import server.database as DB

def create(name, email, pwd_hash):
#	print('INSERT user:', 'email:', email, 'name:', name, 'pwd_hash:', pwd_hash)
	query = 'INSERT INTO user_local (email, name, pwd_hash) VALUES (?, ?, ?)'
	DB.execute_query(query, (email, name, pwd_hash))

# TODO: Test login success
# TODO: Test login failed(no email) - should return None, should not throw error
def find(email):
	query = 'SELECT user_id, email, name, pwd_hash FROM user_local WHERE email=?'
	result = DB.execute_query(query, (email,), one=True)
#	print('SELECT result:', result)
	return dict(zip(('user_id', 'email', 'name', 'pwd_hash'), result)) if result else None

