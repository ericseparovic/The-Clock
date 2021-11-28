from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import os
from services import auth
from services import personal
import time

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

            #Si el usuario personal intenta iniciar sesion en el login administrador se redirecciona al login personal
            try:
                session['logged_in'] = True
                session['idCompany'] = data_company['idCompany']
                session['nameCompany'] = data_company['nameCompany']
                session['idCompany'] = data_company['idCompany']
                session['error'] = False

                return redirect(url_for('home_company'))
            except KeyError:
                return render_template('login_personal.html', error=error)


        if response.status_code == 412:
            error = response.text
            return render_template('login_company.html', error=error)

        if response.status_code == 409:
            error = response.text
            return render_template('login_company.html', error=error)

    return render_template('login_company.html')


#Login personal
@app.route('/login_personal', methods=["GET", "POST"])
def login_personal():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        response = auth.login(email, password)

        if response.status_code == 200:

            data_personal = response.json()

            #Si el usuario administrador intenta iniciar sesion el el usuario personal se redirecciona al login administrador
            try:
                print(data_personal)
                session['logged_in'] = True
                session['idPersonal'] = data_personal['idPersonal']
                session['namePersonal'] = data_personal['namePersonal']
                session['idPersonal'] = data_personal['idPersonal']
                idPersonal = data_personal['idPersonal']
                session['error'] = False

                return redirect(url_for('home_personal', idPersonal=idPersonal))
            except KeyError:
                return render_template('login_company.html', error=error)

        if response.status_code == 412:
            error = response.text
            return render_template('login_personal.html', error=error)

        if response.status_code == 409:
            error = response.text
            return render_template('login_personal.html', error=error)

    return render_template('login_personal.html')

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
    return redirect(url_for('login_company'))
    

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
            idCompany = session['idCompany']
            return render_template('register_personal.html', nameCompany=nameCompany, idCompany=idCompany)
        return redirect(url_for('login_company'))

    return redirect(url_for('login_company'))





#Lista de empleados
@app.route('/list_personal', methods=["POST", "GET"])
def list_personal():
    if request.method == 'GET':
        if 'logged_in' in session:
            nameCompany = session['nameCompany']
            idCompany = session['idCompany']
            response = personal.get_all_personal(idCompany)
            all_personal = response.json()
            code = response.status_code

            return render_template('list_personal.html', nameCompany=nameCompany, idCompany=idCompany, all_personal=all_personal, code=code)
        return redirect(url_for('login_company'))

    return redirect(url_for('login_company'))


@app.route('/delete_personal/<idPersonal>', methods=["GET"])
def delete_personal(idPersonal):
    if 'logged_in' in session:
        response = personal.delete_personal(idPersonal)
        
        if response.status_code == 200:
            #Cargar list_personal
            return redirect(url_for('list_personal'))

        
        if response.status_code == 412:
            #Mostrar error
            nameCompany = session['nameCompany']
            idCompany = session['idCompany']
            response = personal.get_all_personal(idCompany)
            all_personal = response.json()
            error = "No se pudo eliminar"
            return render_template('list_personal.html', nameCompany=nameCompany, idCompany=idCompany, all_personal=all_personal, error=error)

    return redirect(url_for('login_company'))


#Endopoint actualizar datos
@app.route('/update_personal/<idPersonal>', methods=["GET", "POST"])
def update_personal(idPersonal):
    if 'logged_in' in session:
        nameCompany = session['nameCompany']
        idCompany = session['idCompany']

        if request.method == 'GET':
                dataPersonal = personal.get_personal(idPersonal)
                dataPersonal = dataPersonal.json()
                print(dataPersonal)
                return render_template('update_personal.html', nameCompany=nameCompany, idCompany=idCompany, idPersonal=idPersonal, dataPersonal=dataPersonal[0])

        if request.method == 'POST':

            document = request.form['document']
            name = request.form['name']
            lastname = request.form['lastname']
            gender = request.form['gender']
            birthday = request.form['birthday']
            tel = request.form['tel']
            address = request.form['address']
            email = request.form['email']

            response = personal.update_personal(document, name, lastname, gender, birthday, tel, address, idPersonal, email)
            dataPersonal = personal.get_personal(idPersonal)

            dataPersonal = dataPersonal.json()
            if response.status_code == 200:
                error = response.text
                return render_template('update_personal.html', nameCompany=nameCompany, idCompany=idCompany, idPersonal=idPersonal, error=error, dataPersonal=dataPersonal[0])
    
            if response.status_code == 409:
                error = response.text
                return render_template('update_personal.html', nameCompany=nameCompany, idCompany=idCompany, idPersonal=idPersonal, error=error, dataPersonal=dataPersonal)

            if response.status_code == 412:
                error = response.text
                return render_template('update_personal.html', nameCompany=nameCompany, idCompany=idCompany, idPersonal=idPersonal, error=error, dataPersonal=dataPersonal)
    return redirect(url_for('login_company'))


#Endopoint asignar horarios
@app.route('/assign_schedule/<idPersonal>', methods=["GET", "POST"])
def assign_schedule(idPersonal):
    if 'logged_in' in session:
        nameCompany = session['nameCompany']
        idCompany = session['idCompany']

        if request.method == 'GET':
                dataPersonal = personal.get_personal(idPersonal)
                dataPersonal = dataPersonal.json()
                return render_template('assign_schedule.html', nameCompany=nameCompany, idCompany=idCompany, idPersonal=idPersonal, dataPersonal=dataPersonal[0])

        if request.method == 'POST':

            workStart = request.form['workStart']
            workEnd = request.form['workEnd']


            response = personal.assign_schedule(workStart, workEnd, idPersonal)
            dataPersonal = personal.get_personal(idPersonal)
            dataPersonal = dataPersonal.json()
            if response.status_code == 200:
                error = response.text
                return render_template('assign_schedule.html', nameCompany=nameCompany, idCompany=idCompany, idPersonal=idPersonal, error=error, dataPersonal=dataPersonal[0])
    
            if response.status_code == 409:
                error = response.text
                return render_template('assign_schedule.html', nameCompany=nameCompany, idCompany=idCompany, idPersonal=idPersonal, error=error, dataPersonal=dataPersonal)
            
            if response.status_code == 412:
                error = response.text
                return render_template('assign_schedule.html', nameCompany=nameCompany, idCompany=idCompany, idPersonal=idPersonal, error=error, dataPersonal=dataPersonal)
    return redirect(url_for('login_company'))

#Endopoint asignar libres
@app.route('/assign_days_off/<idPersonal>', methods=["GET", "POST"])
def assign_days_off(idPersonal):
    if 'logged_in' in session:
        nameCompany = session['nameCompany']
        idCompany = session['idCompany']
        responseAbsence = personal.get_all_absence(idPersonal)
        print(responseAbsence.text)
        all_absence = responseAbsence.json()
        if request.method == 'GET':
                dataPersonal = personal.get_personal(idPersonal)
                dataPersonal = dataPersonal.json()

                return render_template('assign_days_off.html', nameCompany=nameCompany, idCompany=idCompany, idPersonal=idPersonal, dataPersonal=dataPersonal[0], all_absence=all_absence)

        if request.method == 'POST':

            startDate = request.form['startDate']
            endDate = request.form['endDate']
            reason = request.form['reason']


            response = personal.assign_days_off(startDate, endDate, reason, idPersonal)
            dataPersonal = personal.get_personal(idPersonal)
            dataPersonal = dataPersonal.json()


            if response.status_code == 200:
                error = response.text
                return render_template('assign_days_off.html', nameCompany=nameCompany, idCompany=idCompany, idPersonal=idPersonal, error=error, dataPersonal=dataPersonal[0], all_absence=all_absence)
    
            if response.status_code == 409:
                error = response.text
                return render_template('assign_days_off.html', nameCompany=nameCompany, idCompany=idCompany, idPersonal=idPersonal, error=error, dataPersonal=dataPersonal, all_absence=all_absence)
            
            if response.status_code == 412:
                error = response.text
                return render_template('assign_days_off.html', nameCompany=nameCompany, idCompany=idCompany, idPersonal=idPersonal, error=error, dataPersonal=dataPersonal, all_absence=all_absence)
    return redirect(url_for('login_company'))



#Endopoint registar marcas
@app.route('/register_mark/<idPersonal>', methods=["GET", "POST"])
def register_mark(idPersonal):
    if 'logged_in' in session:
        nameCompany = session['nameCompany']
        idCompany = session['idCompany']

        if request.method == 'GET':
                dataPersonal = personal.get_personal(idPersonal)
                dataPersonal = dataPersonal.json()
                return render_template('register_mark.html', nameCompany=nameCompany, idCompany=idCompany, idPersonal=idPersonal, dataPersonal=dataPersonal[0])

        if request.method == 'POST':

            date = request.form['date']
            workStart = request.form['workStart']
            workEnd = request.form['workEnd']

            response = personal.register_mark(date, workStart, workEnd, idPersonal)
            dataPersonal = personal.get_personal(idPersonal)
            dataPersonal = dataPersonal.json()

            if response.status_code == 200:
                error = response.text
                return render_template('register_mark.html', nameCompany=nameCompany, idCompany=idCompany, idPersonal=idPersonal, error=error, dataPersonal=dataPersonal[0])
    
            if response.status_code == 409:
                error = response.text
                return render_template('register_mark.html', nameCompany=nameCompany, idCompany=idCompany, idPersonal=idPersonal, error=error, dataPersonal=dataPersonal)
            
            if response.status_code == 412:
                error = response.text
                return render_template('register_mark.html', nameCompany=nameCompany, idCompany=idCompany, idPersonal=idPersonal, error=error, dataPersonal=dataPersonal)
    return redirect(url_for('login_company'))


#Endpont home
@app.route('/home_company', methods=["GET", "POST"])
def home_company():
    if 'logged_in' in session:
        nameCompany = session['nameCompany']
        idCompany = session['idCompany']

        #Obtiene cantidad de faltas del dia
        absences = personal.get_absences(idCompany)
        absences = absences.json()
        countAbsences = len(absences)

        #Obtiene cantidad de llegadas tardes del dia
        late_arrivals = personal.get_late_arrivals(idCompany)
        late_arrivals = late_arrivals.json()
        count_late_arrivals = len(late_arrivals)


        #Obtiene cantidad con salida anticipada
        early_departure = personal.get_early_departure(idCompany)
        early_departure = early_departure.json()
        count_early_departure = len(early_departure)
        
        #Obtiene cantidad de asistencias del dia
        assists = personal.get_assists(idCompany)
        assists = assists.json()
        count_assists = len(assists)

        if request.method == 'GET':
                return render_template('home_company.html', nameCompany=nameCompany, idCompany=idCompany, countAbsences = countAbsences, count_late_arrivals=count_late_arrivals, count_early_departure=count_early_departure, count_assists=count_assists)

    return redirect(url_for('login_company'))
        

#Endpont home
@app.route('/home_personal', methods=["GET", "POST"])
def home_personal():
    if 'logged_in' in session:
        namePersonal = session['namePersonal']
        idPersonal = session['idPersonal']
        error = session['error']
        print(error)
        if request.method == 'GET':
                return render_template('home_personal.html', namePersonal=namePersonal, idPersonal=idPersonal, error=error)

    return render_template('login_personal.html')


#Elimina dias libres
@app.route('/delete_absence/<idPersonal>/<idAbsence>', methods=["GET"])
def delete_absence(idPersonal, idAbsence):
    if 'logged_in' in session:
        response = personal.delete_absence(idAbsence)
        
        if response.status_code == 200:
            return redirect(url_for('assign_days_off', idPersonal=idPersonal))
        else:
            
            return redirect(url_for('assign_days_off', idPersonal=idPersonal))
    return redirect(url_for('login_company'))




#Lista de empleados
@app.route('/report', methods=["POST", "GET"])
def report():
    if 'logged_in' in session:
        nameCompany = session['nameCompany']
        idCompany = session['idCompany']

        if request.method == 'GET':
            return render_template('report.html', nameCompany=nameCompany, idCompany=idCompany)
        
        if request.method == 'POST':
            startDate = request.form['startDate']
            endDate = request.form['endDate']
            document = request.form['document']
            response = personal.get_marks(startDate, endDate, document, idCompany)
            if response.status_code == 200:
                marks = response.json()
                return render_template('report.html', nameCompany=nameCompany, idCompany=idCompany, marks=marks, code=response.status_code)
            else:
                return render_template('report.html', nameCompany=nameCompany, idCompany=idCompany, code=response.status_code, error= response.text)
    return redirect(url_for('login_company'))

#Ingrsar marca de entrada
@app.route('/mark_start/<idPersonal>', methods=["POST", "GET"])
def mark_start(idPersonal):
    if 'logged_in' in session:
        response = personal.post_mark_start(idPersonal)
        if response.status_code == 200:
            session['error'] = response.text

            return redirect(url_for('home_personal'))

        if response.status_code == 404:
            session['error'] = 'No se pudo ingresar marca 404'

            return redirect(url_for('home_personal'))
        
        if response.status_code == 412:
            session['error'] = 'No se pudo ingresar marca 412'

            return redirect(url_for('home_personal'))
    
    return redirect(url_for('login_personal'))

#Ingrsar marca de salida
@app.route('/mark_end/<idPersonal>', methods=["POST", "GET"])
def mark_end(idPersonal):
    if 'logged_in' in session:
        response = personal.post_mark_end(idPersonal)


        if response.status_code == 200:
            session['error'] = response.text

            return redirect(url_for('home_personal'))
        
        if response.status_code == 404:
            session['error'] = 'No se pudo ingresar marca 404'

            return redirect(url_for('home_personal'))
        
        if response.status_code == 412:
            session['error'] = 'No se pudo ingresar marca 412'

            return redirect(url_for('home_personal'))
    
    return redirect(url_for('login_personal'))

if __name__ == '__main__':
    app.debug = True
    app.run(port=5005)

