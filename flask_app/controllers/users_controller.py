from flask_app import app 
from flask import render_template, redirect, session, request, flash
from flask_app.models.users_model import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt( app )

@app.route( '/' )
def home():
    return render_template( 'user_login.html' )

@app.route( '/logged' )
def loggedIn():
    if "logged_user" not in session:
        return redirect( '/' )
    logged_uid = int( session['logged_user'] )
    data = {
        "id" : session['logged_user']
    }
    context = {
        'user' : User.get_one( data )
    }
    return render_template( 'user.html', user = User.get_one( data ) )

@app.route( '/user/process_login', methods = [ 'POST' ] )
def process_login():
    is_valid = User.validate_login( request.form )
    current_user = User.get_one( request.form )
    if is_valid == False:
        return redirect( '/' )
    else:
        if is_valid != False:
            if not bcrypt.check_password_hash( current_user.password, request.form['password'] ):
                flash( "Invalid credentials", "error_login_invalid_credentials" )
                return redirect( '/' )
            session[ 'logged_user' ] = current_user.id
            session[ 'first_name' ] = current_user.first_name
            print( session )
            return redirect( '/logged' )

@app.route( '/user/process_registration', methods = [ 'POST' ] )
def process_registration():
    is_valid = User.validate_registration( request.form )
    if is_valid == False:
        return redirect( '/' )
    result = User.get_one( request.form )
    if result == False:
        flash( "this email is already in use, please type another one.", "error_registration_email" )
        return redirect( '/' )
    user_data = {
        **request.form,
        'password' : bcrypt.generate_password_hash( request.form['password'] )
    }
    print( 'USER DATA!!!!!!!!!!!!', user_data )
    user_id = User.create_one( user_data )
    if user_id != False:
        session[ 'logged_user' ] = user_id
        session[ 'first_name' ] = user_data.first_name
        return redirect( '/logged' )
    else:
        flash( "Something went wrong with the query", "error_registration_query" )
        return redirect( '/' )

@app.route( '/user/logout' )
def user_logout():
    del session[ 'logged_user' ]
    return redirect( '/' )

