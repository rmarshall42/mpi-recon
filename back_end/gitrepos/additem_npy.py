import numpy as np
import sqlite3
import glob
import pickle

import os

FOLDER='./all_pkl/*.pkl'

conn = sqlite3.connect('CC.db')
c = conn.cursor()
c.execute(""" CREATE TABLE CC (
	filename TEXT(256) NOT NULL,
	call_name TEXT(256) NOT NULL,
	line INT
	)""") 

for filename in glob.iglob(FOLDER):
	with open(filename, 'rb') as f:
		store = pickle.load(f)
		#store = store.tolist()
		for key, value in store.items():
			print(key)
			for v in value:
				c.execute("INSERT INTO CC VALUES (?,?,?)", (sqlite3.Binary(key), sqlite3.Binary(v[0]), int(v[1])))


conn.commit()
conn.close()

