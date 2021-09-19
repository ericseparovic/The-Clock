from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from services import auth
from services import company
from services import personal
from services import schedule
from services import mark
import os

app = Flask(__name__)

app.config.update(SECRET_KEY=os.urandom(24))

#Ruta login usuarios
@app.route('/login')
def login():
    return render_template("login.html")


#Ruta registro de empresas
@app.route('/register')
def register():
    return render_template("register.html")


#Ruta registro de empresas
@app.route('/')
def index():
    if 'email' in session:
        return render_template("index.html")
    else:
        return "No tiene permisos"
    


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




#Inicio de sesion para empresas
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
                    
                    # Ejecuta el metodo index
                    # return redirect(url_for('index'))
                    return "Bienvenido usuario Administrador"
                elif rol == 2:

                    #Obtiene el id del usuario que se esta iniciando  sesion
                    idPersonal = personal.search_id_personal(email)

                    #se guardan los datos de la sesion, usuario y id
                    session['email'] = email
                    session['personal'] = idPersonal

                    return "Bienvenido usuario Personal"

            else:
                #Ejecuta el metodo login
                # return redirect(url_for('login'))
                return 'Usuario o contrasña incorrecto'
        
        else: 
            return validation_form()


#Cierra seccion del usuario
@app.route('/logout', methods=["POST", "GET"])
def logout():
    if request.methods == 'POST':
        session.clear()
        return redirect(url_for('login'))




#Crea usuario en la tabla usuarios y guarda los datos del empleado en la tabla empleados
@app.route('/register-personal', methods=["POST", "GET"])
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
            if auth.search_user(email) == True:
                return "Usuario registrado", 412
            else:
                #Se verifica que el usuario adm tenga iniciado sesion
                if 'email' in session:
                    idCompany = session['company']

                    # Crea usuario y retorna el id
                    idUser=  auth.create_user(email, password, idRol)
                    # Registra datos del empleado
                    personal.register_personal(document, name, lastname, gender, birthday, phone, address, idUser, idCompany)
                    return "Usuario registrado Correctamente", 200
                else:
                    return "Debe iniciar sesion", 412

        else:
            return validation_form()



#Api lista de empleados
@app.route('/all-personal/<idCompany>')
def get_all_personal(idCompany):
    allPersonal = personal.get_all_personal(idCompany)

    if len(allPersonal) == 0:
      return "No hay registros de personal" 
    else:
        return jsonify(allPersonal)


#Api empleado por id
@app.route('/personal/<idPersonal>')
def get_personal(idPersonal):
    employee = personal.get_personal(idPersonal)
    if len(employee) == 0:
        return "No hay registro"
    else:
        return jsonify(employee)


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
@app.route('/schedule', methods=['POST'])
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

#Marcar hora de entrada y salida
@app.route('/mark-start', methods=['POST'])
def insert_mark_start():

    #Se verifica que sea un metods POST
    if request.method == 'POST':
        #Se verifica que el usuario ese en session
        if 'personal' in session:
            #Se obtienen los datos de formularoi
            hour = request.form['hour']
            date = request.form['date']
            idPersonal = session['personal']

            #se valida el formulario
            def validation_form():
                if hour == '':
                    return 'La hora no es correcta', 412
                return  True
        
            if validation_form() == True:
                    result = mark.insert_mark_start(idPersonal, hour, date)
                    return result
        else:
            return 'Debe iniciar sesion', 412
    

@app.route('/mark-end', methods=['POST'])
def insert_mark_end():

    #Se verifica que sea un metods POST
    if request.method == 'POST':
        #Se verifica que el usuario ese en session
        if 'personal' in session:
            #Se obtienen los datos de formularoi
            hour = request.form['hour']
            date = request.form['date']
            idPersonal = session['personal']

            #se valida el formulario
            def validation_form():
                if hour == '':
                    return 'La hora no es correcta', 412
                return  True
        
            if validation_form() == True:
                result = mark.insert_mark_end(idPersonal, hour, date)
                return result
        else:
            return 'Debe iniciar sesion', 412



if __name__ == '__main__':
    app.debug = True
    app.run(port=5000)