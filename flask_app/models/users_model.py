from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, app
from flask import flash
from flask_bcrypt import Bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
bcrypt = Bcrypt( app )

class User:
    def __init__( self, data ):
        self.id = data[ 'id' ]
        self.first_name = data[ 'first_name' ]
        self.last_name = data[ 'last_name' ]
        self.email = data[ 'email' ]
        self.password = data[ 'password' ]
        self.created_at = data[ 'created_at' ]
        self.updated_at = data[ 'updated_at' ]

    @classmethod
    def get_one( cls, data ):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL( DATABASE ).query_db( query, data )
        print( 'RESULT====', result )
        if result:
            current_user = cls( result[0] )
            return current_user
        else:
            return None

    @classmethod
    def create_one( cls, data ):
        query = "INSERT INTO users( first_name, last_name, email, password )"
        query += "VALUES( %(first_name)s, %(last_name)s, %(email)s, %(password)s );"
        return connectToMySQL( DATABASE ).query_db( query, data )

    @staticmethod
    def validate_login( data ):
        is_valid = True
        if len( data['email'] ) == 0:
            flash( "You must provide your email", "error_login_email" )
            is_valid = False
        if len( data['password'] ) == 0:
            flash( "You must provide your password", "error_login_password" )
            is_valid = False
        return is_valid

    @staticmethod
    def validate_registration( data ):
        is_valid = True
        if len( data['first_name'] ) < 2:
            flash( "Please provide your first name", "error_registration_first_name" )
            is_valid = False
        if len( data['last_name'] ) < 2:
            flash( "Please provide your last name", "error_registration_last_name" )
            is_valid = False
        if len( data['email'] ) == 0:
            flash( "Please provide your email", "error_registration_email" )
            is_valid = False
        elif not EMAIL_REGEX.match( data[ 'email' ] ):
            flash( "Email not in valid format", "error_registration_email" )
            is_valid = False
        if len( data['password'] ) < 8:
            flash( "The password must be at least 8 characters long!", "error_registration_password" )
            is_valid = False
        if data['password'] != data['password_confirmation']:
            flash( "Passwords do not match", "error_registration_password_confirmation" )
            is_valid = False
        return is_valid
