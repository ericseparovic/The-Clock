from data.data_base import DataBase
from data.models import model_user
  

#Registra datos del empleado
def register_personal(document, name, lastname, gender, birthday, tel, address, email, password, idCompany, idUser):

    register_personal_sql = f"""
    INSERT INTO EMPLEADOS(DOCUMENTO, NOMBRE, APELLIDO, GENERO, FECHA_NACIMIENTO, TELEFONO, DIRECCION, ID_USUARIO, ID_EMPRESA)
    VALUES ('{document}','{name}', '{lastname}', '{gender}', '{birthday}', '{tel}','{address}','{idUser}', '{idCompany}')
    """
    bd = DataBase()
    bd.ejecutar_sql(register_personal_sql)
    try:
        return "Se registro correctamente", 200
    except:
        return "No se pudo registrar", 412
    

    


#Obtiene todos los empleado de la empresa
def get_all_personal(idCompany):
    select_allpersonal_sql = f"""
        SELECT * FROM EMPLEADOS WHERE ID_EMPRESA='{idCompany}'
    """ 
    
    db = DataBase()
    all_personal = []



    for personal in db.ejecutar_sql(select_allpersonal_sql):

        name_user = get_name_user(personal[8])
    
        dict_personal = {
            'idPersonal': personal[0],
            'document': personal[1],
            'name': personal[2],
            'lastName': personal[3],
            'gender': personal[4],
            'birthday': personal[5],
            'tel': personal[6],
            'address': personal[7],
            'idUser': personal[8],
            'idCompany': personal[9],
            'idHour': personal[10],
            'nameUser': name_user
        }

        all_personal.append(dict_personal)
    return all_personal


#Obtienen nombre de usuario
def get_name_user(idUser):
    select_name_user_sql = f"""
        SELECT CORREO FROM USUARIOS WHERE ID_USUARIO='{idUser}'
    """ 
    
    db = DataBase()
    name_user = db.ejecutar_sql(select_name_user_sql)
    return name_user[0][0]

#Obtiene empleado por id
def get_personal(idPersonal):

    select_personal_sql = f"""
        SELECT * FROM EMPLEADOS WHERE ID_EMPLEADO='{idPersonal}'
    """ 

    db = DataBase()
    all_personal = []

    for personal in db.ejecutar_sql(select_personal_sql):
        name_user = get_name_user(personal[8])

        dict_personal = {
            'idPersonal': personal[0],
            'document': personal[1],
            'name': personal[2],
            'lastName': personal[3],
            'genero': personal[4],
            'birthday': personal[5],
            'tel': personal[6],
            'address': personal[7],
            'idUser': personal[8],
            'idCompany': personal[9],
            'idHour': personal[10],
            'nameUser': name_user

        }

        all_personal.append(dict_personal)
    return all_personal


#Elimina empleado de la tabla empleados
def delete_personal(idPersonal, idUser):
    delete_personal_sql = f"""
        DELETE FROM EMPLEADOS WHERE ID_EMPLEADO='{idPersonal}'
    """
    delete_usuario_sql = f"""
        DELETE FROM USUARIOS WHERE ID_USUARIO='{idUser}'
    """

    #Consultamos si el id que queremos borrar pertenece a un usuario
    result = get_personal(idPersonal)

    if len(result) == 0:
        return "No existe empleado con ese id", 409
    else:
        db = DataBase()
        try:
            db.ejecutar_sql(delete_personal_sql)
            db.ejecutar_sql(delete_usuario_sql)
            return "Se elimino correctamente", 200
        except:
            return "No se pudo eliminar", 412

#ACtualiza datos del empleado
def update_personal(document, name, lastname, gender, birthday, tel, address, idPersonal, email):
    update_personal_sql = f"""
        UPDATE EMPLEADOS SET DOCUMENTO='{document}', NOMBRE='{name}', APELLIDO='{lastname}', GENERO='{gender}', FECHA_NACIMIENTO='{birthday}', TELEFONO='{tel}', DIRECCION='{address}' WHERE ID_EMPLEADO='{idPersonal}'
    """

    #Consultamos si el id que queremos actualizar esta registrado pertenece a un usuario
    result = get_personal(idPersonal)

    if len(result) == 0:
        return False
    else:
        db = DataBase()
        #Actualizados datos en la tabla empleados
        db.ejecutar_sql(update_personal_sql)

        #Actualizamos correo en la tabla usuario
        update_email(email, idPersonal)

        return True


def update_email(email, idPersonal):
    result = get_personal(idPersonal)

    update_email_sql = f"""
        UPDATE USUARIOS SET CORREO='{email}' WHERE ID_USUARIO='{result[0]['idUser']}'
    """
    db = DataBase()

    db.ejecutar_sql(update_email_sql)

    return result

#Retorna id de la personal
def search_id_personal(email):

    idUser = model_user.search_id_user(email)
    

    select_id_personal = f"""
        SELECT ID_EMPLEADO FROM EMPLEADOS WHERE ID_USUARIO='{idUser[0][0]}'
    """ 
    
    db = DataBase()
    idPersonal = db.ejecutar_sql(select_id_personal)

    return idPersonal[0][0]




#Asignar hora empleado
def assign_time(idPersonal, idSchedule):

    assign_time_sql = f"""
        UPDATE EMPLEADOS SET ID_HORARIO='{idSchedule}' WHERE ID_EMPLEADO='{idPersonal}'
    """

    #Consultamos si el id que queremos actualizar esta registrado pertenece a un usuario
    result = get_personal(idPersonal)
    
    if len(result) == 0:
        return "No existe empleado con ese id"
    else:
        db = DataBase()
        db.ejecutar_sql(assign_time_sql)
        return 'Se registro la hora correctamente', 200



def get_id_personal(document, idCompany):
    select_id_sql =  f"""
            SELECT ID_EMPLEADO FROM EMPLEADOS WHERE DOCUMENTO='{document}' AND ID_EMPRESA='{idCompany}'
    """ 
    db = DataBase()
    idPersonal = db.ejecutar_sql(select_id_sql) 
    
    if idPersonal:
        return True
    else: 
        return False


def get_id_user(idPersonal):
    select_id_sql =  f"""
            SELECT ID_USUARIO FROM EMPLEADOS WHERE ID_EMPLEADO='{idPersonal}'
    """ 
    db = DataBase()
    idUser = db.ejecutar_sql(select_id_sql) 
    
    return idUser[0][0]

#Obtiene del usuario
def get_data_personal(idUser):    

    select_id_personal = f"""
        SELECT * FROM EMPLEADOS WHERE ID_USUARIO='{idUser}'
    """ 
    
    db = DataBase()
    data_personal = db.ejecutar_sql(select_id_personal)
    
        
    dict_personal = {
        'idPersonal': data_personal[0][0],
        'namePersonal': data_personal[0][2],
        'tel': data_personal[0][6],
        'idUser': data_personal[0][8]
    }

    return dict_personal