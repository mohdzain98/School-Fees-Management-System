#!/usr/bin/python3
import os

from flask import Flask, render_template, request, redirect, url_for

from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Geeky@Zain98'
app.config['MYSQL_DB'] = 'feemanagement'

mysql = MySQL(app)




@app.route("/", methods=['GET'])
def index():

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM sessions")
    sessions = cursor.fetchall()

    return render_template("index.html", sessions=sessions)

@app.route("/insert", methods=['GET'])
def insert():

    cursor = mysql.connection.cursor()

    cursor.execute("SELECT * FROM sessions")
    sessions = cursor.fetchall()


    return render_template("insert.html", sessions=sessions)
def covert_rn(str):
    if(str=='first'):
        return '1'
    if(str=='sec0nd'):
        return '2'
    if(str=='third'):
        return '3'
    if(str=='fourth'):
        return '4'
    if(str=='fifth'):
        return '5'
    if(str=='sixth'):
        return '6'
    if(str=='seventh'):
        return '7'
    if(str=='eighth'):
        return '8'
    if(str=='ninth'):
        return '9'
    if(str=='tenth'):
        return '10'
    if(str=='eleven'):
        return '11'
    if(str=='twelve'):
        return '12'
    
def view_update(grade):
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT * from students INNER JOIN fee ON students.roll_no = fee.roll_no and students.session=fee.class 
                   where students.session=%s""",(grade,))
    students = cursor.fetchall()
        
    return render_template("view.html", students=students)

@app.route("/view", methods=['POST', 'GET'])
def view():

    cursor = mysql.connection.cursor()

    if request.method == "POST":
        
        name = request.form.get("name")
        fname = request.form.get("fname")
        roll_no2 = request.form.get("roll_no")
        Adhar = request.form.get("Adhar")
        session = request.form.get("session")
        total_fee = request.form.get("total_fee")
        sub_fee = request.form.get("sub_fee")
        rem_fee = int(total_fee) - int(sub_fee)
        roll_no = covert_rn(session) + "-" + str(roll_no2)
        
        cursor.execute("INSERT into students (name, fname, Adhar,roll_no,session) VALUES (%s, %s, %s, %s,%s)",
                (name,fname,Adhar,roll_no,session))

        cursor.execute("INSERT into fee (total_fee, sub_fee, rem_fee, roll_no,class) VALUES (%s, %s, %s, %s, %s)",
                (total_fee,sub_fee,rem_fee,roll_no,session))
        
        mysql.connection.commit()

        # Get all records again
        cursor.execute("SELECT * from students INNER JOIN fee ON students.roll_no = fee.roll_no and students.session=fee.class")
        students = cursor.fetchall()
        
        return render_template("view.html", students=students)
    else:
        cursor.execute("SELECT * from students INNER JOIN fee ON students.roll_no = fee.roll_no and students.session=fee.class")
        students = cursor.fetchall()
        
        return render_template("view.html", students=students)

@app.route("/all_session", methods=['POST', 'GET'])
def all_session():

    cursor = mysql.connection.cursor()

    if request.method == "POST":
        
        session = request.form.get("session")
        
        
        cursor.execute("INSERT into sessions (title) VALUES (%s)",
                (session,))
        
        mysql.connection.commit()

        # Get all records again
        cursor.execute("SELECT sessions.title, COUNT(distinct students.roll_no), sum(fee.total_fee), sum(fee.sub_fee), sum(fee.rem_fee) FROM students INNER JOIN fee on students.roll_no = fee.roll_no RIGHT JOIN sessions ON students.session = sessions.title GROUP BY sessions.title ORDER BY sessions.id")
        sessions = cursor.fetchall()
        
        return render_template("all_session.html", sessions=sessions)
    else:

        cursor.execute("SELECT sessions.title, COUNT(distinct students.roll_no), sum(fee.total_fee), sum(fee.sub_fee), sum(fee.rem_fee) FROM students INNER JOIN fee on students.roll_no = fee.roll_no RIGHT JOIN sessions ON students.session = sessions.title GROUP BY sessions.title ORDER BY sessions.id")
        sessions = cursor.fetchall()
        
        return render_template("all_session.html", sessions=sessions)


@app.route("/search", methods=['POST','GET'])
def search():

    cursor = mysql.connection.cursor()    

    if request.method == "POST":
        
        session = request.form.get("session")

        cursor.execute("SELECT * from students INNER JOIN fee ON students.roll_no = fee.roll_no and students.session=fee.class where students.session = %s", (session,))
        students = cursor.fetchall()
        
        return render_template("view.html", students=students)

    else:

        return "Please search from Home Tab"


@app.route("/update/<roll_no>/", methods=['POST','GET'])
def update(roll_no):

    cursor = mysql.connection.cursor()

    if request.method=="POST":
        name = request.form.get("name")
        fname = request.form.get("fname")
        roll_no2 = request.form.get("roll_no")
        Adhar = request.form.get("Adhar")
        session = request.form.get("class")
        total_fee = request.form.get("total_fee")
        sub_fee = request.form.get("sub_fee")
        rem_fee = int(total_fee) - int(sub_fee)
        a = str(roll_no)
     

        cursor.execute("Update students SET name = %s, fname =%s, Adhar =%s, roll_no = %s where roll_no=%s",
                    (name,fname,Adhar,roll_no2,roll_no))

        cursor.execute("Update fee SET total_fee = %s, sub_fee =%s, rem_fee =%s, roll_no = %s where roll_no=%s",
                    (total_fee,sub_fee,rem_fee,roll_no2,roll_no))

        mysql.connection.commit()

        return redirect(url_for('view'))
    else:
        cursor.execute("SELECT * from students INNER JOIN fee ON students.roll_no = fee.roll_no and students.session=fee.class WHERE students.roll_no = %s", (roll_no,))
        stud = cursor.fetchone()

        return render_template("update.html", stud=stud, roll_no=roll_no)

@app.route("/delete/<roll_no>/")
def delete(roll_no):
    print(roll_no)
    cursor = mysql.connection.cursor()
    query="SELECT * FROM students WHERE roll_no = %s"
    cursor.execute(query, (roll_no,))
    stud = cursor.fetchone()
    if stud is None:
        return "No record found by Roll No = " + str(roll_no) +". Kindly go back to <a href='/view'> View All Students </a>"
    else:
        cursor.execute("DELETE FROM students WHERE roll_no =%s",(roll_no,))
        cursor.execute("DELETE FROM fee WHERE roll_no =%s",(roll_no,))

        mysql.connection.commit()
        return redirect(url_for('view'))


if __name__ == "__main__":
    app.run(debug=True)