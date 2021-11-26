
import requests
from werkzeug.wrappers import response

from services import rest_api

#Registar personal
def register_personal(document, name, lastname, gender, birthday, tel, address, email, idCompany):
    body = {
        'document': document,
        'name': name,
        'lastname': lastname,
        'gender': gender,
        'birthday': birthday,
        'tel': tel,
        'address': address,
        'email': email,
        'idCompany': idCompany
    }

    response = requests.post(f'{rest_api.URL_API}/register_personal', json=body)
    return response


def get_all_personal(idCompany):
    body = {
        'idCompany': idCompany
    }
    
    response = requests.get(f'{rest_api.URL_API}/get_all_personal', json=body)
    return response



def delete_personal(idPersonal):
    response = requests.get(f'{rest_api.URL_API}/delete_personal/{idPersonal}')
    return response


def update_personal(document, name, lastname, gender, birthday, tel, address, idPersonal):
    body = {
        'document': document,
        'name': name,
        'lastname': lastname,
        'gender': gender,
        'birthday': birthday,
        'tel': tel,
        'address': address
    }

    response = requests.post(f'{rest_api.URL_API}/update_personal/{idPersonal}', json=body)
    return response

def get_personal(idPersonal):
    response = requests.get(f'{rest_api.URL_API}/get_personal/{idPersonal}')
    return response


def assign_schedule(workStart, workEnd, idPersonal):
    body = {
        'workStart': workStart,
        'workEnd': workEnd,
    }
    response = requests.post(f'{rest_api.URL_API}/insert_schedule/{idPersonal}', json=body)
    return response

def assign_days_off(startDate, endDate, reason, idPersonal):
    body = {
        'startDate': startDate,
        'endDate': endDate,
        'reason': reason
    }
    response = requests.post(f'{rest_api.URL_API}/insert_authorized_absences/{idPersonal}', json=body)
    return response


def register_mark(date, hourStart, hourEnd, idPersonal):
    body = {
        'date': date,
        'hourStart': hourStart,
        'hourEnd': hourEnd,
        'idPersonal': idPersonal
    }
    response = requests.post(f'{rest_api.URL_API}/insert_marks/{idPersonal}', json=body)
    return response
    

def get_absences(idCompany):
    response = requests.get(f'{rest_api.URL_API}/get_absences/{idCompany}')
    print(response)
    return response


def get_all_absence(idPersonal):   
    response = requests.get(f'{rest_api.URL_API}/get_authorized_absence/{idPersonal}')
    return response  


def delete_absence(idAbsence):
    response = requests.delete(f'{rest_api.URL_API}/delete_authorized_absence/{idAbsence}')
    return response

def get_late_arrivals(idCompany):
    response = requests.get(f'{rest_api.URL_API}/get_late_arrivals/{idCompany}')
    return response

def get_early_departure(idCompany):
    response = requests.get(f'{rest_api.URL_API}/get_early_departure/{idCompany}')
    return response

def get_marks(startDate, endDate, document, idCompany):

    body = {
        'startDate': startDate,
        'endDate': endDate,
        'document': document,
        'idCompany': idCompany
    }
    response = requests.get(f'{rest_api.URL_API}/get_marks', json=body)
    return response

def post_mark_start(idPersonal):
    print('post mark start')

    response = requests.post(f'{rest_api.URL_API}/mark_start/{idPersonal}')
    print(response)
    return response

def post_mark_end(idPersonal):
    print('post mark end')
    response = requests.post(f'{rest_api.URL_API}/mark_end/{idPersonal}')
    return response

