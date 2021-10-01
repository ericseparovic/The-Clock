from data.models import model_mark

#Inserta marca de entrada
def insert_mark_start(idPersonal, hour, date):
    return model_mark.insert_mark_start(idPersonal, hour, date)

#Inserta marca de salida
def insert_mark_end(idPersonal, hour, date):
    return model_mark.insert_mark_end(idPersonal, hour, date)


#Actualiza datos marca de entrda y salida



#Inserta incidencia