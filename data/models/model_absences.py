from data.data_base import DataBase
from data.models import model_personal
from data.models import model_mark
from datetime import datetime
from datetime import timedelta

#Asigna ausencias programadas, licencias, libres
def insert_authorized_absences(idPersonal, startDate, endDate, reason):


    if startDate == endDate:
        #Buscamos si el funcionario ya tiene registrado dia libre
        search_absence_sql = f"""
            SELECT ID_AUSENCIA FROM AUSENCIAS WHERE FECHA_AUSENCIA='{startDate}' AND ID_EMPLEADO='{idPersonal}'
        """
        db = DataBase()
        result = db.ejecutar_sql(search_absence_sql)
        if result == []:
            insert_authorized_absences_sql = f"""
                INSERT INTO AUSENCIAS(FECHA_AUSENCIA, MOTIVO, ID_EMPLEADO)
                VALUES ('{startDate}','{reason}', '{idPersonal}')
            """
            db = DataBase()
            db.ejecutar_sql(insert_authorized_absences_sql)

            absence = model_mark.get_absences_personal(startDate, idPersonal)
            
            #Eliminamos registro de falta
            if absence:
                idMark = absence[0][0]
                incidence = reason
                model_mark.update_incidence(idMark, incidence)
            return "Se registro ausencia", 200
        else: 
            return "Ya existe registro", 412
    else:
        startDate = datetime.strptime(startDate, '%d/%m/%Y')
        endDate = datetime.strptime(endDate, '%d/%m/%Y')
        start = int(startDate.strftime("%d"))
        end = int(endDate.strftime("%d"))



        for x in range(start, end + 1):
            #Buscamos si el funcionario ya tiene registrado dia libre
            search_absence_sql = f"""
                SELECT ID_AUSENCIA FROM AUSENCIAS WHERE FECHA_AUSENCIA='{startDate.strftime("%d/%m/%Y")}' AND ID_EMPLEADO='{idPersonal}'
            """
            db = DataBase()
            result = db.ejecutar_sql(search_absence_sql)
            if result == []:
                insert_authorized_absences_sql = f"""
                    INSERT INTO AUSENCIAS(FECHA_AUSENCIA, MOTIVO, ID_EMPLEADO)
                    VALUES ('{startDate.strftime("%d/%m/%Y")}','{reason}', '{idPersonal}')
                """
                db = DataBase()
                db.ejecutar_sql(insert_authorized_absences_sql)

                absence = model_mark.get_absences_personal(startDate.strftime("%d/%m/%Y"), idPersonal)
                startDate= startDate + timedelta(days=1)  
                #Eliminamos registro de falta
                if absence:
                    idMark = absence[0][0]
                    incidence = reason
                    model_mark.update_incidence(idMark, incidence)


        return 'ok', 200

#Eliminar registro de ausencia
def delete_authorized_absence(idAbsence):

    try:
        #Obtenemos datos de la ausenca a elimnar
        data_absence = get_data_absence(idAbsence)
        idPersonal = data_absence[0][3]
        date_absence = data_absence[0][1]
        reason = data_absence[0][2]

        #Eliminamos registro de ausencia
        delete_absence_sql = f"""
            DELETE FROM AUSENCIAS WHERE ID_AUSENCIA='{idAbsence}'
        """

        db = DataBase()
        db.ejecutar_sql(delete_absence_sql)

        #Eliminamos incidencia de libre en la tabla marcas
        print('dsfasdfasdjfjasdfjasdjfas')
        result_delete_mark = delete_ausence_mark(idPersonal, date_absence, reason)
        return "Se elimino ausencia", 200
    except:
        return "Error no se pudieron eliminar datos", 412


#Actualizar fechas ausencia
def update_authorized_absence(idAbsence, dateAbsence, reason):
    try:
        update_absence_sql = f"""
            UPDATE AUSENCIAS SET FECHA_AUSENCIA='{dateAbsence}', MOTIVO='{reason}' WHERE ID_AUSENCIA='{idAbsence}'
            """
        db = DataBase()
        db.ejecutar_sql(update_absence_sql)
        return "Se actualizaron los datos", 200
    except:
        return "No se pudieron actualizar datos", 412


#API Obtener ausencias por rango de fechas
def get_authorized_absence(idPersonal, currentDate):
    absences = []    

    try:
        select_absence = f"""
            SELECT * 
            FROM AUSENCIAS 
            WHERE  FECHA_AUSENCIA >= '{currentDate}' AND ID_EMPLEADO='{idPersonal}' ORDER BY FECHA_AUSENCIA 
        """
        db = DataBase()

        for abcence in db.ejecutar_sql(select_absence):
            dict_absence = {
                'idAbsence': abcence[0],
                'dateAbsence': abcence[1],
                'reason': abcence[2],
                'idPersonal': abcence[3]
            }

            absences.append(dict_absence)
        return absences
    except:
        return []

#Obtiene aucencias de un empleado por id
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


def get_day(date):
    date_part = date.split('/')    
    day = date_part[0] 
    return int(day)


def get_data_absence(idAbsence):
    search_absence_sql = f"""
            SELECT * FROM AUSENCIAS WHERE ID_AUSENCIA='{idAbsence}'
    """
    db = DataBase()
    result = db.ejecutar_sql(search_absence_sql)
    return result


def delete_ausence_mark(idPersonal, date_absence, reason):

    #Eliminamos registro de ausencia
    search_mark_sql =  f"""
            DELETE FROM MARCAS WHERE ID_EMPLEADO='{idPersonal}' AND FECHA='{date_absence}' AND INCIDENCIA_ASISTENCIA='{reason}'
    """ 
    db = DataBase()
    result = db.ejecutar_sql(search_mark_sql) 
    print('resultaedo', result) 
    return result
