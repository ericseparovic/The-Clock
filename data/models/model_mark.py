from data.data_base import DataBase
from datetime import datetime

#Registra hora de entrada en la base de datos
def insert_mark_start(idPersonal, hour, date):
        #Consultamos si el funcionario ya marco la entrada del dia
        search_mark_sql =  f"""
                SELECT * FROM MARCAS WHERE FECHA='{date}'
        """ 
        db = DataBase()
        result = db.ejecutar_sql(search_mark_sql)          
        
        if len(result) == 0:

                insert_mark_sql = f"""
                        INSERT INTO MARCAS(HORA_ENTRADA, FECHA, ID_EMPLEADO)
                        VALUES ('{hour}','{date}','{idPersonal}')
                """

                db = DataBase()
                db.ejecutar_sql(insert_mark_sql)
                return 'Marca entrada ingresda', 200
        else:
                return 'Ya esta ingresada la marca de entrada', 200


#Registra hora de salida en la base de datos
def insert_mark_end(idPersonal, hour, date):

        duration = calcDuration(idPersonal, hour, date)

        insert_mark_sql = f"""
                UPDATE MARCAS SET HORA_SALIDA='{hour}', DURACION='{duration}' WHERE FECHA='{date}' AND ID_EMPLEADO='{idPersonal}'
        """
        db = DataBase()
        db.ejecutar_sql(insert_mark_sql)


        return 'Marca Salida ingresada', 200


def calcDuration(idPersonal, hour_end, date):
        db = DataBase()

        #Seleccionamos hora de entrda 
        select_markstart_sql =  f"""
                SELECT * FROM MARCAS WHERE ID_EMPLEADO='{idPersonal}' AND FECHA='{date}'
        """ 
        mark_start = db.ejecutar_sql(select_markstart_sql)

        # calcular duracion
        hour_start = mark_start[0][1]
        FMT = '%H:%M:%S'
        result = datetime.strptime(hour_end, FMT) - datetime.strptime(hour_start, FMT)
        return result


#Indidencia
#1) Obtener datos de los empreados que trabajan hoy
#2) Obtener horarios y verificar si hay marca de salida y entreda  sino no hay marca se ingresa falta
#3) Si falta una u otra marca se ingresa falata x marca.
#4) el el funcionario no tenia libre ingresar libre