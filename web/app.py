from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta


app = Flask(__name__)
app.config['DERS'] = None #global değişken
app.config['SECRET_KEY'] = "erawebsiteforuni" # flask veri güvenliği
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
    courses = db.relationship('Lesson', backref='teacher', lazy=True) #ilişkili nesneler yalnızca erişildiğinde yüklenir bu sayede performansta iyileşme sağlanır

class Lesson(db.Model):
    __tablename__ = 'lesson'
    id = db.Column(db.Integer, primary_key=True)
    lesson_name = db.Column(db.String)
    period = db.Column(db.Integer)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))

class Ders1(db.Model):
    __tablename__ = 'ders1'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    student_no = db.Column(db.String)
    student_name = db.Column(db.String)
    student_surname = db.Column(db.String)

class Ders2(db.Model):
    __tablename__ = 'ders2'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    student_no = db.Column(db.String)
    student_name = db.Column(db.String)
    student_surname = db.Column(db.String)

class Ders3(db.Model):
    __tablename__ = 'ders3'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    student_no = db.Column(db.String)
    student_name = db.Column(db.String)
    student_surname = db.Column(db.String)

class Ders4(db.Model):
    __tablename__ = 'ders4'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    student_no = db.Column(db.String)
    student_name = db.Column(db.String)
    student_surname = db.Column(db.String)
    
class Ders5(db.Model):
    __tablename__ = 'ders5'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    student_no = db.Column(db.String)
    student_name = db.Column(db.String)
    student_surname = db.Column(db.String)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_no = db.Column(db.Integer)
    photo = db.Column(db.String)
    student_name = db.Column(db.String)
    student_surname = db.Column(db.String)

class LessonStudent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

#ders sayısını hesapladığımız fonk. start end date alır
today = datetime.now().date()
target_date = datetime(2023, 7, 11).date()

start_date = datetime(2023, 2, 27)
if today > target_date:
    end_date = datetime(target_date.year, target_date.month, target_date.day)
else:
    end_date = datetime.now()


def get_lesson_id(lesson_name):
    lesson_id = None
    if lesson_name == "Ders1":
        lesson_id = 1
    elif lesson_name == "Ders2":
        lesson_id = 2
    elif lesson_name == "Ders3":
        lesson_id = 3
    elif lesson_name == "Ders4":
        lesson_id = 4
    elif lesson_name == "Ders5":
        lesson_id = 5
    elif lesson_name == "Ders6":
        lesson_id = 6
    elif lesson_name == "Ders7":
        lesson_id = 7
    elif lesson_name == "Ders8":
        lesson_id = 8
    elif lesson_name == "Ders9":
        lesson_id = 9
    elif lesson_name == "Ders10":
        lesson_id = 10

    return lesson_id


def ders_count(start_date, end_date):
    count = 0
    current_date = start_date

    # start_date'den end_date'e kadar döngü
    while current_date <= end_date:
        # Eğer gün Pazartesi ise count'u artır
        if current_date.weekday() == 0:  # Pazartesi: 0, Salı: 1, ...
            count += 1

        # Bir gün ilerlet
        current_date += timedelta(days=1)

    return count

# Başlangıç ve bitiş tarihlerini ayarla
start_date = datetime(2023, 2, 27)
end_date = datetime.now()


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

    return redirect(url_for('login'))




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

        ders_name = app.config['DERS']
        ders = globals()[ders_name]

        # Ders günü sayısını hesapla
        count = ders_count(start_date, end_date)-1

        #Öğrencilerin geldiği gün sayısını hesapla
        student_count = {}

        # Ders tablosundaki student_no değerlerinin tekrar sayısını hesapla
        students = ders.query.with_entities(ders.student_no).all()
        for student in students:
            student_no = student.student_no
            student_count[student_no] = student_count.get(student_no, 0) + 1

        # Öğrenci bilgilerini Student tablosundan al
        student_info = []
        for student_no in student_count.keys():
            record = Student.query.filter_by(student_no=student_no).first()
            student_info.append({
                'student_no': record.student_no,
                'student_name': record.student_name,
                'student_surname': record.student_surname,
                'student_count': count-student_count[student_no]
            })

        return render_template("all_list.html", teacher=teacher,courses=teachers_lessons, student_info=student_info, student_count=len(student_count), count=count)


@app.route('/course/<lesson_name>')
def course(lesson_name):
    if 'nick' in session:
        nick = session['nick']
        #session içindeki öğretmenin derslerini al
        teacher = Teacher.query.filter_by(nick=nick).first()
        teacher_id = teacher.id
        teachers_lessons = db.session.query(Lesson.lesson_name, Lesson.period).join(Teacher).filter(Lesson.teacher_id == teacher_id).all()
        
        #dersi alan öğrencilerin listesi
        lesson_id = get_lesson_id(lesson_name)
        lesson_students = LessonStudent.query.filter_by(lesson_id=lesson_id).count()

        # Ders adını al ve app.config üzerinde sakla
        app.config['DERS'] = lesson_name
        ders_name = app.config['DERS']
        ders = globals()[ders_name]

        # ders günü sayısını hesapla
        count = ders_count(start_date, end_date)-1

        # Toplam ders sayısı ve öğrencilerin geldiği toplam gün sayısı veriler
        total_lessons = count*lesson_students
        attended_days = ders.query.with_entities(ders.student_no).count()

        # Yüzdelik hesaplama
        attendance_percentage = (attended_days / total_lessons) * 100

        # Pasta grafiği için gerekli verileri hazırla
        labels = ['Gelmeyenler', 'Gelenler']
        colors = ['red', 'green']
        sizes = [100 - attendance_percentage, attendance_percentage]

        return render_template("course.html", teacher=teacher,courses=teachers_lessons,  lesson_name=lesson_name, labels=labels, colors=colors, sizes=sizes)
    

@app.route("/calendar_detail")
def calendar_detail():
    if 'nick' in session:
        nick = session['nick'] 
        teacher = Teacher.query.filter_by(nick=nick).first()
        teacher_id = teacher.id
        teachers_lessons = db.session.query(Lesson.lesson_name, Lesson.period).join(Teacher).filter(Lesson.teacher_id == teacher_id).all()

        ders_name = app.config['DERS']
        ders = globals()[ders_name]
   
        date_str = request.url
        date_parts = date_str.split("=")[1].split("%2F")  # "D/M/Y" bölümünü ayır
        print(date_parts)
        day = date_parts[0]
        month = date_parts[1]
        year = date_parts[2]

        date = f"{year}-{month}-{day}"  # YYYY-MM-DD formatında tarih oluştur
        
        # lesson_id'sine göre öğrencilerin student_no değerlerini tutacak bir liste oluştur
        lesson_id = get_lesson_id(ders_name)
        all_students = []
        empty_students = []  # Gelmeyen öğrenci listesi

        # Öğrencileri sorgula ve student_no değerlerini liste içine ekle
        lesson_students = LessonStudent.query.filter_by(lesson_id=lesson_id).all()
        for lesson_student in lesson_students:
            student = Student.query.get(lesson_student.student_id)
            all_students.append(student.student_no)

        student_nos = []
        # Kayıtları sorgula ve student_no değerlerini liste içine ekle
        records = ders.query.filter_by(date=date).all()
        for record in records:
            student_nos.append(record.student_no)
            
        # Öğrenci bilgilerini ders tablosundan al
        student_info = []
        for student_no in student_nos:
            record = ders.query.filter_by(student_no=student_no).first()
            student_info.append({
                'student_no': record.student_no,
                'student_name': record.student_name,
                'student_surname': record.student_surname
            })

        for student_no in all_students:
            if student_no not in student_nos:
                empty_students.append(student_no)

        # Öğrenci bilgilerini Student tablosundan al
        student_empty_info = []
        for student_no in empty_students:
            record = Student.query.filter_by(student_no=student_no).first()
            student_empty_info.append({
                'student_no': record.student_no,
                'student_name': record.student_name,
                'student_surname': record.student_surname
            })

        return render_template("calendar_detail.html", teacher=teacher,courses=teachers_lessons, student_info=student_info, student_empty_info=student_empty_info)


if __name__ == "__main__":
    
    app.debug = True
    app.run()
