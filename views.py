from flask import Flask, render_template, redirect, request, g, session, url_for, flash, jsonify, Response
from model import User, Post
from flask.ext.login import LoginManager, login_required, login_user, current_user
from flaskext.markdown import Markdown
import config
import forms
import model
import json

app = Flask(__name__)
app.config.from_object(config)

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
tasks = [
    {
        'id': 1,
        'description': u'Blood clot.', 
        'patient': {'id': 1, 'name': u'Count Dracula', 'age': 128, 'phoneNumber': '408-807-4454'}
    },
    {
        'id': 2,
        'description': u'Jaundice.', 
        'patient': {'id': 2, 'name': u'Big Bird', 'age': 54, 'phoneNumber': '408-807-7577'}
    },
    {
        'id': 3,
        'description': u'Irritable bowel syndrome',
        'patient': {'id': 3, 'name': u'Oscar The Grouch', 'age': 25, 'phoneNumber': '408-821-9088'}
    },
    {
        'id': 4,
        'description': u'Diabetic coma.',
        'patient': {'id': 4, 'name': u'Cookie Monster', 'age': 5, 'phoneNumber': '408-266-5437'}
    },
    {
        'id': 5,
        'description': u'Halitosis',
        'patient': {'id': 3, 'name': u'Oscar The Grouch', 'age': 25, 'phoneNumber': '408-821-9088'}
    }
    
]

patient_tasks = [
    {
        'id': 4,
        'description': u'Diabetic coma.',
    },
    {
        'id': 5,
        'description': u'Halitosis',
    }
]
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
@app.route("/")
def index():
    # posts = Post.query.all()
    # return render_template("index.html", posts=posts)
    # js = json.dumps( {'tasks': tasks} )
    # resp = Response(js, status=200, mimetype='application/json')
    # return resp
    
    return jsonify({'tasks': tasks})

@app.route("/tasks/<int:id>")
def view_tasks(id):
    return jsonify({'tasks': patient_tasks})    

@app.route("/post/<int:id>")
def view_post(id):
    post = Post.query.get(id)
    return render_template("post.html", post=post)

@app.route("/post/new")
@login_required
def new_post():
    return render_template("new_post.html")

@app.route("/post/new", methods=["POST"])
@login_required
def create_post():
    form = forms.NewPostForm(request.form)
    if not form.validate():
        flash("Error, all fields are required")
        return render_template("new_post.html")

    post = Post(title=form.title.data, body=form.body.data)
    current_user.posts.append(post) 
    
    model.session.commit()
    model.session.refresh(post)

    return redirect(url_for("view_post", id=post.id))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def authenticate():
    form = forms.LoginForm(request.form)
    if not form.validate():
        flash("Incorrect username or password") 
        return render_template("login.html")

    email = form.email.data
    password = form.password.data

    user = User.query.filter_by(email=email).first()

    if not user or not user.authenticate(password):
        flash("Incorrect username or password") 
        return render_template("login.html")

    login_user(user)
    return redirect(request.args.get("next", url_for("index")))


if __name__ == "__main__":
    app.run(debug=True)
