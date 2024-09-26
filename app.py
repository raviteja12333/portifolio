from flask import Flask, redirect, render_template, request, url_for # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:admin@localhost/student'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Student model corresponding to the 'student' table
class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'



# Define routes
@app.route('/')
def home():
    students = Student.query.all()  # Fetch all students from the database
    return render_template('students.html', students=students)


@app.route('/add', methods=['POST'])
def add():
    formName= request.form['name']
    formAge= request.form['age']
    formCourse= request.form['course']

    newStudent= Student(name=formName,age=formAge,course=formCourse)
    db.session.add(newStudent)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/edit/<int:id>',methods=['POST','GET'])
def edit_student(id):
    std =Student.query.get_or_404(id)
    if request.method == 'POST':
        std.name = request.form['name']
        std.age = request.form['age']
        std.course= request.form['course']
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html',student=std)

@app.route('/delete/<int:id>',methods=['POST'])
def delete_student(id):
    std =Student.query.get_or_404(id)
    db.session.delete(std)
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
