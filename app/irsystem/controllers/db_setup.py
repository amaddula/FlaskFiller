# from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
# import os
# from sqlalchemy import func
# from datetime import datetime
from app import db
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# db = SQLAlchemy(app)

#######################################################################
# Create our database model
class test_table(db.Model):
    __tablename__ = "test_table"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email

# # Set "homepage" to index.html
# @app.route('/')
# def index():
#     print "I'm here!!!!!!!!!!!!!!!!!"
#     print User.query.filter(email = "hello@world.com").all()
#     return render_template('index.html')
#
# # Save e-mail to database and send to success page
# @app.route('/prereg', methods=['POST'])
# def prereg():
#     email = None
#     if request.method == 'POST':
#         email = request.form['email']
#         # Check that email does not already exist (not a great query, but works)
#         if not db.session.query(User).filter(User.email == email).count():
#             reg = User(email)
#             db.session.add(reg)
#             db.session.commit()
#             return render_template('success.html')
#     return render_template('index.html')

# if __name__ == '__main__':
#     app.debug = True
#     app.run()
