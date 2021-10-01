from data.models import model_company

#Registra los datos de la empresa en la BD empresas
def register_company(correo, clave, idUser):
    model_company.register_company(correo, clave, idUser)

#Busca si la empresa esta registrada y debuelve el id
def search_id_company(email):
    return model_company.search_id_company(email)

