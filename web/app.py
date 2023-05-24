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


@app.route("/")
def home():
    if 'nick' in session:
        nick = session['nick'] 
        me = Teacher.query.filter_by(nick=nick).first()
        return render_template("home.html", me=me)

    return redirect(url_for('home'))


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


@app.route("/logout")
def logout():
    session.pop("nick", None)
    return redirect(url_for('login'))


@app.route("/all_list")
def all_list():
    return render_template("all_list.html")


@app.route("/calender_detail")
def calender_detail():
    return render_template("calender_detail.html")


@app.route("/course")
def course():
    return render_template("course.html")

if __name__ == "__main__":
    
    app.debug = True
    app.run()
