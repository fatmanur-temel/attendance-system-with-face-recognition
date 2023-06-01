from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = "erawebsiteforuni"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost/attendace'
db = SQLAlchemy(app)


class Teacher(db.Model):
    _tablename_ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String)
    password = db.Column(db.String)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String)
    tel = db.Column(db.String)
    faculty = db.Column(db.String)
    department = db.Column(db.String)
    photo = db.Column(db.String)
    courses = db.relationship('Lesson', backref='teacher', lazy=True)

class Lesson(db.Model):
    __tablename__ = 'lesson'
    id = db.Column(db.Integer, primary_key=True)
    lesson_name = db.Column(db.String)
    period = db.Column(db.Integer)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))



@app.route('/')
def root():
    return redirect(url_for('login'))


@app.route("/login", methods = ["GET", "POST"])
def login():
    if 'nick' in session:
        return redirect(url_for('home'))
    

    if request.method == "POST":
        nick = request.form.get("nick")
        password=request.form.get("password")
        search = Teacher.query.filter_by(nick=nick).first()

        if search is None:
            flash("YANLIŞ KULLANICI ADI")
            return render_template("login.html")
        
    
        if password == search.password:
            session['nick'] = nick
            return redirect(url_for('home'))
        else:
            flash("YANLIŞ ŞİFRE")
            return render_template("login.html")
    
    return render_template("login.html")

@app.route("/home")
def home():
    if 'nick' in session:
        nick = session['nick'] 
        teacher = Teacher.query.filter_by(nick=nick).first()
        teacher_id = teacher.id
        teachers_lessons = db.session.query(Lesson.lesson_name, Lesson.period).join(Teacher).filter(Lesson.teacher_id == teacher_id).all()
        

        return render_template("home.html", teacher=teacher, 
                               name=teacher.name, surname=teacher.surname, email=teacher.email, tel=teacher.tel, 
                               faculty=teacher.faculty, department=teacher.department, photo=teacher.photo, courses=teachers_lessons)

    return redirect(url_for('home'))




@app.route("/logout")
def logout():
    session.pop("nick", None)
    return redirect(url_for('login'))


@app.route("/all_list")
def all_list():
    if 'nick' in session:
        nick = session['nick'] 
        teacher = Teacher.query.filter_by(nick=nick).first()
        teacher_id = teacher.id
        teachers_lessons = db.session.query(Lesson.lesson_name, Lesson.period).join(Teacher).filter(Lesson.teacher_id == teacher_id).all()
        return render_template("all_list.html", teacher=teacher,courses=teachers_lessons)


@app.route("/calendar_detail")
def calendar_detail():
    if 'nick' in session:
        nick = session['nick'] 
        teacher = Teacher.query.filter_by(nick=nick).first()
        teacher_id = teacher.id
        teachers_lessons = db.session.query(Lesson.lesson_name, Lesson.period).join(Teacher).filter(Lesson.teacher_id == teacher_id).all()
        return render_template("calendar_detail.html", teacher=teacher,courses=teachers_lessons)


@app.route('/course/<lesson_name>')
def course(lesson_name):
    if 'nick' in session:
        nick = session['nick'] 
        teacher = Teacher.query.filter_by(nick=nick).first()
        teacher_id = teacher.id
        teachers_lessons = db.session.query(Lesson.lesson_name, Lesson.period).join(Teacher).filter(Lesson.teacher_id == teacher_id).all()
        return render_template("course.html", teacher=teacher,courses=teachers_lessons,  lesson_name=lesson_name)

if __name__ == "__main__":
    
    app.debug = True
    app.run()
