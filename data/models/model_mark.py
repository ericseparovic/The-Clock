from data.data_base import DataBase

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
        insert_mark_sql = f"""
                UPDATE MARCAS SET HORA_SALIDA='{hour}' WHERE FECHA='{date}'
        """
        db = DataBase()
        db.ejecutar_sql(insert_mark_sql)
        return 'Marca Salida ingresada', 200
