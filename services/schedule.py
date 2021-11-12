from data.models import model_shedule


#Asigna horario a funcionario
def insert_schedule(workStart, workEnd, idPersonal):
    return model_shedule.insert_schedule(workStart, workEnd, idPersonal)



def validation_form_schedule(workStart, workEnd, idPersonal):
    if workStart == '':
        return 'Debe ingresar hora de entrada', 412
    if workEnd == '':
        return 'Debe ingresar hora de salida', 412
    if idPersonal == '':
        return 'Debe seleccionar un funcionario', 412
    return True