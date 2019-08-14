from flask import Blueprint, render_template, url_for, redirect, flash, request,jsonify
from ..extensions import db
from .models import (
                    User, Userroles, Userrolesmapping, Userprofile, Useraddress
                    )

from .forms import SignupForm,LoginForm,ChangePasswordForm,ProfileForm,AddAddressForm

from ..extensions import db, login_manager
from flask_login import login_user, login_required,logout_user,current_user

from werkzeug.security import check_password_hash, generate_password_hash

from sqlalchemy import exc, and_, or_

import random
import hashlib

import datetime
from datetime import timedelta



user_management = Blueprint('user_management', __name__, url_prefix="/", static_folder='./static', static_url_path="main_app/static", template_folder='./templates')

@user_management.route('signup',methods=["POST","GET"])
def signup():
    form =SignupForm()
    if request.method=="POST":
        if form.validate():
            x = request.form.to_dict()
            email = x['email']
            password = x['password']
            confirm_password = x['confirm_password']
            if password != confirm_password:
                return jsonify(error="ERROR! Passwords not matching.")
            # return render_template('user_management/signup.html', form=form)
            else:
                try:
                    salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:10]
                    password_hash = generate_password_hash(password + salt, 'sha256')
                    data = User(email=email, password=password_hash, email_salt=salt)
                    db.session.add(data)
                    db.session.commit()

                    userrole = Userroles.query.filter_by(role='User').first()
                    user_role_mapping = Userrolesmapping(user_id=data.id, role_id=userrole.role_id)
                    db.session.add(user_role_mapping)
                    db.session.commit()

                    userprofile = Userprofile(user_id=data.id)
                    db.session.add(userprofile)
                    db.session.commit()

                    # send_confirmation_email(email)
                    return jsonify(success='Please check you email')
                except exc.IntegrityError:
                    db.session.rollback()
                    error = 'ERROR! Email ({}) already exists.'.format(email)
                    return jsonify(error=error)
        else:
            return jsonify(fielderror=form.errors)
                # return render_template('user_management/signup.html', form=form)
    return render_template('user_management/signup.html', form=form)


@user_management.route("login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            x = request.form.to_dict()
            user = User.query.filter_by(email=x['email']).first()
            if user:
                if check_password_hash(user.password, x['password'] + user.email_salt):
                    login_user(user)
                    # identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
                    return jsonify(success='logged in', redirect='/')
                else:
                    return jsonify(error='Incorrect password')
            else:
                return jsonify(error='Username not registered')
        else:
            return jsonify(fielderror=form.errors)
    else:
        return render_template('user_management/loginpage.html', form=form)

@user_management.route("forgotpassword", methods=['GET', 'POST'])
def forgotpassword():
    form = ForgotPasswordForm()
    if request.method=="POST":
        if form.validate():
            x=request.form.to_dict()
            email=x['email']
            user = User.query.filter_by(email=email).first()
            print(user)
            if user:
                send_password_reset_email(email)
                return jsonify(success="Password reset email sent, Please check your inbox")
            else:
                print(email)
                error="Your email {} not registered with us. Please signup with us".format('email')
                # flash("email not registered with us")
                return jsonify(error=error)
        else:
            return jsonify(fielderror=form.errors)
    return render_template('user_management/forgotpassword.html', form=form)     

@login_required
@user_management.route("logout")
def logout():
    logout_user()
    return redirect(url_for('main_app.home'))

@user_management.route("changepassword", methods=['GET', 'POST'])
@login_required
def changepassword():
    form = ChangePasswordForm()
    user = User.query.filter_by(id=current_user.id).first()
    if request.method=='POST' :
        if form.validate():
            x=request.form.to_dict()
            if check_password_hash(user.password, x['current_password'] + user.email_salt):
                if x['new_password'] ==x['confirm_password']:
                    password_hash = generate_password_hash(x['new_password'] + user.email_salt, 'sha256')
                    user.password = password_hash
                    db.session.add(user)
                    db.session.commit()
                    return jsonify(success='Password Changed Successfully')
                else:
                    return jsonify(error='New Password is not matching with Confirm Password')
            else:
                return jsonify(error='Inccorrect password')
        else:
            return jsonify(fielderror=form.errors)
    return render_template('user_management/changepassword.html', form=form)

@user_management.route("edituserprofile", methods=['GET', 'POST'])
@login_required
def edituserprofile():
    form = ProfileForm()
    if request.method == 'POST':
        print('FORM IS POSTED BY POST')
        if form.validate():
            x = request.form.to_dict()
            try:
                data=Userprofile.query.filter_by(user_id=current_user.id).first()
                data.first_name=x['first_name'] 
                data.last_name=x['last_name']
                data.dateofbirth=x['dateofbirth']
                data.mobile_number=x['mobile_number']
                data.gender=x['gender']
                db.session.add(data)
                db.session.commit()
                return jsonify(success='Updated your profile successfully')
            except:
                db.session.rollback()
                return jsonify(error='Error while updating')
        else:
            return jsonify(fielderror=form.errors)    
    else:
        try:
            userprofile = Userprofile.query.filter_by(user_id=current_user.id).first()
            form = ProfileForm(obj=userprofile)
            form.populate_obj(userprofile)
            return render_template('user_management/edituserprofile.html', form=form)
        except: 
            return jsonify(error='Unable to find profilie')
    return render_template('user_management/edituserprofile.html', form=form)


@user_management.route("addresslist", methods=['GET'])
@login_required
def addresslist():
    useraddress = Useraddress.query.filter(Useraddress.user_id == current_user.id).filter(Useraddress.delete_flag == 0).all()
    return render_template('user_management/addresslist.html', useraddress=useraddress)




@user_management.route('addaddress', methods=['GET', 'POST'])
@user_management.route("addaddress/<int:address_id>", methods=['GET', 'POST'])
@login_required
def addaddress(address_id=None):
    # x=1/0
    form = AddAddressForm()
    if request.method=='POST':
        if form.validate():
            x=request.form.to_dict()
            try:
                x['default_flag']
                x['default_flag']=True

            except:
                x['default_flag']=False

            if address_id==None:
                try:
                    data = Useraddress(first_name=x['first_name'], last_name=x['last_name'], address1=x['address1'], address2=x['address2'], landmark=x['landmark'], state=x['state'], city=x['city'], pincode=x['pincode'], mobileno=x['mobileno'], default_flag=x['default_flag'],user_id=current_user.id)
                    db.session.add(data)
                    db.session.commit()
                    if  x['default_flag']==True:
                        try:
                            defaultadddata=Useraddress.query.filter(Useraddress.user_id==current_user.id).filter(Useraddress.address_id.address_id !=data.address_id).filter(Useraddress.default_flag==True).first()
                            defaultadddata.default_flag=False
                            db.session.commit()
                        except:
                            db.session.rollback()
                            return jsonify(error="You don't have any default adddress" )
                            # defaultadddata1=Useraddress.query.filter(Useraddress.user_id==current_user.id).filter(Useraddress.address_id.address_id ==data.address_id).filter(Useraddress.default_flag==True).first()
                            # defaultadddata1.default_flag=True
                            # db.session.commit()
                    return jsonify(success='Address Added Successfully',redirect='/addresslist')
                except:
                    db.session.rollback()
                    return jsonify(error='Error in adding Address')
            else:
                try:
                    
                    data=Useraddress.query.filter(Useraddress.address_id ==address_id).filter(Useraddress.user_id==current_user.id).first()
                    print('this is useraddress {}'.format(data.address_id))
                    data.first_name=x['first_name']
                    data.last_name=x['last_name']
                    data.address1=x['address1']
                    data.address2=x['address2']
                    data.landmark=x['landmark']
                    data.state=x['state']
                    data.city=x['city']
                    data.pincode=x['pincode']
                    data.mobileno=x['mobileno']
                    data.default_flag=x['default_flag']
                    data.user_id=current_user.id
                    db.session.add(data)
                    db.session.commit()
                    if  x['default_flag']==True:
                        try:
                            defaultadddata=Useraddress.query.filter(Useraddress.user_id==current_user.id).filter(Useraddress.address_id!=address_id).filter(Useraddress.default_flag==True).first()
                            defaultadddata.default_flag=False
                            db.session.commit()
                            # defaultadddata1=Useraddress.query.filter(Useraddress.user_id==current_user.id).filter(Useraddress.address_id==address_id).first()
                            # defaultadddata1.default_flag=True
                            # db.session.commit()
                        except:
                            print('THIS IS CURRENT {} WITH ADDRESS_ID {}'.format(address_id,current_user.id))
                            
                    return jsonify(success='Address Updated Successfully',redirect='/addresslist')
                except:
                    return jsonify(error='Address not found')
        else:
            x=jsonify(fielderror=form.errors)
            print(x)

            return jsonify(fielderror=form.errors)
    else:
        if address_id==None:
            return render_template('user_management/addaddress.html', form=form,address_id=address_id)
        else:
            try:
                data=Useraddress.query.filter(Useraddress.user_id==current_user.id).filter(Useraddress.address_id==address_id).first()
                form = AddAddressForm(obj=data)
                form.populate_obj(data)
                print(form.landmark.data)
                return render_template('user_management/addaddress.html', form=form,address_id=address_id)
            except:
                return redirect(404)

    # return render_template('user_management/addaddress.html', form=form)    