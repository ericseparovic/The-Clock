from flask import Flask, json, request, render_template, redirect, url_for, session, jsonify
from flask.wrappers import Response
from services import auth
from services import company
from services import personal
from services import schedule
from services import mark
from services import absences
from services import notification
from datetime import datetime


import os

app = Flask(__name__)

app.config.update(SECRET_KEY=os.urandom(24))


#Se ejecuta al registrar la empresa, se guarda los datos del usuario en la tabla usuarios y se guarda los datos de la empresa en la tabla empresas
@app.route('/signup', methods=["POST", "GET"])
def signup():

    if request.method == 'POST':
        date_company = request.get_json()

        name = date_company['name']
        tel = date_company['tel']
        email = date_company['email']
        password = date_company['password']
        passwordRepeat = date_company['passwordRepeat']
        idRol = 1


        if auth.validation_form(name, tel, email, password, passwordRepeat) == True:

            #Consulta si el usuario ya esta registrado.
            if auth.search_user(email) == True:
                return "Usuario ya esta registrado", 412
            else:

                #Registra los datos del usuario y retorna el id
                idUser=  auth.create_user(email, password, idRol)
            
                #Registra los datos de la empresa en la base de datos
                company.register_company(name, tel, idUser)

                return 'Usuario registrado correctamente', 200
            
        else:
            return auth.validation_form(name, tel, email, password, passwordRepeat)




#Inicio de sesion para empresas y usuarios
@app.route('/signin', methods=["POST"])
def signin():
    if request.method == 'POST':
        date = request.get_json()

        email = date['email']
        password = date['password']
    
        #Validacion formulario, se verifican que los datos esten vacios
        if auth.validation_form_login(email, password) == True:
            #Primero se verifica si el usuario esta registrado
            existsUser = auth.search_user(email)

            if existsUser == False:
                return 'Email no esta registrado', 409
            if existsUser == True:
                user = auth.login_user(email, password)
                if user:
                    rol = user[0][3]
                    idUser = user[0][0]
                    
                    #Obtiene el id de la empresa que se esta iniciando  sesion
                    idCompany = company.search_id_company(email)

                    #se guardan los datos de la sesion, usuario y id
                    session['company'] = idCompany
                    
                    #Obtiene hora actual
                    DT = datetime.now()
                    currentDate = DT.strftime('%d/%m/%Y')
                    currentTime = DT.strftime("%X")

        #             #Ejecuta funcion que compurba si los funcionarios asistieron.
                    absences.attendanceControl(idCompany, currentDate, currentTime)
                    if rol == 1:
                    # Obtiene el id de la empresa que se esta iniciando  sesion
                        dataCompany = company.get_data_company(idUser)
                        
                        return jsonify(dataCompany), 200
                else:
                    return 'Contraseña incorrecta', 412


        else:
            return auth.validation_form_login(email, password)

        #     #Consulta en la base de datos si las credenciales son correctas 
        #     user = auth.login_user(email, password)
         

        #     #Si el usuario esta registrado se guarda la session en el catche del usuario
        #     if user != False:

        #         rol = user[0][3]
        #         if rol == 1:
        #             #Obtiene el id de la empresa que se esta iniciando  sesion
        #             idCompany = company.search_id_company(email)

        #             #se guardan los datos de la sesion, usuario y id
        #             session['email'] = email
        #             session['company'] = idCompany
                    
        #             #Obtiene hora actual
        #             DT = datetime.now()
        #             currentDate = DT.strftime('%d/%m/%Y')
        #             currentTime = DT.strftime("%X")

        #             #Ejecuta funcion que compurba si los funcionarios asistieron.
        #             absences.attendanceControl(idCompany, currentDate, currentTime)

        #             return jsonify({'message': 'Bienvenido usuario', 'code': '200'})
        #         elif rol == 2:
        #             #Obtiene el id del usuario que se esta iniciando  sesion
        #             idPersonal = personal.search_id_personal(email)

        #             #se guardan los datos de la sesion, usuario y id
        #             session['email'] = email
        #             session['personal'] = idPersonal
                    
        #             return jsonify({'ok': '200'})

        #     else:
        #         return jsonify({'Usuario o contraseña incorrecto': '412'})
        
        # else: 
        #     return validation_form()




#Crea usuario en la tabla usuarios y guarda los datos del empleado en la tabla empleados
@app.route('/register_personal', methods=["POST", "GET"])
def register_personal():
     if request.method == 'POST':
        data = request.get_json()

        document = data['document']
        name = data['name']
        lastname = data['lastname']
        gender = data['gender']
        birthday = data['birthday']
        tel = data['tel']
        address = data['address']
        email = data['email']
        password = 12345678
        idCompany = data['idCompany']
        idRol = 2

        if personal.validation_form_personal(document, name, lastname, gender, birthday, tel, address, email, password, idCompany) == True:

            #Primero se verifica si el correo ya esta registrado
            existsEmail = auth.search_user(email)
            if existsEmail == True:
                return "Correo ya esta registrado", 409
            else:

                existsDocument = personal.get_id_personal(document, idCompany)

                if existsDocument == True:
                    return 'Usuario ya esta registrado', 409

                if existsDocument == False:
                    
                    #Registra los datos del usuario y retorna el id
                    idUser=  auth.create_user(email, password, idRol)

                    #Registra los datos del empleado
                    result = personal.register_personal(document, name, lastname, gender, birthday, tel, address, email, password, idCompany, idUser)
                    return result
            
        else:
            return personal.validation_form_personal(document, name, lastname, gender, birthday, tel, address, email, password, idCompany)



#API empelados: Obtiene todos los empleados de la empresa
@app.route('/get_all_personal')
def get_all_personal():
    data = request.get_json()
    idCompany = data['idCompany']
    
    allPersonal = personal.get_all_personal(idCompany)

    if len(allPersonal) == 0:
        return jsonify("No hay registro de personal"), 412
    else:
        return jsonify(allPersonal), 200


#API Empleado: Obtiene los datos de un empleado
@app.route('/get_personal/<idPersonal>')
def get_personal(idPersonal):

    result = personal.get_personal(idPersonal)
    if len(result) == 0:
        return jsonify('No hay registro'), 409
    else:
        return jsonify(result)


#Elimna empleado de la base de datos
@app.route('/delete_personal/<idPersonal>', methods=["GET", "POST", "DELETE"])
def delete_personal(idPersonal):
    idUser = personal.get_id_user(idPersonal)
    response = personal.delete_personal(idPersonal, idUser)
    return "ok", 200


#Actualiza datos del emplado en la base de datos
@app.route('/update_personal/<idPersonal>', methods=['GET','POST', 'PUT'])
def update_personal(idPersonal):
        data = request.get_json()

        document = data['document']
        name = data['name']
        lastname = data['lastname']
        gender = data['gender']
        birthday = data['birthday']
        tel = data['tel']
        address = data['address']
        if personal.validation_form_update(document, name, lastname, gender, birthday, tel, address, idPersonal) == True:

            #Actualiza datos personales
            result = personal.update_personal(document, name, lastname, gender, birthday, tel, address, idPersonal)
            if result == True:
                return 'Se actualizaron los datos', 200

            if result == False:
                return 'No existe usuario', 409
        else:
            return personal.validation_form_update(document, name, lastname, gender, birthday, tel, address, idPersonal)


#Asignar horario
@app.route('/insert_schedule/<idPersonal>', methods=['POST'])
def insert_schedule(idPersonal):
    if request.method == 'POST':
        data = request.get_json()
        workStart = data['workStart']
        workEnd = data['workEnd']

        if schedule.validation_form_schedule(workStart, workEnd, idPersonal) == True:

            result = schedule.insert_schedule(workStart, workEnd, idPersonal)
            return result
        else:
            return schedule.validation_form_schedule(workStart, workEnd, idPersonal)


#Marcar hora de entrada
@app.route('/mark_start', methods=['POST'])
def insert_mark_start():

    #Se verifica que sea un metods POST
    if request.method == 'POST':

        #Se obtiene la hora y la fecha
        DT = datetime.now()
        currentTime = DT.strftime("%X")
        date = DT.strftime('%d/%m/%Y')

        #Se verifica que el usuario ese en session
        if 'personal' in session:
            idPersonal = session['personal']

            #se valida el formulario
            def validation_form():
                if currentTime == '':
                    return 'La hora no es correcta', 412
                return  True
        
            if validation_form() == True:
                    result = mark.insert_mark_start(idPersonal, currentTime, date)
                    return result
        else:
            return 'Debe iniciar sesion', 412
    

#marca hora salida
@app.route('/mark_end', methods=['POST'])
def insert_mark_end():

    #Se verifica que sea un metods POST
    if request.method == 'POST':
        #Se obtiene la hora y la fecha
        DT = datetime.now()
        currentTime = DT.strftime("%X")
        date = DT.strftime('%d/%m/%Y')
        #Se verifica que el usuario ese en session
        if 'personal' in session:
            #Se obtienen los datos de formularoi
            idPersonal = session['personal']

            #se valida el formulario
            def validation_form():
                if currentTime == '':
                    return 'La hora no es correcta', 412
                return  True
        
            if validation_form() == True:
                result = mark.insert_mark_end(idPersonal, currentTime, date)
                return result
        else:
            return 'Debe iniciar sesion', 412



#Indicar dias libres
@app.route('/insert_authorized_absences/<idPersonal>', methods=['POST'])
def insert_authorized_absences(idPersonal):
    data = request.get_json()
    date = data['date']
    reason = data['reason']
    date_object = datetime.strptime(date, '%m/%d/%y')

    print(data_object)
    if request.method == 'POST':
        if absences.validation_form_absences(date, reason) == True:
            result = absences.insert_authorized_absences(idPersonal, date, reason)
            return result
        else:
            return absences.validation_form_absences(date, reason)

#Eliminar registro de ausencia
@app.route('/delete_authorized_absence/<idAbsence>', methods=['DELETE'])
def delete_authorized_absence(idAbsence):
    if request.method == 'DELETE':
        result = absences.delete_authorized_absence(idAbsence)
        return result


#Actualizar dias de ausencia
@app.route('/update_authorized_absence/<idAbsence>', methods=['PUT'])
def update_authorized_absence(idAbsence):
    
    dateAbsence = request.form['dateAbsence']
    reason = request.form['reason']
    
    if request.method == 'PUT':
        result =  absences.update_authorized_absence(idAbsence, dateAbsence, reason)
        return result


#API AUSENCIAS: Obtiene ausencias progamadas, licenias, libres, etc
@app.route('/get_authorized_absence', methods=['GET'])
def get_authorized_absence():
    if request.method == "GET":
        startDate =  request.args.get("startDate")
        endDate =  request.args.get("endDate")
        idCompany = request.args.get('idCompany')


        result = absences.get_authorized_absence(startDate, endDate, idCompany)
        if result == []:
            return "No hay registros de ausencias", 412
        else:
            return jsonify(result)

#API marcas: Obtiene todas las marcas de un empleado en un periodo 
@app.route('/get_mark', methods=['GET'])
def get_mark():

    if request.method == 'GET':
        document =  request.args.get("document")
        startDate =  request.args.get("startDate")
        endDate =  request.args.get("endDate")
        idCompany = request.args.get('idCompany')
        result = mark.get_mark(document, startDate, endDate, idCompany)
        
        if result:
            return jsonify(result)
        else:
            return jsonify('No se encontraron datos')


#Ingresa marcas manualmente, solo para usuarios con rol administrador
@app.route('/insert_marks/<idPersonal>', methods=['POST'])
def insert_marks(idPersonal):
    if request.method == 'POST':
        
        data = request.get_json()
        date = data['date']
        hourStart = data['hourStart']
        hourEnd = data['hourEnd']
                
        def validation_form():
            if hourStart == '':
                return 'Debe indicar hora entrada', 412
            if hourEnd == '':
                return 'Debe indicar hora salida', 412
            if idPersonal == '':
                return 'Debe indicar idPersonal', 412
            if date == '':
                return 'Debe ingresar fecha', 412
            return True

        if validation_form() == True:

            result = mark.insert_marks(idPersonal, hourStart, hourEnd, date)

            return result

        else:
            return validation_form()




#Actualiza marca ingresada por  id marca
@app.route('/update_mark/<idMark>', methods=['PUT'])
def update_mark(idMark):

    if request.method == 'PUT':
        hourStart = request.form['hourStart']
        hourEnd = request.form['hourEnd']
        idPersonal = request.form['idPersonal']

        def validation_form():
            if hourStart == '':
                return 'Debe indicar hora entrada', 412
            if hourEnd == '':
                return 'Debe indicar hora salida', 412
            if idPersonal == '':
                return 'Debe indicar idPersonal', 412
            if idMark == '':
                return 'Debe ingresar id marca', 412
            return True

        if validation_form() == True:

            result = mark.update_mark(idPersonal, hourStart, hourEnd, idMark)

            return result

        else:
            return validation_form()




#API Notificaciones
@app.route('/get_notification')
def get_notification():
    if request.method == 'GET':
        idCompany =  request.args.get("idCompany")
        status =  request.args.get("status")

   
        result = notification.get_notification(idCompany, status)
        
        if result:
            return jsonify(result)
        else:
            return jsonify("No hay notificaciones pendientes")


#API Ausencias: Obtiene las auencias del dia
@app.route('/get_absences/<idCompany>',methods=['GET'])
def get_absences(idCompany):
    if request.method == 'GET':
    
        DT = datetime.now()
        currentDate = DT.strftime('%d/%m/%Y')

        result = mark.get_absences(currentDate, idCompany)
        if result:
            return jsonify(result), 200
        else:
            return jsonify([]), 412
        

if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)