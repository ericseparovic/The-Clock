from data.data_base import DataBase

#Obtiene notificaciones
def get_notification(idCompany, status):
    select_notification_sql = f"""
        SELECT * FROM NOTIFICACIONES WHERE ESTADO='{status}' AND ID_EMPRESA='{idCompany}'
    """
    db = DataBase()    
    notifications = []

    for notification in db.ejecutar_sql(select_notification_sql):
            dict_notification = {
            'idNotificacion': notification[0],
            'fecha': notification[1],
            'hora': notification[2],
            'asunto': notification[3],
            'descripcion': notification[4],
            'estado': notification[5],
            'idEmpleado': notification[6],
            'idEmpresa': notification[7]
            }

            notifications.append(dict_notification)
    return notifications



def insert_notification(date, currentTime, subject, description, status, idPersonal, idCompany):

        #Inserta notificaciones
        insert_notification_sql = f"""
                INSERT INTO NOTIFICACIONES(FECHA_NOTIFICACION, HORA, ASUNTO, DESCRIPCION, ESTADO, ID_EMPLEADO, ID_EMPRESA)
                VALUES ('{date}', '{currentTime}','{subject}','{description}', '{status}', '{idPersonal}', '{idCompany}')
        """

        db = DataBase()
        db.ejecutar_sql(insert_notification_sql)
        return True