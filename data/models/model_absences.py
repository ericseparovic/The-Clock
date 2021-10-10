from data.data_base import DataBase

#Asigna ausencias programadas, licencias, libres
def insert_absence(idPersonal, dateAbsence, reason):
    try:
        #Buscamos si el funcionario ya tine registrado dia libre
        search_absence_sql = f"""
            SELECT ID_AUSENCIA FROM AUSENCIAS WHERE FECHA_AUSENCIA='{dateAbsence}' AND ID_EMPLEADO='{idPersonal}'
        """
        bd = DataBase()
        result = bd.ejecutar_sql(search_absence_sql)
        
        if result == []:
            insert_absence_sql = f"""
                INSERT INTO AUSENCIAS(FECHA_AUSENCIA, MOTIVO, ID_EMPLEADO)
                VALUES ('{dateAbsence}','{reason}', '{idPersonal}')
            """
            bd = DataBase()
            bd.ejecutar_sql(insert_absence_sql)
        
            return "Se registro ausencia", 200
        else: 
            return "Ya existe registro", 412
    except:
        return "Error al registrar datos", 412

#Eliminar registro de ausencia
def delete_absence(idAbsence):

    try:
        delete_absence_sql = f"""
            DELETE FROM AUSENCIAS WHERE ID_AUSENCIA='{idAbsence}'
        """

        db = DataBase()
        db.ejecutar_sql(delete_absence_sql)

        return "Se elimino ausencia", 200
    except:
        return "Error no se pudieron eliminar datos", 412


#Actualizar fechas ausencia
def update_absence(idAbsence, dateAbsence, reason):
    try:
        update_personal_sql = f"""
            UPDATE AUSENCIAS SET FECHA_AUSENCIA='{dateAbsence}', MOTIVO='{reason}' WHERE ID_AUSENCIA='{idAbsence}'
            """
        db = DataBase()
        db.ejecutar_sql(update_personal_sql)
        return "Se actualizaron los datos", 200
    except:
        return "No se pudieron actualizar datos", 412

#Obtener ausencias por rango de fechas
def get_absence_by_date(startDate, endDate):
    select_absence = f"""
        SELECT * 
        FROM AUSENCIAS 
        WHERE  FECHA_AUSENCIA BETWEEN '{startDate}' AND '{endDate}' ORDER BY FECHA_AUSENCIA 
    """
    db = DataBase()
    absences = []

    for abcence in db.ejecutar_sql(select_absence):
        dict_absence = {
            'idAbcence': abcence[0],
            'dateAbsence': abcence[1],
            'reason': abcence[2],
            'idPersonal': abcence[3]
        }

        absences.append(dict_absence)
    return absences
   


def get_absence_by_id(idPersonal, currentDate):
    select_absence = f"""
        SELECT * 
        FROM AUSENCIAS 
        WHERE  FECHA_AUSENCIA='{currentDate}' AND ID_EMPLEADO='{idPersonal}' 
    """

    db = DataBase()
    absences = []

    for abcence in db.ejecutar_sql(select_absence):
        dict_absence = {
            'idAbcence': abcence[0],
            'dateAbsence': abcence[1],
            'reason': abcence[2],
            'idPersonal': abcence[3]
        }

        absences.append(dict_absence)
    return absences