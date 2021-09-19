from data.models import model_company

def register_company(correo, clave, idUser):
    model_company.register_company(correo, clave, idUser)

def search_id_company(email):
    return model_company.search_id_company(email)