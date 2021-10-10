from data.models import model_mark

#Inserta marca de entrada
def insert_mark_start(idPersonal, hour, date):
    return model_mark.insert_mark_start(idPersonal, hour, date)

#Inserta marca de salida
def insert_mark_end(idPersonal, hour, date):
    return model_mark.insert_mark_end(idPersonal, hour, date)

#Obtiene marcas 
def get_mark(document, startDate, endDate, idComapny):
    return model_mark.get_mark(document, startDate, endDate, idComapny)

#Inserta marcas manualente solo para usuairos administador
def insert_marks(idPersonal, hourStart, hourEnd, date):
    return model_mark.insert_marks(idPersonal, hourStart, hourEnd, date)