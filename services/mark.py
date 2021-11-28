from data.models import model_mark

#Inserta marca de entrada
def insert_mark_start(idPersonal, hour, date):
    return model_mark.insert_mark_start(idPersonal, hour, date)

#Inserta marca de salida
def insert_mark_end(idPersonal, hour, date):
    return model_mark.insert_mark_end(idPersonal, hour, date)

#Obtiene marcas 
def get_marks(startDate, endDate, document, idCompany):
    return model_mark.get_marks(startDate, endDate, document, idCompany)

#Inserta marcas manualente solo para usuairos administador
def insert_marks(idPersonal, hourStart, hourEnd, date):
    return model_mark.insert_marks(idPersonal, hourStart, hourEnd, date)

#Actualiza marca ya registrada
def update_mark(idPersonal, hourStart, hourEnd, idMark):
    return model_mark.update_mark(idPersonal, hourStart, hourEnd, idMark)


#Obtiene faltas del dia
def get_absences(currentDate, idCompany):
    return model_mark.get_absences(currentDate, idCompany)


#Obtiene llegadas tardes del dia
def get_late_arrivals(currentDate, idCompany):
    return model_mark.get_late_arrivals(currentDate, idCompany)

#Obtiene cantidad salidas anticipadas
def get_early_departure(currentDate, idCompany):
    return model_mark.get_early_departure(currentDate, idCompany)

#Obtiene cantidad de asistencias del dia
def get_assists(currentDate, idCompany):
    return model_mark.get_assists(currentDate, idCompany)



