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
        dict_personal = {
            'idPersonal': personal[0],
            'document': personal[1],
            'name': personal[2],
            'lastName': personal[3],
            'genero': personal[4],
            'year': personal[5],
            'phone': personal[6],
            'address': personal[7],
            'idUser': personal[8],
            'idCompany': personal[9],
            'idHour': personal[10]
        }

        all_personal.append(dict_personal)
    return all_personal

#Obtiene empleado por id
def get_personal(idPersonal):

    select_personal_sql = f"""
        SELECT * FROM EMPLEADOS WHERE ID_EMPLEADO='{idPersonal}'
    """ 

    db = DataBase()
    all_personal = []

    for personal in db.ejecutar_sql(select_personal_sql):
        dict_personal = {
            'idPersonal': personal[0],
            'document': personal[1],
            'name': personal[2],
            'lastName': personal[3],
            'genero': personal[4],
            'year': personal[5],
            'phone': personal[6],
            'address': personal[7],
            'idUser': personal[8],
            'idCompany': personal[9],
            'idHour': personal[10]
        }

        all_personal.append(dict_personal)
    return all_personal


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