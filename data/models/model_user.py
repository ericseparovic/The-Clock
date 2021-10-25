from data.data_base import DataBase


#Crea el usuario de la empresa 
def create_user(email, password, idRol):

    create_user_sql = f"""
        INSERT INTO USUARIOS(CORREO, CLAVE, ID_ROL)
        VALUES ('{email}','{password}', '{idRol}')
    """
    db = DataBase()
    db.ejecutar_sql(create_user_sql)

    id = search_id_user(email)

    return id[0][0]


#Consulta en la base de datos si el usuario esta registrado
def search_user(email):

    search_user_sql = f"""
        SELECT * FROM USUARIOS WHERE correo= '{email}'
    """
    db = DataBase()
    user = db.ejecutar_sql(search_user_sql)
    

    if len(user) == 0:
        return False
    else:
        return True


#Retorna id usuario registrado
def search_id_user(email):
    select_id_usuario = f"""
        SELECT ID_USUARIO FROM USUARIOS WHERE CORREO='{email}'
    """ 
    
    db = DataBase()
    id = db.ejecutar_sql(select_id_usuario)
    return id


#Consulta en la base de datos si las credenciales son correctas 
def login_user(email, password):
    select_id_usuario = f"""
        SELECT * FROM USUARIOS WHERE CORREO='{email}' AND CLAVE='{password}'
    """ 

    db = DataBase()
    user = db.ejecutar_sql(select_id_usuario)

    return user