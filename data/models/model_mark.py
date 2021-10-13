from data.data_base import DataBase
from datetime import datetime
from data.models import model_personal
from data.models import model_absences
from data.models import model_notification

#Registra hora de entrada en la base de datos
def insert_mark_start(idPersonal, currentTime, date):

        #Consultamos si el funcionario ya marco la entrada del dia
        search_mark_sql =  f"""
                SELECT * FROM MARCAS WHERE FECHA='{date}' AND ID_EMPLEADO='{idPersonal}'
        """ 
        db = DataBase()
        result = db.ejecutar_sql(search_mark_sql)          
        
        if len(result) == 0:
                schedule = get_schedule(idPersonal)
                if schedule:
                        hourStart = schedule[0][1]
                        incidence = incident_hour_start(currentTime, hourStart)

                        if incidence == 'Tarde':
                                
                                insert_mark_sql = f"""
                                        INSERT INTO MARCAS(HORA_ENTRADA, FECHA, INCIDENCIA_HORARIO_ENTRADA, ID_EMPLEADO)
                                        VALUES ('{currentTime}','{date}','Tarde','{idPersonal}')
                                """

                                db = DataBase()
                                db.ejecutar_sql(insert_mark_sql)
                        
                                return 'Marca entrada ingresda', 200
                        else:
                                insert_mark_sql = f"""
                                        INSERT INTO MARCAS(HORA_ENTRADA, FECHA, INCIDENCIA_HORARIO_ENTRADA, ID_EMPLEADO)
                                        VALUES ('{currentTime}','{date}','En Hora','{idPersonal}')
                                """

                                db = DataBase()
                                db.ejecutar_sql(insert_mark_sql)
                                return 'Marca entrada ingresda', 200
                else:
                        #Si el empleado no tiene horario asignado, se guarda la incidencia en tabla notificaciones para que el usuario administrador, ingrese los datos manualmente y le asigne el horario laboral
                        subject = 'No tiene horario asigando'
                        description = "Funcionario realizo marca de entrada y no tiene hroario asigando, asigne horario e ingrese la marcas manualmente"
                        status = 'Pendiente'
                        idCompany = get_id_company(idPersonal)

                        model_notification.insert_notification(date, currentTime, subject, description, status, idPersonal, idCompany)
                        return 'No tiene horario asignado', 200
        else:
                return 'Ya ingreso marca de entrada', 200


#Registra hora de salida en la base de datos
def insert_mark_end(idPersonal, currentTime, date):
        #Otiene id empresa
        idCompany = get_id_company(idPersonal)
        print(idCompany)
        
        schedule = get_schedule(idPersonal)
        if schedule:
                hourEnd = schedule[0][2]
                try:
                        duration = calcDuration(idPersonal, currentTime, date)
                except:
                        subject = 'No tiene horario asigando'
                        description = "Funcionario realizo marca y no tiene hroario asigando"
                        status = 'Pendiente'
                        idCompany = get_id_company(idPersonal)

                        model_notification.insert_notification(date, currentTime, subject, description, status, idPersonal, idCompany)
                        return "No tiene horario asignado, se informo al administrador", 200


                incident = incident_hour_end(currentTime, hourEnd)
                if currentTime < hourEnd:
                        insert_mark_sql = f"""
                                UPDATE MARCAS SET HORA_SALIDA='{currentTime}', DURACION='{duration}', INCIDENCIA_ASISTENCIA='Asistio', INCIDENCIA_HORARIO_SALIDA='{incident}' WHERE FECHA='{date}' AND ID_EMPLEADO='{idPersonal}'
                        """
                        db = DataBase()
                        db.ejecutar_sql(insert_mark_sql)
                        return 'Marca Salida ingresada', 200
                else:
                        insert_mark_sql = f"""
                                UPDATE MARCAS SET HORA_SALIDA='{currentTime}', DURACION='{duration}', INCIDENCIA_ASISTENCIA='Asistio', INCIDENCIA_HORARIO_SALIDA='{incident}' WHERE FECHA='{date}' AND ID_EMPLEADO='{idPersonal}'
                        """
                        db = DataBase()
                        db.ejecutar_sql(insert_mark_sql)
                        return 'Marca Salida ingresada', 200
        else:
                subject = 'No tiene horario asigando'
                description = "Funcionario realizo marca de salida y no tiene hroario asigando, asigne horario e ingrese marca manualmente"
                status = 'Pendiente'
                idCompany = get_id_company(idPersonal)

                model_notification.insert_notification(date, currentTime, subject, description, status, idPersonal, idCompany)
                return "No tiene horario asignado, se informo al administrador", 200


def calcDuration(idPersonal, currentTime, date):

        #Seleccionamos hora de entrda 
        select_markstart_sql =  f"""
                SELECT * FROM MARCAS WHERE ID_EMPLEADO='{idPersonal}' AND FECHA='{date}'
        """ 
        db = DataBase()
        mark_start = db.ejecutar_sql(select_markstart_sql)

        
        # calcular duracion
        hour_start = mark_start[0][1]
        FMT = '%H:%M:%S'
        result = datetime.strptime(currentTime, FMT) - datetime.strptime(hour_start, FMT)
        return result


#Si el funcionario tiene horario asignado se obtiene el id. En  caso contrario retorna false
def get_id_schedule(idPersonal):
        #Seleccionamos hora de entrda 
        select_schedule_sql =  f"""
                SELECT ID_HORARIO FROM EMPLEADOS WHERE ID_EMPLEADO='{idPersonal}'
        """ 
        db = DataBase()
        result = db.ejecutar_sql(select_schedule_sql) 
        
        if result:
                return result[0][0]
        else:
                return False

#Obtiene horario de entrada y horario de salida
def get_schedule(idPersonal):
        idHorario = get_id_schedule(idPersonal)

        if idHorario != False:
                select_schedule_sql =  f"""
                        SELECT * FROM HORARIOS WHERE ID_HORARIO='{idHorario}'
                """ 
                db = DataBase()
                result = db.ejecutar_sql(select_schedule_sql) 
                return result
        else:
                return []


#Funcion encargada de controlar que empleado falto
def attendanceControl(idCompany, currentDate, currentTime):
        #Obtengo todos los empleados activos de la empresa
        employees = model_personal.get_all_personal(idCompany)
        for employee in employees:
                idPersonal = employee['idPersonal']

                # Se consulta hora de salida
                schedule = get_schedule(idPersonal)
                #Se consulta si tiene libre
                absence = model_absences.get_absence_by_id(idPersonal, currentDate)
                #Se consulta si hay marca
                mark = search_mark(idPersonal, currentDate)
                # print(absence[0][''] == currentDate)
                if absence and mark == []:
                        #Se registra en incidencia libre
                        incidence = absence[0]['reason']
                        insert_incidence(idPersonal, incidence, currentDate)
                        
                elif schedule and mark == []:
                        #Se regisra en incidencia falta
                        #Se verifica que el funcionario tenga asiganado un horario
                        #Se verifica si hay mara y si paso el horario de salida
                        if currentTime > schedule[0][2]:
                                incidence = "Falta"
                                insert_incidence(idPersonal, incidence, currentDate)
                
                
#Consulta si hay marca ingresada
def search_mark(idPersonal, currentDate):
        search_mark_sql =  f"""
                SELECT * FROM MARCAS WHERE FECHA='{currentDate}' AND ID_EMPLEADO='{idPersonal}'
        """ 
        db = DataBase()
        result = db.ejecutar_sql(search_mark_sql)  
        return result

#Registra falta en la tabla marcas
def insert_incidence(idPersonal, incidence, currentDate):
        insert_mark_incidence_sql = f"""
                        INSERT INTO MARCAS(HORA_ENTRADA, HORA_SALIDA, FECHA, DURACION, INCIDENCIA_ASISTENCIA, INCIDENCIA_HORARIO_ENTRADA, INCIDENCIA_HORARIO_SALIDA, ID_EMPLEADO)
                        VALUES ('-','-','{currentDate}','-','{incidence}','-','-','{idPersonal}')
                """

        db = DataBase()
        db.ejecutar_sql(insert_mark_incidence_sql)
        
        return True


#Obtiene marcas
def get_mark(document, startDate, endDate, idCompany):
        result = get_id_personal(document, idCompany)
        
        if result:
                idPersonal = result[0][0]

                select_mark_sql =  f"""
                        SELECT * FROM MARCAS WHERE ID_EMPLEADO='{idPersonal}' AND FECHA BETWEEN '{startDate}' AND '{endDate}'
                """ 
                db = DataBase()
                marks = []

                for mark in db.ejecutar_sql(select_mark_sql):
                        dict_mark = {
                        'idMarca': mark[0],
                        'horaEntrada': mark[1],
                        'horaSalida': mark[2],
                        'fecha': mark[3],
                        'duracion': mark[4],
                        'incidenciaAsistencia': mark[5],
                        'incidenciaHoraEntrada': mark[6],
                        'incidenciaHoraSalida': mark[7],
                        'idEmpleado': mark[8]
                        }

                        marks.append(dict_mark)
                return marks
        else:
                return 'Documento o id Empresa incorrecto'

#Obtiene id empleados por numero de documento
def get_id_personal(document, idCompany):
        
        select_id_sql =  f"""
                SELECT ID_EMPLEADO FROM EMPLEADOS WHERE DOCUMENTO='{document}' AND ID_EMPRESA='{idCompany}'
        """ 
        db = DataBase()
        result = db.ejecutar_sql(select_id_sql) 
        return result


def incident_hour_start(currentTime, hourStart):
        if currentTime > hourStart:
                return 'Tarde'
        else:
                return 'En hora'

def incident_hour_end(currentTime, hourEnd):
        if currentTime < hourEnd:
                return 'Anticipado'
        else:
                return 'En hora'

#Inserta marcas manualente solo para usuairos administador
def insert_marks(idPersonal, hourStart, hourEnd, date):
        #Verificamos si ya hay un registro del dia
        #Consulta si hay marca ingresada
        result = search_mark(idPersonal, date)
        duration = calcDurationMark(hourStart, hourEnd)

        schedule = get_schedule(idPersonal)
        if schedule:
                scheduleHourStart = schedule[0][1]
                scheduleHourEnd = schedule[0][2]
      
                incidenceStart = incident_hour_start(hourStart, scheduleHourStart)
                incidenceEnd = incident_hour_end(hourEnd, scheduleHourEnd)

                if result: 
                        insert_mark_sql = f"""
                                        UPDATE MARCAS SET HORA_ENTRADA='{hourStart}', HORA_SALIDA='{hourEnd}', FECHA='{date}', DURACION='{duration}', INCIDENCIA_ASISTENCIA='Asistio', INCIDENCIA_HORARIO_ENTRADA='{incidenceStart}', INCIDENCIA_HORARIO_SALIDA='{incidenceEnd}' WHERE FECHA='{date}' AND ID_EMPLEADO='{idPersonal}'
                                """
                        db = DataBase()
                        db.ejecutar_sql(insert_mark_sql)
                        return 'Marca Salida ingresada', 200 
                else:
                        insert_mark_sql = f"""
                                INSERT INTO MARCAS(HORA_ENTRADA, HORA_SALIDA, FECHA, DURACION, INCIDENCIA_ASISTENCIA,INCIDENCIA_HORARIO_ENTRADA, INCIDENCIA_HORARIO_SALIDA, ID_EMPLEADO)
                                VALUES ('{hourStart}','{hourEnd}','{date}', '{duration}' ,'Asistio', '{incidenceStart}', '{incidenceEnd}', '{idPersonal}')
                        """

                        db = DataBase()
                        db.ejecutar_sql(insert_mark_sql)
                
                return 'Marca entrada ingresda', 200







#Actualiza marcas ya registradas
def update_mark(idPersonal, hourStart, hourEnd, idMark):
        duration = calcDurationMark(hourStart, hourEnd)
      
        schedule = get_schedule(idPersonal)
        if schedule:
                #Calcuala si el empleado marco despues de la hora de entrada o antes de la hora de salida
                scheduleHourStart = schedule[0][1]
                scheduleHourEnd = schedule[0][2]
                incidenceStart = incident_hour_start(hourStart, scheduleHourStart)
                incidenceEnd = incident_hour_end(hourEnd, scheduleHourEnd)

                insert_mark_sql = f"""
                        UPDATE MARCAS SET HORA_ENTRADA='{hourStart}', HORA_SALIDA='{hourEnd}', DURACION='{duration}', INCIDENCIA_ASISTENCIA='Asistio',INCIDENCIA_HORARIO_ENTRADA='{incidenceStart}', INCIDENCIA_HORARIO_SALIDA='{incidenceEnd}' WHERE ID_MARCA='{idMark}'
                """
                db = DataBase()
                result = db.ejecutar_sql(insert_mark_sql)
                print(result)
                return 'Marcas ingresadas', 200
        else:
                return 'No tiene horario asignado', 412

#Calcula duracion cuando se ingersa marca manual
def calcDurationMark(hourStart, hourEnd):
        
        FMT = '%H:%M'
        result = datetime.strptime(hourEnd, FMT) - datetime.strptime(hourStart, FMT)
        return result


#Obtiene id empresa
def get_id_company(idPersonal):
        select_company_sql =  f"""
                SELECT ID_EMPRESA FROM EMPLEADOS WHERE ID_EMPLEADO='{idPersonal}'
        """ 
        db = DataBase()
        result = db.ejecutar_sql(select_company_sql) 

        if result:
                return result[0][0]
        else:
                return []



#Obtiene faltas
def get_absences(startDate, endDate, idCompany):

        employees = model_personal.get_all_personal(idCompany)
        absences = []

        for employee in employees:
                idPersonal = employee['idPersonal']


                select_absence_sql =  f"""
                        SELECT * FROM MARCAS WHERE INCIDENCIA_ASISTENCIA='Falta' AND FECHA BETWEEN '{startDate}' AND '{endDate}' AND ID_EMPLEADO='{idPersonal}'
                """ 
                db = DataBase()

                for absence in db.ejecutar_sql(select_absence_sql):
                        dict_absence = {
                        'idFalta': absence[0],
                        'fecha': absence[3],
                        'incidenciaAsistencia': absence[5],
                        'idEmpleado': absence[8]
                        }

                        absences.append(dict_absence)
        return absences

