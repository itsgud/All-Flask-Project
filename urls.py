from flask import Flask,redirect,url_for
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/student')
def student():
    return 'this is students page!'


@app.route('/faculty')
def faculty():
    return 'this is faculty page!'


@app.route('/user/<name>/')
def user(name):
    if name=='student':
        return redirect(url_for('student'))
    elif name=='faculty':
        return redirect(url_for('faculty'))
    
    return 'this is dyanamic page for user !!!'



if __name__=="__main__":
    app.run(debug=True)
