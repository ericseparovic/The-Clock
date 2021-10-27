
import requests

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