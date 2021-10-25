from data.data_base import DataBase
from data.models import model_user

def register_company(name, phone, idUser):

    register_company_sql = f"""
        INSERT INTO EMPRESAS(NOMBRE, TELEFONO, ID_USUARIO)
        VALUES ('{name}','{phone}', '{idUser}')
    """

    bd = DataBase()
    bd.ejecutar_sql(register_company_sql)


#Retorna id de la empresa
def search_id_company(email):

    idUser = model_user.search_id_user(email)
    

    select_id_company = f"""
        SELECT ID_EMPRESA FROM EMPRESAS WHERE ID_USUARIO='{idUser[0][0]}'
    """ 
    
    db = DataBase()
    idCompany = db.ejecutar_sql(select_id_company)

    return idCompany[0][0]

#Obtiene datos de la empresa
def get_data_company(idUser):    

    select_id_company = f"""
        SELECT * FROM EMPRESAS WHERE ID_USUARIO='{idUser}'
    """ 
    
    db = DataBase()
    data_company = db.ejecutar_sql(select_id_company)
    
        
    dict_company = {
        'idCompany': data_company[0][0],
        'nameCompany': data_company[0][1],
        'tel': data_company[0][2],
        'idUser': data_company[0][3]
    }

    
    return dict_company