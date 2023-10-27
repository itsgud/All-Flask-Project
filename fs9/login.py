from flask import Flask,jsonify,request,url_for,render_template,session


app=Flask(__name__)
app.secret_key='login'



@app.route('/')
def login1():
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('email',None)
    return render_template('login.html')



@app.route('/login',methods=['GET','POSt'])
def login():
    if request.method=='POST':
         username=request.form['username']
         pwd=request.form['password']
         if username=='guddu' and pwd=='123':
              session['email']=username
              return render_template("success.html",email=username)
         else:
              msg="invalid user name or password !"
              return render_template("login.html",msg=msg)

    return render_template('login.html')


@app.route('/profile')
def profile():
    if 'email' in session:
         email=session['email']
         return render_template('profile.html', name=email)
    else:
         msg="Lofin first !!!"
         return render_template("login.html",msg=msg)
    







if __name__=="__main__":
        app.run(debug=True)
