from flask import Flask,jsonify,request,url_for,render_template


app=Flask(__name__)


@app.route('/')
def home():
    return render_template('fill.html')


@app.route('/formlogin',methods=['GET','POST'])
def loginuser():             
    result=request.form
    f=request.files['file']
    f.save(f.filename
           )
    return render_template("fetch.html",result=result,file=f)



if __name__=="__main__":
        app.run(debug=True)
