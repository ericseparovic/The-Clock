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