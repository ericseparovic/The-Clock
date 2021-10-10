from data.models import model_notification

#Obtiene las notificaciones por empresa
def get_notification(idCompnay, status):
    return model_notification.get_notification(idCompnay, status)