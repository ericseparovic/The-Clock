from data.models import model_notification

#Obtiene las notificaciones por empresa
def get_notification(idCompnay, status):
    return model_notification.get_notification(idCompnay, status)

#Guarda noficaciones en la base de datos notificaciones.
def insert_notification(date, currentTime, subject, description, status, idPersonal, idCompany):
    return model_notification.insert_notification(date, currentTime, subject, description, status, idPersonal, idCompany)
