from flask import Flask, request, render_template, redirect, url_for, session, jsonify
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

#Ruta registro de empresas
@app.route('/register_company')
def register_company():
    return render_template("register_company.html")

#Login empresas
@app.route('/')
def login_company():
    return render_template('login_company.html')

#Login personal
@app.route('/login_personal')
def login_personal():
    return render_template("login_personal.html")

@app.route('/index_company')
def index_company():
    if 'company' in session:
        return render_template('index_company.html')
    else:
        return  redirect(url_for('login_company'))




#Se ejecuta al registrar la empresa, se guarda los datos del usuario en la tabla usuarios y se guarda los datos de la empresa en la tabla empresas
@app.route('/signup', methods=["POST", "GET"])
def signup():

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        idRol = 1

        #Valida que el fomrmulario no este vacio
        def validation_form():
            if name == "":
                return 'Nombre es requerido', 412
            if phone == "":
                return 'Telefono es requerido', 412
            if email == "":
                return 'Correo es requerido', 412
            if password == "":
                return 'Clave es requerida', 412
            return True
        

        if validation_form() == True:

            #Consulta si el usuario ya esta registrado.
            if auth.search_user(email) == True:
                return "Usuario ya esta registrado"
            else:
                #Registra los datos del usuario y retorna el id
                idUser=  auth.create_user(email, password, idRol)
            
                #Registra los datos de la empresa en la base de datos
                company.register_company(name, phone, idUser)

                return "Usuario registrado Correctamente", 200
            
        else:
            return validation_form()




#Inicio de sesion para empresas y usuarios
@app.route('/signin', methods=["POST", "GET"])
def signin():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

       #Valida que el formulario no este vacio
        def validation_form():
            if email == "":
                return 'Correo es requerido', 412
            if password == "":
                return 'Clave es requerida', 412
            return True

        if validation_form() == True:

            #Consulta en la base de datos si las credenciales son correctas 
            user = auth.login_user(email, password)
         

            #Si el usuario esta registrado se guarda la session en el catche del usuario
            if user != False:

                rol = user[0][3]
                if rol == 1:
                    #Obtiene el id de la empresa que se esta iniciando  sesion
                    idCompany = company.search_id_company(email)

                    #se guardan los datos de la sesion, usuario y id
                    session['email'] = email
                    session['company'] = idCompany
                    
                    #Obtiene hora actual
                    DT = datetime.now()
                    currentDate = DT.strftime('%d/%m/%Y')
                    currentTime = DT.strftime("%X")

                    #Ejecuta funcion que compurba si los funcionarios asistieron.
                    absences.attendanceControl(idCompany, currentDate, currentTime)

                    # Ejecuta el metodo index
                    # return redirect(url_for('index'))
                    return "Bienvenido usuario Administrador"
                elif rol == 2:
                    #Obtiene el id del usuario que se esta iniciando  sesion
                    idPersonal = personal.search_id_personal(email)

                    #se guardan los datos de la sesion, usuario y id
                    session['email'] = email
                    session['personal'] = idPersonal
                    
                    return "Bienvenido usuario Personal", 200

            else:
                return 'Usuario o contrasña incorrecto', 412
        
        else: 
            return validation_form()


#Cierra seccion del usuario
@app.route('/logout', methods=["POST", "GET"])
def logout():
    if request.method == 'POST':
        session.clear()
        return "Sesion Cerrada", 200




#Crea usuario en la tabla usuarios y guarda los datos del empleado en la tabla empleados
@app.route('/register_personal', methods=["POST", "GET"])
def register_personal():
     if request.method == 'POST':
        document = request.form['document']
        name = request.form['name']
        lastname = request.form['lastname']
        gender = request.form['gender']
        birthday = request.form['birthday']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']
        password = 12345678
        idRol = 2

        #Valida que el fomrmulario no este vacio
        def validation_form():
            if document == "":
                return 'Documento es requerido', 412
            if name == "":
                return 'Nombre es requerido', 412
            if lastname == "":
                return 'Apellido es requerido', 412
            if gender == "":
                return 'Genero es requerido', 412
            if phone == "":
                return 'Telefono es requerido', 412
            if birthday == "":
                return 'Fecha de nacimiento es requerido', 412
            if email == "":
                return 'Correo es requerido', 412
            if address == "":
                return 'Direccion es requerida', 412
            if password == "":
                return 'Clave es requerida', 412
            return True


        if validation_form() == True:
            #Consulta si el usuario ya esta registrado.
            if auth.search_user(email):
                return "Usuario ya esta registrado", 412
            else:
                #Se verifica que el usuario administrador tenga iniciado sesion
                if 'email' in session:
                    idCompany = session['company']

                    if personal.get_id_personal(document, idCompany):
                        return "Empleado ya registrado en la planilla", 412
                    else:
                        
                        # Crea usuario y retorna el id
                        idUser=  auth.create_user(email, password, idRol)

                        # Registra datos del empleado
                        result = personal.register_personal(document, name, lastname, gender, birthday, phone, address, idUser, idCompany)
                        return result
                else:
                    return "Debe iniciar sesion", 412

        else:
            return validation_form()



#API empelados: Obtiene todos los empleados de la empresa
@app.route('/all_personal')
def get_all_personal():
    idCompany =  request.args.get("idCompany")

    allPersonal = personal.get_all_personal(idCompany)

    if len(allPersonal) == 0:
        return jsonify("No hay registro de personal") 
    else:
        return jsonify(allPersonal)


#API Empleado: Obtiene los datos de un empleado
@app.route('/personal')
def get_personal():
    idPersonal =  request.args.get("idPersonal")

    result = personal.get_personal(idPersonal)
    if len(result) == 0:
        return jsonify('No hay registro'), 412
    else:
        return jsonify(result)


#Elimna empleado de la base de datos
@app.route('/personal/<idPersonal>', methods=['DELETE'])
def delete_personal(idPersonal):
    result = personal.delete_personal(idPersonal)
    
    if result == True:
        return "Empleado eliminado", 200
    else:
        return "No se pudo elimnar", 412


#Actualiza datos del emplado en la base de datos
@app.route('/personal', methods=['PUT'])
def update_personal():
    document = request.form['document']
    name = request.form['name']
    lastname = request.form['lastname']
    gender = request.form['gender']
    birthday = request.form['birthday']
    phone = request.form['phone']
    address = request.form['address']
    idPersonal = request.form['id']

    result = personal.update_personal(idPersonal, document, name, lastname, gender, birthday, phone, address)

    return 'Datos Actulizados', 200


#Asignar horario
@app.route('/insert_schedule', methods=['POST'])
def insert_schedule():
    if request.method == 'POST':
        workStart = request.form['workStart']
        workEnd = request.form['workEnd']
        idPersonal = request.form['idPersonal']

        #Validacion formulario
        def validation_form():
            if workStart == '':
                return 'Debe ingresar hora de entrada', 412
            if workEnd == '':
                return 'Debe ingresar hora de salida', 412
            if idPersonal == '':
                return 'Debe seleccionar un funcionario', 412
            return True
        
        if validation_form() == True:
            result = schedule.insert_schedule(workStart, workEnd, idPersonal)

            return result
        else:
            return validation_form()


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
@app.route('/insert_authorized_absences', methods=['POST'])
def insert_authorized_absences():
    try:
        #Se verifica que sea metodo POST
        if request.method == 'POST':

            #Se obtiene los datos
            dateAbsence = request.form['dateAbsence']
            reason = request.form['reason']
            idPersonal = request.form['idPersonal']
            
            #se valida el formulario
            def validation_form():
                if dateAbsence == '':
                    return 'Debe indicar indicar fecha de falta', 412
                if reason == '':
                        return 'Debe indicar motivo', 412
                return True

            if validation_form() == True:

                result = absences.insert_authorized_absences(idPersonal, dateAbsence, reason)

                return result
    except:
        return "No se pudo agregar ausencia", 412


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
@app.route('/insert_marks', methods=['POST'])
def insert_marks():
    if request.method == 'POST':
        
        hourStart = request.form['hourStart']
        hourEnd = request.form['hourEnd']
        idPersonal = request.form['idPersonal']
        date = request.form['date']
        
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
@app.route('/get_absences',methods=['GET'])
def get_absences():
    if request.method == 'GET':
        startDate =  request.args.get("startDate")
        endDate = request.args.get("endDate")
        idCompany = request.args.get("idCompany")

        result = mark.get_absences(startDate, endDate, idCompany)
        
        if result:
            return jsonify(result)
        else:
            return jsonify("No hay datos"), 412
        

if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)