from data.data_base import DataBase
from data.models import model_personal

#Asigna hora de entrada y salida
def insert_schedule(workStart, workEnd, idPersonal):
    db = DataBase()

    #Buscamos si el horario ya esta reigrado 
    search_shcedule_sql = f"""
        SELECT ID_HORARIO FROM HORARIOS WHERE HORA_ENTRADA='{workStart}' AND HORA_SALIDA='{workEnd}'
    """

    result = db.ejecutar_sql(search_shcedule_sql)

    if result == []:
        #Se guarda horario en la base de datos
        insert_schedule_sql = f"""
            INSERT INTO HORARIOS(HORA_ENTRADA, HORA_SALIDA)
            VALUES ('{workStart}','{workEnd}')
        """
        bd = DataBase()
        bd.ejecutar_sql(insert_schedule_sql)

        #Buscamos el id del registro
        search_shcedule_sql = f"""
            SELECT ID_HORARIO FROM HORARIOS WHERE HORA_ENTRADA='{workStart}' AND HORA_SALIDA='{workEnd}'
        """
        result = db.ejecutar_sql(search_shcedule_sql)
        idSchedule = result[0][0]
        #Asigno la hora guardada al funcionario
        return model_personal.assign_time(idPersonal, idSchedule)
    else:

        idSchedule = result[0][0]
        return model_personal.assign_time(idPersonal, idSchedule)


