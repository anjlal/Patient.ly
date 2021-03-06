from flask import Flask, render_template, redirect, request, g, session, url_for, flash, jsonify, Response
from model import Patient, Provider, Task, Note #User, Post
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
import config
import forms
import model
import json
import os
import twilio.twiml
from twilio.rest import TwilioRestClient
import logging
from logging.handlers import RotatingFileHandler
from werkzeug import secure_filename

UPLOAD_FOLDER = 'static/patient_photos'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# Pull in configuration from system environment variables
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.environ.get('TWILIO_NUMBER')

# create an authenticated client that can make requests to Twilio for your
# account.
client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

app = Flask(__name__)
app.config.from_object(config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Stuff to make login easier
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# End login stuff

# Adding markdown capability to the app
Markdown(app)
# patients = [
#     {
#         'id': 1,
#         'name': u'Anjana Lal',
#         'description': u'Stiff neck.', 
#     },
#     {
#         'id': 2,
#         'name': u'Smita Lal',
#         'description': u'Femara refill.', 
#     },
#     {
#         'id': 3,
#         'name': u'Rishi Lal',
#         'description': u'Migraine.',
#     }
#     
# ]
# patients = [
#     {
#         'id': 1,
#         'name': u'Anjana Lal',
#         'description': u'Stiff neck.', 
#     },
#     {
#         'id': 2,
#         'name': u'Smita Lal',
#         'description': u'Femara refill.', 
#     },
#     {
#         'id': 3,
#         'name': u'Rishi Lal',
#         'description': u'Migraine.',
#     }
#     
# ]
# tasks = [
#     {
#         'id': 1,
#         'description': u'Blood clot.', 
#         'patient': {'id': 1, 'name': u'Count Dracula', 'age': 128, 'phoneNumber': '408-807-4454'},
#         'providerId': 2,
#         'status': 'UNREAD'
#     },
#     {
#         'id': 3,
#         'description': u'Irritable bowel syndrome',
#         'patient': {'id': 3, 'name': u'Oscar The Grouch', 'age': 25, 'phoneNumber': '408-821-9088'},
#         'providerId': 2,
#         'status': 'UNREAD'
#     },
#     {
#         'id': 2,
#         'description': u'Jaundice.', 
#         'patient': {'id': 2, 'name': u'Big Bird', 'age': 54, 'phoneNumber': '408-807-7577'},
#         'providerId': 3,
#         'status': 'UNREAD'  
#     },
#     {
#         'id': 4,
#         'description': u'Diabetic coma.',
#         'patient': {'id': 4, 'name': u'Cookie Monster', 'age': 5, 'phoneNumber': '408-266-5437'},
#         'providerId': 3,
#         'status': 'UNREAD'
#     },
#     {
#         'id': 5,
#         'description': u'Halitosis',
#         'patient': {'id': 3, 'name': u'Oscar The Grouch', 'age': 25, 'phoneNumber': '408-821-9088'},
#         'providerId': 1,
#         'status': 'READ'    
#     },
#     {
#         'id': 6,
#         'description': u'asfasdf',
#         'patient': {'id': 3, 'name': u'Oscar The Grouch', 'age': 25, 'phoneNumber': '408-821-9088'},
#         'providerId': 1,
#         'status': 'READ'
#     }
# ]
# 
# patient_tasks = [
#     {
#         'id': 4,
#         'description': u'Diabetic coma.',
#         'status': u'UNREAD'
#     },
#     {
#         'id': 5,
#         'description': u'Halitosis',
#         'status': u'READ'
#     }
# ]
# 
# providers = [
#     {
#         'id': 1,
#         'email': u'angie@hb.com',
#         'phoneNumber': u'+14089161903'
#     },
#     {
#         'id': 3,
#         'email': u'drwho@hb.com',
#         'phoneNumber': u'+14089161903'
#     },
#     {
#         'id': 2,
#         'email': u'drseus@hb.com',
#         'phoneNumber': u'+14089161903'
#     }
# ]
# 
# tasks = [
#     {
#         'id': 1,
#         'pid': 1,
#         'pname': u'Anjana Lal',
#         'description': u'Stiff neck.'
#     },
#     
#     {
#         'id': 2,
#         'pid': 3,
#         'pname': u'Rishi Lal',
#         'description': u'Migraine.'
#     },
#     {
#         'id': 3,
#         'pid': 2,
#         'pname': u'Smita Lal',
#         'description': u'Femara refill'
#     }
# ]
@app.route("/", methods=["GET", "POST"])
def index():
    # posts = Post.query.all()
    # return render_template("index.html", posts=posts)
    # js = json.dumps( {'tasks': tasks} )
    # resp = Response(js, status=200, mimetype='application/json')
    # return resp
    
    resp = twilio.twiml.Response()
    message = "Thank you for your message! We will process your request ASAP."
    
    text_body = request.values.get('Body')
    from_number = request.values.get('From')
    
    # return jsonify(json_list=[i.serialize for i in qryresult.all()])
    # serialized_tasks = serialize_tasks(provider.id)

    
    patient = Patient.query.filter_by(phone_number=from_number).first()
    provider = Provider.query.get(3)
    task = Task(description=text_body, patient_id=patient.id, provider_id=provider.id)
    model.session.add(task)
    model.session.commit()
    
    
    resp.sms(message)
    return str(resp)

    
    
    # return jsonify({'tasks': tasks})
@app.route("/tasks/<int:id>/reassign", methods=["POST"])
def reassign(id):
    updated_task = Task.query.filter_by(id=id).first()
    updated_task.provider_id = int(request.form['providerId'])
    model.session.commit()
    return jsonify(task=updated_task.serialize_task)

@app.route("/tasks/<int:id>/status", methods=["POST"])
def change_status(id):
        updated_task = Task.query.filter_by(id=id).first()
        updated_task.status = request.form['status']
        model.session.commit()
        return jsonify(task=updated_task.serialize_task)    

@app.route("/tasks/<int:id>/description", methods=["POST"])
def change_description(id):
    updated_task = Task.query.filter_by(id=id).first()
    updated_task.description = request.form['description']
    model.session.commit()
    return jsonify(task=updated_task.serialize_task)
    
@app.route("/tasks")
def view_tasks():
    provider = Provider.query.get(request.values.get('provider_id'))
    tasks = Task.query.filter_by(provider_id=provider.id, status='UNREAD').all()
    return jsonify(tasks=[task.serialize_task for task in tasks])
    # return jsonify({'tasks': tasks})  

@app.route("/tasks/create", methods=["POST"])
def create_task():
    description = request.form['description']
    provider_id = int(request.form['provider_id'])
    patient_id = int(request.form['patient_id'])
    
    task = Task(description=description, patient_id=patient_id, provider_id=provider_id)
    model.session.add(task)
    model.session.commit()
    
    return jsonify(task=task.serialize_task)   
    
@app.route("/patients/<int:id>/message", methods=["POST"])
def messaging_patient(id):
    message = request.form['message']
    provider_id = int(request.form['providerId'])

    patient = Patient.query.get(id)
    provider = Provider.query.get(provider_id)
    
    # send_message_helper(patient.name, provider.name, patient.phone_number, message)
    intro = "Hello %s, this is Dr. %s. " % (patient.name, provider.name)
    if (message):
        body_text = intro + message
        # return redirect(url_for("send_message", message=body_text, phone_number=patient.phone_number))
        # Send a text message to the number provided
        sms_message = client.sms.messages.create(to=patient.phone_number,
                                             from_=TWILIO_NUMBER,
                                             body=body_text)

        # Return a message indicating the text message is enroute
        # return 'Message on the way!'
        return jsonify({'result': 'success'})
     
@app.route("/patients/<int:id>/tasks", methods=["GET"])
def view_task(id):
    patient_tasks = Task.query.filter_by(patient_id=id).all()
    return jsonify(tasks=[i.serialize_task for i in patient_tasks])
    
    
    # return jsonify({'tasks': patient_tasks})    
@app.route("/patients")
def view_patients():    
    patients = Patient.query.all()
    return jsonify(patients=[i.serialize_patient for i in patients])
    
@app.route("/patients/create", methods=["POST"])
def create_patient():
    name = request.form['name']
    sex = request.form['sex']
    birth_year = int(request.form['birthYear'])
    phone_number = request.form['phoneNumber']
    provider_id = int(request.form['providerId'])
    
    
    patient = Patient(name=name, birth_year=birth_year, phone_number=phone_number, sex=sex)
    model.session.add(patient)
    model.session.commit()
    
    photo = request.files['photo']
    if photo:
        # and allowed_file(photo.fileName):
        # filename = secure_filename(file.filename)
        filename = "patient_%d_image.jpg" % patient.id
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        patient.photo_filename = filename
        model.session.commit()
    
    provider = Provider.query.get(provider_id)
    # send_message_helper(patient.name, provider.name, patient.phone_number, message)
    intro = "Hello %s, this is Dr. %s. " % (patient.name, provider.name)
    message = "Feel free to send me a message here with your requests/concerns."
    body_text = intro + message

    # Send a text message to the number provided
    sms_message = client.sms.messages.create(to=patient.phone_number,
                                         from_=TWILIO_NUMBER,
                                         body=body_text)    
    return jsonify(patient=patient.serialize_patient)    

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/providers")
def view_providers():
    providers = Provider.query.all()
    return jsonify(providers=[i.serialize_provider for i in providers])


    # return jsonify({'providers': providers})
    
@app.route("/providers/log_in", methods=["POST"]) 
def login():
    email = request.form['email']
    pw = request.form['password']

    provider = Provider.query.filter_by(email=email, password=pw).first()
    if provider:
        return jsonify(token=(email+':'+pw), provider=provider.serialize_provider)
    else:
        return jsonify(error="Error: could not find user with given credentials"), 404
        
@app.route("/providers/current", methods=["GET"]) 
def current_provider():
    token = request.values.get('token')
    tokenized = token.split(":")
    email = tokenized[0]
    pw = tokenized[1]

    provider = Provider.query.filter_by(email=email, password=pw).first()
    if provider:
        return jsonify(provider=provider.serialize_provider)
    else:
        return jsonify(error="Error: could not find user with given credentials"), 404

# Handle a POST request to send a text message.
# @app.route('/message/<message>/<phone_number>', methods=['POST'])
# def send_message(message, phone_number):
#     # Send a text message to the number provided
#     message = client.sms.messages.create(to=phone_number,
#                                          from_=TWILIO_NUMBER,
#                                          body=body_text)
# 
#     # Return a message indicating the text message is enroute
#     return 'Message on the way!' 
# def send_message_helper(name, provider_name, phone_number, message=None):
#     intro = "Hello %s, this is %s. " % (name, provider_name)
#     if (message):
#         body_text = intro + message
#         return redirect(url_for("send_message", message=body_text, phone_number=phone_number))
#     body_text = intro + "Feel free to send me a message here with your requests/concerns."
#     return redirect(url_for("send_message", message=body_text, phone_number=phone_number))
     
    
# @app.route("/post/<int:id>")
# def view_post(id):
#     post = Post.query.get(id)
#     return render_template("post.html", post=post)
# 
# @app.route("/post/new")
# @login_required
# def new_post():
#     return render_template("new_post.html")
# 
# @app.route("/post/new", methods=["POST"])
# @login_required
# def create_post():
#     form = forms.NewPostForm(request.form)
#     if not form.validate():
#         flash("Error, all fields are required")
#         return render_template("new_post.html")
# 
#     post = Post(title=form.title.data, body=form.body.data)
#     current_user.posts.append(post) 
#     
#     model.session.commit()
#     model.session.refresh(post)
# 
#     return redirect(url_for("view_post", id=post.id))

# @app.route("/login")
# def login():
#     return render_template("login.html")

# @app.route("/login", methods=["POST"])
# def authenticate():
#     form = forms.LoginForm(request.form)
#     if not form.validate():
#         flash("Incorrect username or password") 
#         return render_template("login.html")
# 
#     email = form.email.data
#     password = form.password.data
# 
#     user = User.query.filter_by(email=email).first()
# 
#     if not user or not user.authenticate(password):
#         flash("Incorrect username or password") 
#         return render_template("login.html")
# 
#     login_user(user)
#     return redirect(request.args.get("next", url_for("index")))
# 
# def create_task(text_body, from_number):
#     patient = Patient.query.filter_by(phone_number=from_number).first()
#     provider = Provider.query.get(3)
#     task = Task(description=text_body, patient_id=patient.id, provider_id=provider.id)

if __name__ == "__main__":
    # handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    # handler.setLevel(logging.INFO)
    # app.logger.addHandler(handler)
    # app.run()
    app.run(debug=True)
