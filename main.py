from enum import unique
from operator import pos
from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
import json
from flask_mail import Mail


# opening json file
with open('config.json','r') as c:
    parameter = json.load(c) ["params"]

local_server = True
# app and sql connect inistialise
app = Flask(__name__)

#sending mail logic
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME= parameter['gmail-user'],
    MAIL_PASSWORD = parameter['gmail-password'],
)
mail = Mail(app)


if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = parameter['local_url']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = parameter['prod_url']
  
db=  SQLAlchemy(app)


# classes for connecting table
class Contacts(db.Model):
    '''
    sno ,name , phone_num, msg , date , email
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80),nullable=False,unique=False)
    phone_num = db.Column(db.String(12),nullable=False)
    msg = db.Column(db.String(80),nullable=False)
    date = db.Column(db.String(12),nullable=True)
    email = db.Column(db.String(20), nullable=False)


class Posts(db.Model):
  
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),nullable=False,unique=False)
    subtitle = db.Column(db.String(80),nullable=False,unique=False)
    slug = db.Column(db.String(21),nullable=False)
    content = db.Column(db.String(120),nullable=False)
    date = db.Column(db.String(12),nullable=True)
    img_name = db.Column(db.String(12),nullable=True)
   


#routes
@app.route("/")
def home():

    posts = Posts.query.filter_by().all()[0:parameter["no_of_post"]]
    return render_template('index.html', params = parameter , posts= posts)


@app.route("/post/<string:post_slug>",methods = ['GET'])
def post_routes(post_slug):
    post = Posts.query.filter_by(slug = post_slug).first()
    return render_template('post.html', params = parameter, post=post )


@app.route("/about")
def about():
    return render_template('about.html', params = parameter)


@app.route("/contact" , methods = ["GET", "POST"])
def contact(): 
    if(request.method == "POST"):
        '''ADD TO DATABASE'''
        name = request.form.get('name')
        email = request.form.get('email')
        phone= request.form.get('phone')
        message = request.form.get('message')

        # Adding to database
        entry = Contacts(name=name , phone_num = phone, msg=message, date= datetime.now() ,email = email)
        db.session.add(entry)
        db.session.commit()

        #recieving mail
        # mail.send_message(
        #     'New message from' + name,
        #     sender = email,
        #     recipients = [parameter['gmail-user']],
        #     body = message + "\n" + phone
        # )
        
    return render_template('contact.html', params = parameter)


app.run(debug=True)

