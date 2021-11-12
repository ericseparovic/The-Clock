from data.models import model_personal

#Registra los datos del empeado
def register_personal(document, name, lastname, gender, birthday, tel, address, email, password, idCompany, idUser):
    return model_personal.register_personal(document, name, lastname, gender, birthday, tel, address, email, password, idCompany, idUser)

#Obtiene todos los empleados de la empresa
def get_all_personal(idCompany):
    return model_personal.get_all_personal(idCompany)


#Obtiene empleado por id
def get_personal(idPersonal):
    return model_personal.get_personal(idPersonal)

#Elimina empleado de la lista
def delete_personal(idPersonal, idUser):
    return model_personal.delete_personal(idPersonal, idUser)

#Actualiza datos del empleado
def update_personal(document, name, lastname, gender, birthday, tel, address, idPersonal):
    return model_personal.update_personal(document, name, lastname, gender, birthday, tel, address, idPersonal)


#obtiene id usuario
def search_id_personal(email):
    return model_personal.search_id_personal(email)


def get_id_personal(document, idCompany):
    return model_personal.get_id_personal(document, idCompany)

#Valida que el fomrmulario no este vacio
def validation_form_personal(document, name, lastname, gender, birthday, tel, address, email, password, idCompnay):

    if document == "":
        return 'Documento es requerido', 412
    if name == "":
        return 'Nombre es requerido', 412
    if lastname == "":
        return 'Apellido es requerido', 412
    if gender == "":
        return 'Genero es requerido', 412
    if birthday == "":
        return 'Fecha de nacimiento es requerido', 412
    if tel == "":
        return 'Telefono es requerido', 412
    if address == "":
        return 'Direccion es requerida', 412
    if email == "":
        return 'Correo es requerido', 412
    if password == "":
        return 'Clave es requerida', 412
    if idCompnay == "":
        return 'id compnay no indicado', 412
    return True

def get_id_user(idPersonal):
    return model_personal.get_id_user(idPersonal)


def validation_form_update(document, name, lastname, gender, birthday, tel, address, idPersonal):
    if document == "":
        return 'Documento es requerido', 412
    if name == "":
        return 'Nombre es requerido', 412
    if lastname == "":
        return 'Apellido es requerido', 412
    if gender == "":
        return 'Genero es requerido', 412
    if birthday == "":
        return 'Fecha de nacimiento es requerido', 412
    if tel == "":
        return 'Telefono es requerido', 412
    if address == "":
        return 'Direccion es requerida', 412
    if idPersonal == "":
        return 'Correo es requerido', 412
    return True


