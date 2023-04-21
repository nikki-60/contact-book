from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'Contact'

mysql = MySQL(app)

#To display
@app.route("/", methods=['GET','POST'])
def showLoginPage():
    return render_template("button.html")


@app.route("/signup", methods=['POST', 'GET'])
def submitSignup():
        print("in submitLogin")
        if request.method == "POST" and request.form['uname_txt'] and request.form['email_txt'] and request.form['password_txt'] and request.form['phno_txt']:
            print(request.form['uname_txt'])
            Uname = request.form['uname_txt']
            Email = request.form['email_txt']
            Password = request.form['password_txt']
            Phone_num = request.form['phno_txt']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO Signup VALUES ('{}','{}','{}','{}');".format(Uname, Email, Password, Phone_num))
            mysql.connection.commit()
            return redirect('/login')
        return render_template('signup.html')


@app.route("/login", methods=['POST', 'GET'])
def submitLogin():
        if request.method=='POST' and request.form['login_txt'] and request.form['password_txt']:
            Uname = request.form['login_txt']
            Password = request.form['password_txt']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM Signup WHERE Uname = '{}' AND Password = '{}';".format(Uname, Password))
            user = cursor.fetchone()
            if user:
                return redirect('/index.html')
        return render_template('login.html')
        return user


@app.route('/insert',methods=['POST'])
def insert():

    if request.method == 'POST' and request.form['id'] and request.form['name'] and request.form['number'] and request.form['email'] and request.form['address']:
        id=request.form['id']
        name = request.form['name']
        number = request.form['number']
        email = request.form['email']
        address = request.form['address']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO uinfo VALUES ('{}','{}','{}','{}','{}');".format(id,name,number,email,address))
        mysql.connection.commit()
        return redirect('/index.html')

@app.route('/index.html')
def data():

     cursor = mysql.connection.cursor()
     cursor.execute("SELECT * FROM uinfo")
     info = cursor.fetchall()
     cursor.close()
     return render_template('index.html',uinfo=info)



@app.route("/update", methods=['GET', 'POST'])
def update():
   if request.method == 'POST':
       id=request.form['id']
       name = request.form['name']
       number = request.form['number']
       email = request.form['email']
       address = request.form['address']
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute("UPDATE uinfo SET id='{}',name='{}',number='{}',email='{}',address='{}' WHERE id='{}';".format(id,name, number, email, address,id))
       mysql.connection.commit()
       return redirect('/index.html')


@app.route('/delete/<int:id>',methods=['POST','GET'])
def delete(id):
     cursor = mysql.connection.cursor()
     cursor.execute("DELETE FROM uinfo WHERE id='{}';".format(id))
     mysql.connection.commit()
     return redirect('/index.html')


if __name__ == '__main__':
    app.run(debug=True)