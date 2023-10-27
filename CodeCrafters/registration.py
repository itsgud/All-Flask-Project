from flask import Flask, render_template, request, redirect, send_file,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from werkzeug.utils import redirect
from datetime import datetime
from sqlalchemy import create_engine
import pandas as pd 
from io import BytesIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key='login'

db = SQLAlchemy(app)
app.app_context().push()

db_url="sqlite:///todo.db"
engine=create_engine(db_url)


 
class contact_detail(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(250),unique=True, nullable=False)
    password = db.Column(db.String(250))

class blog(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=False, nullable=False)  # user name which is logged in ...
    blog_content = db.Column(db.String(250),unique=True, nullable=False) 
    title = db.Column(db.String(250),nullable=True)
    website_link=db.Column(db.String(250),nullable=True)
    github=db.Column(db.String(250),nullable=True)
    tech_use=db.Column(db.String(250),nullable=True)
    domain=db.Column(db.String(250),nullable=True)





@app.route('/')
def home():
    projects=blog.query.all()
    return render_template('index.html',projects=projects)


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
             return render_template('profile.html')
        else:
            return "Login Failed"
           

    return render_template('signin.html')



@app.route('/signup',methods=["GET", "POST"])
def Signp():
    if request.method=='POST' and request.form['uname']=='guddu' :
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
    msg='Try with the secret Code Value  !!!!'
    return render_template('signup.html',msg=msg )


@app.route('/addpost',methods=['GET','POST'])
def addpost():
   if 'user' in session:
    nm=session['user']
    if request.method=='POST':
        title=request.form['title']
        blog_content=request.form['blog_content']
        website=request.form['web']
        github=request.form['github']
        tech=request.form['tech']
        domain=request.form['domain']
        entry=blog(email=nm,blog_content=blog_content,title=title,website_link=website,github=github,tech_use=tech,domain=domain)
        db.session.add(entry)
        db.session.commit()
        return render_template('profile.html') 
    else:
        return render_template('addpost.html')
        
  



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



@app.route('/profile')
def profile():
    if 'user' in session :
        print("name of the useer is :  ",session['user'])
        nm=session['user']
        #posts=Blog.query.filter_by(email=session['user']).all()
        #posts=Blog.query.filter_by(email='raj')
        posts=blog.query.filter_by(email=session['user'])
        blog_posts=blog.query.all()
        return render_template('profile.html',blog_post=blog_posts,posts=posts,nm=nm)
    else:
        return render_template('signin.html')
    

    

@app.route('/editpost/<int:id>')
def editpost(id):
    if 'user' in session:
        nm=session['user']
        user=blog.query.filter_by(index=id).first()
        return render_template('editpost.html',username=nm,account=user)
    else:     
        return render_template('signin.html')


@app.route('/updatepost/<int:id>',methods=["GET", "POST"])
def updatepost(id):
    if 'user' in session:
        nm=session['user']
        if request.method=='POST':
            user=blog.query.filter_by(index=id).first()
            user.title=request.form['title']
            user.blog_content=request.form['blogdata']
            db.session.add(user)
            db.session.commit()
            return redirect('/profile')
        else:
            return "try again"
    else:   
        return render_template('login.html')



@app.route('/delete/<int:id>')
def deletepost(id):
    if 'user' in session :
        nm=session['user']
        user=blog.query.filter_by(index=id).first()
        db.session.delete(user)
        db.session.commit()
        return redirect('/profile')
    else:
        return render_template('signin.html')



@app.route('/download-excel')
def download_excel():
    # Retrieve data from the database table
    data = blog.query.all()

    # Create a Pandas DataFrame from the retrieved data
    data_dict = [{'column1': item.title, 'column2': item.blog_content} for item in data]
    df = pd.DataFrame(data_dict)

    # Create an Excel writer in memory
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, sheet_name='YourTableData', index=False)
    writer.close()
    output.seek(0)

    # Serve the Excel file as a downloadable attachment
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name='table_data.xlsx')


if __name__=="__main__":
        app.run(debug=True)
