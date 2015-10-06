# -*- coding: utf-8 -*-
"""
	DB API using sqlite3
"""
import sqlite3

def init(schema):
	db = sqlite3.connect('./rainist.db')
	db.cursor().executescript(schema)
	db.commit()
	db.close()

def execute_query(query, args=(), one=False):
	db = sqlite3.connect('./rainist.db')
	cur = db.execute(query, args)
	result = cur.fetchall()
	db.commit()
	cur.close()
	db.close()
	return result if not one else (result[0] if result else None)
