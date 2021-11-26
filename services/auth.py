
from data.models import model_user

#Crea usuario
def create_user(email, password, idRol):
    return model_user.create_user(email, password, idRol)

#Consulta en la base de datos si existe usuario
def search_user(email):
    return model_user.search_user(email)

#Consulta si el usuario esta registrado
def login_user(email, password):
    return model_user.login_user(email, password)


#Valida que el fomrmulario no este vacio
def validation_form(name, tel, email, password, passwordRepeat):
    if name == "":
        return 'Nombre es requerido', 412
    if tel == "":
        return 'Telefono es requerido', 412
    if email == "":
        return 'Correo es requerido', 412
    if password == "":
        return 'Clave es requerida', 412
    if password != passwordRepeat:
        return 'Las contraseñas deben ser iguales', 412
    return True
        

#Valida que el fomrmulario no este vacio y que el usuario exista
def validation_form_login(email, password):
    if email == "":
        return 'Email es requerido', 412
    if password == "":
        return 'Contraseña es requerida', 412
    return True