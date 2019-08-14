import os

from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))



class Config(object):
	
	PROJECT ='app'
	DEBUG= False
	SECRET_KEY ='THIS IS DEFAULT SECRET KEY'

class DevelopmentConfig(Config):

	DEBUG=True
	SECRET_KEY='THIS IS DEVELOPMENT SECRET KEY'
	SQLALCHEMY_ECHO =True
	SQLALCHEMY_DATABASE_URI ='mysql+pymysql://root:welcome@123@localhost:3306/arhamcollection_demo'
	
	MAIL_SERVER='arhamcollections.com'
	MAIL_PORT =465
	MAIL_USERNAME='registration@arhamcollections.com'
	MAIL_PASSWORD ='welcome@123'
	MAIL_USE_TLS=False
	MAIL_USE_SSL =True

	UPLOAD_FOLDER='/home/sarfaraz/flaskenv/arhamcollections/images'
	ALLOWED_EXTENSIONS =set(['jpg','png','gif','jpeg'])

class ProductionConfig(Config):
	
	DEBUG=False
	SQL_ALCHEMY_DATABASE_URI ='mysql://root:welcome@123@localhost:3306/arhamcollection_demo'


app_config={
	'development':DevelopmentConfig,
	'production':ProductionConfig
}

def get_config(MODE):
	SWITCH ={
	'LOCAL':DevelopmentConfig,
	'PRODUCTION':ProductionConfig
	}
	return SWITCH(MODE)


