from ..extensions import db

import datetime


class test(db.Model):
	__tablename__='test'

	id =db.Column(db.Integer,primary_key=True, autoincrement=True)
	name=db.Column(db.String(100), nullable=False)



class test2(db.Model):
	__tablename__='test2'

	id =db.Column(db.Integer,primary_key=True, autoincrement=True)
	name=db.Column(db.String(100), nullable=False)	