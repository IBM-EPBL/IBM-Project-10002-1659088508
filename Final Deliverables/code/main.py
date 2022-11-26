from flask import Flask, render_template, request, session
@app.route("/")
@app.route("/login", methods=['POST', 'GET'])
def login():
    return render_template('login.html')


@app.route("/register", methods=['POST', 'GET'])
def register():
    return render_template('registration.html')


@app.route("/add", methods=['POST', 'GET'])
def add():
    return render_template('add.html')



@app.route("/changedetails", methods=['POST', 'GET'])
def changedetails():
    return render_template('changedetails.html')


@app.route("/dashboard",methods=['POST','GET'])
def dashboard():
    return render_template('dashboard.html')


@app.route("/dispexpense", methods=['POST', 'GET'])
def dispexpense():
        return render_template('dispexpense.html')


@app.route('/logout')
def logout():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)