from flask import Flask, render_template, request, redirect,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from werkzeug.utils import redirect
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key='login'

db = SQLAlchemy(app)
app.app_context().push()



 
class contact_detail(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(250),unique=True, nullable=False)
    password = db.Column(db.String(250))
    

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/signin',methods=["GET", "POST"])
def signin():
    if request.method=='POST':
        user=request.form['username']
        pwd=request.form['password']
        print("name o f the user is:  ",user)
        print(" password of user:  ",pwd)
        #from database 
        usr=contact_detail.query.filter_by(name=user).first()
        pas=usr.password
        print("form database usr and roll : ",usr.name,pas)
        if (sha256_crypt.verify(pwd,pas)):
             session['user']=user 
             return render_template('test.html')
        else:
            return "Login Failed"
           

    return render_template('signin.html')



@app.route('/signup',methods=["GET", "POST"])
def Signp():
    if request.method=='POST':
        Roll=request.form['roll']
        nam=request.form['uname']
        email=request.form['email']
        
        password=request.form['password']
        print(nam,email,password) 
        encpassword=sha256_crypt.encrypt(password)
        entry=contact_detail(sno=Roll,name=nam,email=email,password=encpassword)
        db.session.add(entry)
        db.session.commit()
        flash('refistration done succesfully')
        return redirect(url_for('signin'))
    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.pop('user',None)
    return render_template('signin.html')


@app.route('/about')
def About():
    return render_template('about.html')


@app.route('/blog')
def Blog():
    return render_template('blog.html')


@app.route('/services')
def Service():
    return render_template('services.html')


@app.route('/contact')
def Contact():
    return render_template('contact.html')




if __name__=="__main__":
        app.run(debug=True)
