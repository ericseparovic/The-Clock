from data.models import model_personal

#Registra los datos del empeado
def register_personal(document, name, lastname, gender, birthday, phone, address, idUser, idCompany):
    return model_personal.register_personal(document, name, lastname, gender, birthday, phone, address, idUser, idCompany)

#Obtiene todos los empleados de la empresa
def get_all_personal(idCompany):
    return model_personal.get_all_personal(idCompany)


#Obtiene empleado por id
def get_personal(idPersonal):
    return model_personal.get_personal(idPersonal)

#Elimina empleado de la lista
def delete_personal(idPersonal):
    return model_personal.delete_personal(idPersonal)

#Actualiza datos del empleado
def update_personal(idPersonal, document, name, lastname, gender, birthday, phone, address):
    return model_personal.update_personal(idPersonal, document, name, lastname, gender, birthday, phone, address)
    
#obtiene id usuario
def search_id_personal(email):
    return model_personal.search_id_personal(email)


