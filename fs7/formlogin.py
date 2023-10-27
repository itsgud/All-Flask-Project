from flask import Flask,jsonify,request,url_for,render_template


app=Flask(__name__)


@app.route('/')
def home():
    
    return render_template('form.html')


@app.route('/formlogin',methods=['GET','POST'])
def loginuser():
                   
    name=request.form['uname']
    pwd=request.form['password']
    if name=='guddu' and pwd=='123':
        return 'hii guddu succussfully logged in !!!'
        
    return "try again"




if __name__=="__main__":
        app.run(debug=True)
