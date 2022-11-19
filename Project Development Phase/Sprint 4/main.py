import re
import ibm_db
from flask import Flask, render_template, request, session
global table
global userid
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def insertTableData(conn, username, email, password, age, profession, table):
    table = 'no'
    sql = "INSERT INTO usersdetails(username,email,password,age,profession,table) VALUES ('{}','{}','{}','{}','{}','{}')".format(
        username, email,
        password, age, profession, table)
    out = ibm_db.exec_immediate(conn, sql)
    print('Number of affected rows : ', ibm_db.num_rows(out), "\n")


def conditionCheak():
    username = session.get('username', None)
    sql = "SELECT table FROM usersdetails WHERE username=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, username)
    ibm_db.execute(stmt)
    out = ibm_db.fetch_assoc(stmt)
    print("out cheak condition ->", out)
    value = out['TABLE']
    session['tablequery'] = value


def createNewTableForUser(userid):
    sqlc = "CREATE TABLE userid=? (date DATE , expensename VARCHAR(22),expenseamount INTEGER,paymode VARCHAR(24),category VARCHAR(22))"
    stmt = ibm_db.prepare(conn, sqlc)
    ibm_db.bind_param(stmt,0, userid)
    createtable = ibm_db.execute(stmt)
    session['createtable']=createtable


def updateTabletable(table):
    username = session.get('username', None)
    sql1 = "UPDATE usersdetails SET TABLE=? WHERE USERNAME=?"
    stmt = ibm_db.prepare(conn, sql1)
    ibm_db.bind_param(stmt, 1, table)
    ibm_db.bind_param(stmt, 2, username)
    ibm_db.execute(stmt)


def updateTableData(username, password, email, profession):
    sql = "SELECT * FROM usersdetails  WHERE username =? AND password=?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, username)
    ibm_db.bind_param(stmt, 2, password)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print(account)
    if account:
        username = account['USERNAME']
        sql1 = "UPDATE usersdetails SET EMAIL=?,PROFESSION=? WHERE USERNAME=?"
        stmt = ibm_db.prepare(conn, sql1)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, profession)
        ibm_db.bind_param(stmt, 3, username)
        ibm_db.execute(stmt)


def displayDetails(userid):
    sql1 = "SELECT username, email, age, profession FROM usersdetails WHERE username=?"
    stmt_db = ibm_db.prepare(conn, sql1)
    ibm_db.bind_param(stmt_db, 1, userid)
    ibm_db.execute(stmt_db)
    accounts = ibm_db.fetch_assoc(stmt_db)
    return accounts


try:
    conn = ibm_db.connect(
        "DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=bkf39982;PWD=tnRiAWwYZEwQOptp;",
        "", "")
    print("Db connected")
except:
    print("Error")

app = Flask(__name__)
app.secret_key = 'aa'


@app.route("/")
@app.route("/login", methods=['POST', 'GET'])
def login():
    msg = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = "SELECT * FROM usersdetails  WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)

        table = account['TABLE']
        userid = account['USERNAME']

        session['username'] = userid

        sql1 = "SELECT username, email, age, profession FROM usersdetails WHERE username=?"
        stmt_db = ibm_db.prepare(conn, sql1)
        ibm_db.bind_param(stmt_db, 1, userid)
        ibm_db.execute(stmt_db)
        accounts = ibm_db.fetch_assoc(stmt_db)

        if account:
            session['id'] = account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in successfully !'
            return render_template('dashboard.html', accounts=accounts)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        profession = request.form['profession']
        username = request.form['username']
        sql = "SELECT * FROM usersdetails WHERE username =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            insertTableData(conn, username, email, password, age, profession, table)
            message = Mail(
                from_email='admin@pta.com',
                to_emails=current_user.user_json['EMAIL'],
                subject='Low Balance !!',
                html_content='<strong>and easy to do anywhere,</strong>')
            return render_template('login.html')
    return render_template('registration.html')


@app.route("/add", methods=['POST', 'GET'])
def add():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        date = request.form['date']
        expensename = request.form['expensename']
        expenseamount = request.form['expenseamount']
        paymode = request.form['paymode']
        category = request.form['category']

        sql = "SELECT * FROM usersdetails  WHERE username =? AND password=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            userids = account['USERNAME']
            sqli = "INSERT INTO expenses(username,date,expensename,expenseamount,paymode,category) VALUES ('{}','{}','{}','{}','{}','{}')".format(
                username,
                date, expensename, expenseamount, paymode, category)
            out = ibm_db.exec_immediate(conn, sqli)
            accounts = displayDetails(userids)
            return render_template('dashboard.html', accounts=accounts)
    return render_template('add.html')

    if request.method == 'GET':
        return render_template('dashboard.html', accounts=accounts)


@app.route("/changedetails", methods=['POST', 'GET'])
def changedetails():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        profession = request.form['profession']
        updateTableData(username, password, email, profession)
        return render_template('login.html')

    return render_template('changedetails.html')


@app.route("/dashboard",methods=['POST','GET'])
def dashboard():
    username = session.get('username',None)
    accounts = displayDetails(username)
    return render_template('dashboard.html',accounts=accounts)


@app.route("/dispexpense", methods=['POST', 'GET'])
def dispexpense():
     if request.method == 'GET':
        user = session.get('username', None)
        print(user)
        expensedetails = []
        sql = "SELECT CHAR(DATE(date),USA) as date, expensename, expenseamount, paymode, category FROM expenses WHERE username=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, user)
        ibm_db.execute(stmt)
        details = ibm_db.fetch_assoc(stmt)
        while details != False:
            expensedetails.append(details)
            details = ibm_db.fetch_assoc(stmt)

        print(expensedetails)

        sql2 = "SELECT SUM(expenseamount) AS TOTALVAL FROM expenses WHERE username = ?"
        stmt2 = ibm_db.prepare(conn, sql2)
        ibm_db.bind_param(stmt2, 1, user)
        ibm_db.execute(stmt2)
        totalexpense = ibm_db.fetch_assoc(stmt2)
        print(totalexpense)
        return render_template('dispexpense.html', expensedetails=expensedetails, totalexpense=totalexpense['TOTALVAL'])


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
