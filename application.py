from flask import Flask, render_template, url_for, request, redirect, flash
from markupsafe import escape
import mysql.connector

#creating an object for class Flask to act as WSGI
app = Flask(__name__)

#for flash messages and data encription
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#creaing database connectivity
mydb=mysql.connector.connect(
    host="localhost",
    username="root",
    password="reshma123",
    database="studdata"
)
mycursor=mydb.cursor(dictionary=True)

#registration page
@app.route("/", methods= ['GET','POST'])
def index():
    return render_template('studentreg.html')

@app.route("/registration", methods=['POST'])    
def viewregistration():
    Firstname = escape(request.form['Firstname'])
    Lastname = escape(request.form['Lastname'])
    Branch = escape(request.form['Branch'])
    Email = escape(request.form['Email'])
    Phonenumber = escape(request.form['Phonenumber'])
    Address = escape(request.form['Address'])

    sql = """INSERT INTO Students (Firstname, Lastname, Branch, Email, Phonenumber, Address)
    VALUES(%s,%s, %s, %s, %s, %s)"""
    value = (Firstname, Lastname, Branch, Email, Phonenumber, Address)

    mycursor.execute(sql, value)
    mydb.commit()
    
    return render_template('login.html')

@app.route("/registration/adminlogin", methods=['POST'])
def adminlogin():
    
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password =='test@123':
            return viewstudent()

        else:
            message = "Invalid credentials, please check!"
            return render_template('login.html', message=message)    


@app.route("/registration/viewstudent")
def viewstudent():
    #fetching data from db
    mycursor.execute("SELECT * FROM Students")
    students = mycursor.fetchall()
    return render_template('studview.html',students=students)

@app.route("/registration/editstudent/<id>", methods=['GET','POST'])
def editstudent(id):

    ID = int(escape(id))
    if request.method =='GET':
        return show_editform(ID)

    Firstname = escape(request.form['Firstname'])
    Lastname = escape(request.form['Lastname'])
    Branch = escape(request.form['Branch'])    
    Email = escape(request.form['Email'])    
    Phonenumber = escape(request.form['Phonenumber'])    
    Address = escape(request.form['Address'])    

    sql = """UPDATE Students
    SET Firstname = %s,
    Lastname = %s,
    Branch = %s,
    Email = %s,
    Phonenumber = %s,
    Address = %s
    WHERE ID = %s"""

    val = (Firstname,Lastname, Branch, Email, Phonenumber,Address,ID)
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for('viewstudent'))
  

def show_editform(ID):

    sql = "SELECT * FROM Students WHERE ID = %s"
    value = (ID,)
    mycursor.execute(sql,value)
    myresult = mycursor.fetchone()
    return render_template('edit_student.html', student = myresult)        


@app.route("/registration/deletestudent/<id>", methods=['GET','POST'])
def deletestudent(id):

    ID = int(escape(id))
    sql = """DELETE FROM Students where ID = %s"""
    val = (ID)
    mycursor.execute(sql,(val,))
    mydb.commit()

    if mycursor.rowcount > 0:
       message = "Employee Records deleted successfully."
       flash(message)

    else:
        message = None 

    return redirect(url_for('viewstudent'))    

