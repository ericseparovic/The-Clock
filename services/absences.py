from data.models import model_absences

#Inserta las fechas de ausencia de un trabajador, licencias, libres. 
def insert_absence(idPersonal, startDate, endDate, reason):
    return model_absences.insert_absence(idPersonal, startDate, endDate, reason)


#Eliminar Fecha ausencia


#Actualizar fecha ausencia


#Obtener Fechas de ausencia  por periodo