from data.data_base import DataBase
from data.models import model_user
  

#Registra datos del empleado
def register_personal(document, name, lastname, gender, birthday, phone, address, idUser, idCompany):

    register_personal_sql = f"""
        INSERT INTO EMPLEADOS(DOCUMENTO, NOMBRE, APELLIDO, GENERO, FECHA_NACIMIENTO, TELEFONO, DIRECCION, ID_USUARIO, ID_EMPRESA)
        VALUES ('{document}','{name}', '{lastname}', '{gender}', '{birthday}', '{phone}','{address}','{idUser}', '{idCompany}')
    """
    bd = DataBase()
    valor = bd.ejecutar_sql(register_personal_sql)

    return True


#Obtiene todos los empleado de la empresa
def get_all_personal(idCompany):
    select_allpersonal_sql = f"""
        SELECT * FROM EMPLEADOS WHERE ID_EMPRESA='{idCompany}'
    """ 

    db = DataBase()
    user = db.ejecutar_sql(select_allpersonal_sql)
    
    return user

#Obtiene empleado por id
def get_personal(idPersonal):

    select_personal_sql = f"""
        SELECT * FROM EMPLEADOS WHERE ID_EMPLEADO='{idPersonal}'
    """ 

    db = DataBase()
    user = db.ejecutar_sql(select_personal_sql)
    
    return user



#Elimina empleado de la tabla empleados
def delete_personal(idPersonal):
    delete_personal_sql = f"""
        DELETE FROM EMPLEADOS WHERE ID_EMPLEADO='{idPersonal}'
    """

    #Consultamos si el id que queremos borrar pertenece a un usuario
    result = get_personal(idPersonal)

    if len(result) == 0:
        return "No existe empleado con ese id"
    else:
        db = DataBase()
        user = db.ejecutar_sql(delete_personal_sql)
        print(result)
        return True

#ACtualiza datos del empleado
def update_personal(idPersonal, document, name, lastname, gender, birthday, phone, address):
    update_personal_sql = f"""
        UPDATE EMPLEADOS SET DOCUMENTO='{document}', NOMBRE='{name}', APELLIDO='{lastname}', GENERO='{gender}', FECHA_NACIMIENTO='{birthday}', TELEFONO='{phone}', DIRECCION='{address}' WHERE ID_EMPLEADO='{idPersonal}'
    """

    #Consultamos si el id que queremos actualizar esta registrado pertenece a un usuario
    result = get_personal(idPersonal)

    if len(result) == 0:
        return "No existe empleado con ese id"
    else:
        db = DataBase()
        user = db.ejecutar_sql(update_personal_sql)
        return True

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
