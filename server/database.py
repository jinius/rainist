# -*- coding: utf-8 -*-
"""
	DB API using sqlite3
"""
import sqlite3
from flask import g

def get_connection():
	conn = getattr(g, 'db_connection', None)
	if conn is None:
		g.db_connection = conn = sqlite3.connect('rainist.db')
	return conn

def init(schema):
	get_connection().cursor().executescript(schema)
	get_connection().commit()

def execute_query(query, args=(), one=False):
	cur = get_connection().execute(query, args)
	result = cur.fetchall()	# for SELECT query
	get_connection().commit()	# for INSERT query
	return result if not one else (result[0] if result else None)

def close():
	conn = getattr(g, 'db_connection', None)
	if conn is not None:
		conn.close()
