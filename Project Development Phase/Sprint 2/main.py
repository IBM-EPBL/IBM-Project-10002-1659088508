from flask import Flask, request, json,url_for
import ibm_db

dictionary = {}


def printTableData(conn):
    sql = "SELECT * FROM userdetails"
    out = ibm_db.exec_immediate(conn, sql)
    document = ibm_db.fetch_assoc(out)
    while document != False:
        dictionary.update({document['USERNAME']: document['PASSWORD']})
        document = ibm_db.fetch_assoc(out)


def insertTableData(conn, username, email, password, age, profession):
    sql = "INSERT INTO userdetails(username,email,password,age,profession) VALUES ('{}','{}','{}','{}','{}')".format(
        username, email,
        password, age, profession)
    out = ibm_db.exec_immediate(conn, sql)
    print('Number of affected rows : ', ibm_db.num_rows(out), "\n")


def updateTableData(email, password, profession):
    sql = "UPDATE userdetails SET (username,email,password)=('{}','{}','{}')".format(email, password, profession)

    out = ibm_db.exec_immediate(conn, sql)
    print('Number of affected rows : ', ibm_db.num_rows(out), "\n")


try:
    conn = ibm_db.connect(
        "DATABASE=bludb;HOSTNAME=98538591-7217-4024-b027-8baa776ffad1.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT=30875;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;PROTOCOL=TCPIP;UID=bkf39982;PWD=tnRiAWwYZEwQOptp;",
        "", "")
    print("Db connected")

except:
    print("Error")

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        printTableData(conn)
        username = request.form['username']
        password = request.form['password']
        if dictionary[username] == password:
            return render_template('dashboard.html')
    return render_template('login.html')


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']
        profession = request.form['profession']
        name = request.form['username']
        insertTableData(conn, name, email, password, age, profession)
        # printTableData(conn)
        return render_template('login.html')
    return render_template('registration.html')


@app.route("/add", methods=['POST', 'GET'])
def add():
    return render_template('add.html')



# deleteTableData(conn,6)
# printTableData(conn)
# print(dictionary)


if __name__ == "__main__":
    app.run(debug=True)