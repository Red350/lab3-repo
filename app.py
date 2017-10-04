from flask import Flask, request, url_for, render_template
from flask_mysqldb import MySQL

mysql = MySQL()
app = Flask(__name__)
# My SQL Instance configurations 
# Change the HOST IP and Password to match your instance configurations
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'visiblepassword'
app.config['MYSQL_DB'] = 'studentbook'
app.config['MYSQL_HOST'] = '35.195.5.225'
mysql.init_app(app)

# The first route to access the webservice from http://external-ip:5000/ 
#@pp.route("/add") this will create a new endpoints that can be accessed using http://external-ip:5000/add
@app.route("/")
def hello(): # Name of the method
    cur = mysql.connection.cursor() #create a connection to the SQL instance
    cur.execute('''SELECT * FROM students''') # execute an SQL statment
    rv = cur.fetchall() #Retreive all rows returend by the SQL statment
    return str(rv)      #Return the data in a string format

@app.route("/add")
def add():
    student_name = request.args.get('studentname', '')
    student_email = request.args.get('studentemail', '')
    if (student_email != '' and student_name != ''):
        conn = mysql.connection
        cur = conn.cursor() #create a connection to the SQL instance
        cur.execute('INSERT INTO students(studentName, email) VALUES("%(student_name)s", "%(student_email)s");' % locals())
        conn.commit()
        return str("Added successfully!")      #Return the data in a string format
    return str("Invalid request")      #Return the data in a string format

@app.route("/delete")
def delete():
    student_id = request.args.get('studentid', '')
    if (student_id != ''):
        conn = mysql.connection
        cur = conn.cursor() #create a connection to the SQL instance
        cur.execute('DELETE FROM students WHERE studentID = %(student_id)s;' % locals())
        conn.commit()
        return str("Deleted successfully!")      #Return the data in a string format
    return str("Invalid request")      #Return the data in a string format

@app.route("/update")
def update():
    student_id = request.args.get('studentid', '')
    student_name = request.args.get('studentname', '')
    student_email = request.args.get('studentemail', '')
    if (student_id != '' and student_name != '' and student_email != ''):
        conn = mysql.connection
        cur = conn.cursor() #create a connection to the SQL instance
        cur.execute('UPDATE students SET studentName="%(student_name)s", email="%(student_email)s" WHERE studentId=%(student_id)s;' % locals())
        conn.commit()
        return str("Updated successfully!")      #Return the data in a string format
    return str("Invalid request")      #Return the data in a string format

@app.route("/index")
def index():
    return render_template("index.html")
#return render_template(url_for('static', filename='index.html'))

if __name__ == "__main__":
        app.run(host='0.0.0.0', port='5000') #Run the flask app at port 5000


