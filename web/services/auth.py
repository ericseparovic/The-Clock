import requests

from services import rest_api

#Crear usuario
def create_user(name, tel, email, password, passwordRepeat):
    body = {
        'name': name,
        'tel': tel,
        'email': email,
        'password': password,
        'passwordRepeat': passwordRepeat
    }

    response = requests.post(f'{rest_api.URL_API}/signup', json=body)
    return response


#Login empresa