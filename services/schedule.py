from data.models import model_shedule


#Asigna horario a funcionario
def insert_schedule(workStart, workEnd, idPersonal):
    return model_shedule.insert_schedule(workStart, workEnd, idPersonal)