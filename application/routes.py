# creating routes
from application import app, db, api
from flask import Response, render_template, request, flash, redirect, url_for, json, jsonify, session
from application.forms import LoginForm, RegisterForm
from application.models import User, Course, Enrollment
from application.course_list import course_list
from application.term_course_list import term_courses
from flask_restx import Resource

# courseData = [
#     {"courseID": "1111", "title": "PHP 111", "description": "Intro to PHP", "credits": "3", "term": "Fall, Spring"},
#     {"courseID": "2222", "title": "Java 1", "description": "Intro to Java Programming", "credits": "4",
#      "term": "Spring"},
#     {"courseID": "3333", "title": "Adv PHP 201", "description": "Advanced PHP Programming", "credits": "3",
#      "term": "Fall"},
#     {"courseID": "4444", "title": "Angular 1", "description": "Intro to Angular", "credits": "3",
#      "term": "Fall, Spring"},
#     {"courseID": "5555", "title": "Java 2", "description": "Advanced Java Programming", "credits": "4",
#     "term": "Fall"}]


########################################################################

# @api.route('/api', '/api/')
# class GetAndPost(Resource):
#     def get(self):
#         return jsonify(User.objects.all())  # get all the data from the user collection in db
#
#     def post(self):
#         data = api.payload
#         new_user = User(user_id = data['user_id'], email=data['email'], first_name=data['first_name'], last_name=data['last_name'])
#         new_user.set_password(data['password'])
#         new_user.save()
#         return jsonify(new_user)
#
#
# @api.route('/api/<idx>')
# class GetUpdateDelete(Resource):
#     def get(self, idx):
#         return jsonify(User.objects(user_id=idx))  # get all the data from the user collection in db
#
#     def put(self, idx):
#         data = api.payload
#         user = User.objects(user_id=idx).update(**data)
#         return jsonify(User.objects(user_id=idx))
#
#     def delete(self, idx):
#         res = User.objects(user_id=idx).delete()
#         return jsonify(res)




########################################################################

@app.route("/")  # decorators
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get('username'):
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.objects(email=email).first()
        # print(user)

        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!", "success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            # if request.form.get("email") == "test@uta.com":
            return redirect("/index")
        else:
            flash("Sorry, something went wrong.", "danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/courses/")
@app.route("/courses/<term>")
def courses(term=None):
    if term is None:
        term = "2019"
    classes = term_courses(term)
    print(len(classes))
    print(classes)
    # classes = Course.objects.order_by('+courseID')
    return render_template("courses.html", courseData=classes, courses=True, term=term)


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count() + 1
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()
        flash("You are successfully registered!", "success")
        return redirect(url_for('index'))
    return render_template("register.html", title='Register', form=form, register=True)


@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    if not session.get('username'):
        return redirect(url_for('login'))

    courseID = request.form.get('courseID')
    courseTitle = request.form.get('title')
    user_id = session.get('user_id')
    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"Oops! You are already registered in this course {courseTitle}!", "danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(f"You are enrolled in {courseTitle}!", "success")
    classes = course_list(user_id)
    return render_template("enrollment.html", enrollment=True, title='Enrollment', classes=classes)


@app.route("/logout")
def logout():
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('login'))


# @app.route("/api/")
# @app.route("/api/<idx>")
# def api(idx=None):
#     if (idx == None):
#         jdata = courseData
#     else:
#         jdata = courseData[int(idx)]
#
#     return Response(json.dumps(jdata), mimetype="application/json")

# class User(db.Document):
#     user_id = db.IntField(unique=True)
#     first_name = db.StringField(max_length = 50)
#     last_name = db.StringField(max_length = 50)
#     email = db.StringField(max_length=30)
#     password = db.StringField(max_length=30)
#
# @app.route("/user")
# def user():
#     # User(user_id=1, first_name="Jahnavi", last_name="P", email="user@gmail.com", password="abcd@1234").save()
#     # User(user_id=1, first_name="Elsa", last_name="Potter", email="elsa@gmail.com", password="xyz@908").save()
#     # User(user_id=2, first_name="Hermoine", last_name="Granger", email="hermoine@hogwarts.edu", password="abcz@908").save()
#     users = User.objects.all()
#     print(jsonify(users))
#     return render_template("user.html", users=users)
