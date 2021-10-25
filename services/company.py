from requests.models import requote_uri
from data.models import model_company

#Registra los datos de la empresa en la BD empresas
def register_company(correo, clave, idUser):
    model_company.register_company(correo, clave, idUser)

#Busca si la empresa esta registrada y retorna el id
def search_id_company(email):
    return model_company.search_id_company(email)

#
def get_data_company(idUser):
    return model_company.get_data_company(idUser)   
