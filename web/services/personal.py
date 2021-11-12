
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

def assign_days_off(date, reason, idPersonal):
    body = {
        'date': date,
        'reason': reason
    }
    response = requests.post(f'{rest_api.URL_API}/insert_authorized_absences/{idPersonal}', json=body)
    return response
    