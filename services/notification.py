from data.models import model_notification

#Obtiene las notificaciones por empresa
def get_notification(idCompnay):
    return model_notification.get_notification(idCompnay)

#Guarda noficaciones en la base de datos notificaciones.
def insert_notification(date, currentTime, subject, description, status, idPersonal, idCompany):
    return model_notification.insert_notification(date, currentTime, subject, description, status, idPersonal, idCompany)


#Acutaliza estado de la notificaciones
def update_notification(idNotification):
    return model_notification.update_notification(idNotification)