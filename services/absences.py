from data.models import model_absences
from data.models import model_mark

#Inserta las fechas de ausencia de un trabajador, licencias, libres. 
def insert_authorized_absences(idPersonal, dateAbsence, reason):
    return model_absences.insert_authorized_absences(idPersonal, dateAbsence, reason)


#Eliminar registro de ausencia
def delete_authorized_absence(idAbsence):
    return model_absences.delete_authorized_absence(idAbsence)

#Actualizar fechas ausencia
def update_authorized_absence(idAbsence, dateAbsence, reason):
    return model_absences.update_authorized_absence(idAbsence, dateAbsence, reason)
    
#Obtener Fechas de ausencia  por periodo
def get_authorized_absence(idPersonal, currentDate):
    return model_absences.get_authorized_absence(idPersonal, currentDate)


#Insierta incidencia de libre o falta en la tabla marcas
def attendanceControl(idCompany, currentDate, currentTime):
    return model_mark.attendanceControl(idCompany, currentDate, currentTime)


#se valida el formulario
def validation_form_absences(date, reason):
    if date == '':
        return 'Debe indicar indicar fecha de falta', 412
    if reason == '':
            return 'Debe indicar motivo', 412
    return True