import json
from flask import Flask ,render_template
from flask_mail import Mail, Message 
   
app = Flask(__name__) 
app.secret_key='login'

mail = Mail(app) # instantiate the mail class 
   
with open('config.json','r')as f:
   params=json.load(f)['param']

# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = params['gmail-user']
app.config['MAIL_PASSWORD'] = params['gmail-password']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 
   
# message object mapped to a particular URL ‘/’ 


@app.route('/')
def login1():
   return 'hiiii this is index page !!! '
    #return render_template('contactform.html')


@app.route("/contact") 
def contact(): 
   msg = Message( 
                'Important Mail', 
                sender ='guddu01bpmce@gmail.com', 
                recipients = ['guddukumar2822002@gmail.com'] 
               ) 
   msg.body = 'Hello Flask message sent from Flask-Mail'
   mail.send(msg) 
   return 'Sent'
   
if __name__ == '__main__': 
   app.run(debug = True)