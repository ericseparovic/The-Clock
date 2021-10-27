from flask import Flask, request, render_template, redirect, url_for, session
import os
from services import auth
from services import personal

app = Flask(__name__)

app.config.update(SECRET_KEY=os.urandom(24))




#Login empresas
@app.route('/', methods=["GET", "POST"])
def login_company():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        response = auth.login(email, password)

        if response.status_code == 200:
            data_company = response.json()
        
            session['logged_in'] = True
            session['idCompany'] = data_company['idCompany']
            session['nameCompany'] = data_company['nameCompany']
            session['idCompany'] = data_company['idCompany']

            return redirect(url_for('home_company'))

        if response.status_code == 412:
            error = response.text
            return render_template('login_company.html', error=error)

        if response.status_code == 409:
            error = response.text
            return render_template('login_company.html', error=error)

    return render_template('login_company.html')

    

#Registro empresa
@app.route('/register_company', methods=["GET", "POST"])
def register_company():
    error = None

    if request.method == 'POST':
        name = request.form['name']
        tel = request.form['tel']
        email = request.form['email']
        password = request.form['password']
        passwordRepeat = request.form['passwordRepeat']

        response = auth.create_user(name, tel, email, password, passwordRepeat)
        
        
        if response.status_code == 412:
            error = response.text
            render_template('register_company.html', error=error)
        else:
            error = response.text
            render_template('register_company.html', error=error)
    return render_template('register_company.html', error=error)



#Home empresa
@app.route('/home_company')
def home_company():
    if 'logged_in' in session:
        nameCompany = session['nameCompany']
        return render_template('home_company.html', nameCompany=nameCompany)
    return redirect(url_for('login_company'))




#Cierra seccion del usuario
@app.route('/logout', methods=["POST", "GET"])
def logout():
    if request.method == 'GET':
        if 'idCompany' in session:
            session.clear()
            return redirect(url_for('login_company'))
        
        if 'idPersonal' in session:
            session.clear()
            return redirect(url_for('login_personal'))

    
#Registrar personal
@app.route('/register_personal', methods=["POST", "GET"])
def register_personal():
    error = None
    passwordDefault = 12345678

    if request.method == 'POST':
        document = request.form['document']
        name = request.form['name']
        lastname = request.form['lastname']
        gender = request.form['gender']
        birthday = request.form['birthday']
        tel = request.form['tel']
        address = request.form['address']
        email = request.form['email']
        idCompany = session['idCompany']
        nameCompany = session['nameCompany']

        response = personal.register_personal(document, name, lastname, gender, birthday, tel, address, email, idCompany)

        if response.status_code == 200:
    
            error = response.text

            if 'logged_in' in session:

                return render_template('register_personal.html', nameCompany=nameCompany, error=error)
            render_template('register_personal.html', error=error, passwordDefault=passwordDefault, nameCompany=nameCompany)
        else:
            error = response.text

            return render_template('register_personal.html', error=error, passwordDefault=passwordDefault, nameCompany=nameCompany)

    if request.method == 'GET':
        if 'logged_in' in session:
            nameCompany = session['nameCompany']
            return render_template('register_personal.html', nameCompany=nameCompany)
        return redirect(url_for('login_company'))

    return redirect(url_for('login_company'))





#Login empleados
@app.route('/login_personal')
def login_personal():
    return render_template('login_personal.html')








#Lista de empleados
@app.route('/list_of_employees')
def list_of_employees():
    return render_template('list_of_employees.html')



if __name__ == '__main__':
    app.debug = True
    app.run(port=5005)