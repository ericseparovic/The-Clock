let htmlForm = document.querySelector('form');
htmlForm.addEventListener('submit', getDateForm);


//Obtiene los datos del formulario
function getDateForm(e) {

    let form = new FormData(htmlForm);
    let name = form.get('name');
    let tel = form.get('tel');
    let email = form.get('email');
    let password = form.get('password');
    let passwordRepeat = form.get('passwordRepeat');
    let messageErrorFront = document.querySelector('.errorFront');
    let messageErrorBack = document.querySelector('.errorBack');




    if(validationForm(name, tel, email, password, passwordRepeat) == true){
        //Limpiar errores y enviar datos al servidor
        messageErrorFront.style.visibility = 'hidden';

    } else {
        // Mostar error y detener envio de datos al seridor
        e.preventDefault();
        messageErrorFront.innerHTML = error
        messageErrorFront.style.visibility = 'visible';

        if(messageErrorBack != null) {
            messageErrorBack.style.visibility = 'hidden';

        }
    }
}


// Valida que los campos no esten vacios
function validationForm(name, tel, email, password, passwordRepeat){

    error = true

    if(name == ''){
        return error = 'Nombre es requerido';
    }

    if(tel == ''){
        return error = 'Telefono es requerido';
    }

    if(email == ''){
        return error = 'Email es requerido';
    }

    if(password == ''){
        return error = 'Clave es requerida';
    }

    if(passwordRepeat == ''){
        return error = 'Clave es requerida';
    }

    if(password != passwordRepeat){
        return error = 'Las claves deben ser iguales'
    }

    return error
}
