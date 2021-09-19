from data.models import model_mark

def insert_mark_start(idPersonal, hour, date):
    return model_mark.insert_mark_start(idPersonal, hour, date)\

def insert_mark_end(idPersonal, hour, date):
    return model_mark.insert_mark_end(idPersonal, hour, date)