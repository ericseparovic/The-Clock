from data.data_base import DataBase

#Asigna ausencias programadas, licencias, libres
def insert_absence(idPersonal, startDate, endDate, reason):
    insert_absence_sql = f"""
        INSERT INTO AUSENCIAS(FECHA_DESDE, FECHA_HASTA, MOTIVO, ID_EMPLEADO)
        VALUES ('{startDate}', '{endDate}', '{reason}', '{idPersonal}')
    """
    bd = DataBase()
    bd.ejecutar_sql(insert_absence_sql)
    

    
    return 'ok', 200