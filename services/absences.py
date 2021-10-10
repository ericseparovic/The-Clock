from data.models import model_absences
from data.models import model_mark

#Inserta las fechas de ausencia de un trabajador, licencias, libres. 
def insert_absence(idPersonal, dateAbsence, reason):
    return model_absences.insert_absence(idPersonal, dateAbsence, reason)


#Eliminar registro de ausencia
def delete_absence(idAbsence):
    return model_absences.delete_absence(idAbsence)

#Actualizar fechas ausencia
def update_absence(idAbsence, dateAbsence, reason):
    return model_absences.update_absence(idAbsence, dateAbsence, reason)
    
#Obtener Fechas de ausencia  por periodo
def get_absence_by_date(startDate, endDate):
    return model_absences.get_absence_by_date(startDate, endDate)


#Insierta incidencia de libre o falta en la tabla marcas
def attendanceControl(idCompany, currentDate, currentTime):
    return model_mark.attendanceControl(idCompany, currentDate, currentTime)