from data.data_base import DataBase
from data.models import model_personal


#Obtiene notificaciones
def get_notification(idCompany):
    select_notification_sql = f"""
        SELECT * FROM NOTIFICACIONES WHERE ESTADO='Pendiente' AND ID_EMPRESA='{idCompany}'
    """
    db = DataBase()    
    notifications = []

    print('idCompany', idCompany)
    for notification in db.ejecutar_sql(select_notification_sql):
        
        data_personal = model_personal.get_personal(notification[6])

        name = data_personal[0]['name']
        lastName = data_personal[0]['lastName']
        document = data_personal[0]['document']


        dict_notification = {
        'idNotification': notification[0],
        'date': notification[1],
        'time': notification[2],
        'subject': notification[3],
        'description': notification[4],
        'status': notification[5],
        'idPersonal': notification[6],
        'idCompany': notification[7],
        'name': name,
        'lastName': lastName,
        'document': document
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

#Actualizar estado
def update_notification(idNotification):

    try:
        update_notification_sql = f"""
            UPDATE NOTIFICACIONES SET ESTADO='Hecho' WHERE ID_NOTIFICACION='{idNotification}'
            """
        db = DataBase()
        db.ejecutar_sql(update_notification_sql)
        return "Hecho", 200
    except:
        return "No se pudo actualizar notificacion", 412
