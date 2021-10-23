from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from werkzeug.wrappers import response
from services import auth

app = Flask(__name__)




#Login empresas
@app.route('/', methods=["GET", "POST"])
def login_company():
    if request.method == 'POST':
        print('holdsfds')

        return render_template('login_company.html')
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







#Login empleados
@app.route('/login_personal')
def login_personal():
    return render_template('login_personal.html')




#Ingresar empleado
@app.route('/register_personal')
def register_personal():
    return render_template('register_personal.html')



#Lista de empleados
@app.route('/list_of_employees')
def list_of_employees():
    return render_template('list_of_employees.html')




if __name__ == '__main__':
    app.debug = True
    app.run(port=5005)