from flask import Blueprint, render_template, url_for, redirect, flash, request
from ..extensions import db

import os

from ..user_management.models import Userroles



from  arhamcollection_app.main_app.models import test


image_path="/".join([os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), "images"])

main_app = Blueprint('main_app', __name__, url_prefix="/", static_folder='./static', static_url_path="main_app/static", template_folder='./templates')

@main_app.route('/',methods=['GET','POST'])
def home():
	data = test.query.all()
	print(data)
	# image_path=image_path+'parallax.jpg'+'parallax.jpg'
	img=image_path+'/parallax.jpg'
	return render_template('main_app/index.html',data=data,image_path=img)




@main_app.route("dropall")
def dropall():
    db.drop_all()
    return "all tables dropped"


@main_app.route("createroles")
def createroles():
    userroles = Userroles(role="Admin")
    db.session.add(userroles)
    db.session.commit()
    userroles = Userroles(role="User")
    db.session.add(userroles)
    db.session.commit()
    return "added all roles"
