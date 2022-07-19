from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
app.secret_key = "THIS IS MY SECRET"

DATABASE = "users_login_schema"