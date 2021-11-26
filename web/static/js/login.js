let htmlForm = document.querySelector('form');

// Obtiene los datos del formulario login
htmlForm.addEventListener('submit', getDateForm)

function getDateForm(e) {

    let form = new FormData(htmlForm)
    let email = form.get('email')
    let password = form.get('password')
    let messageErrorFront = document.querySelector('.errorFront');
    let messageErrorBack = document.querySelector('.errorBack');




    if(validationForm(email, password) == true){
        //Limpiar errores y enviar datos al servidor
        messageErrorFront.style.visibility = 'hidden';

    } else {
        // Mostar error y detener envio de datos al seridor
        e.preventDefault();
        messageErrorFront.innerHTML = error
        messageErrorFront.style.visibility = 'visible';
        
        if(messageErrorBack !== null){
            messageErrorBack.style.visibility = 'hidden';
        }

    }
}



// Valida que los campos no esten vacios
function validationForm(email, password){
    error = true

    if(email == ""){
        return error = "Email es requerido"
    } 

    if(password == ""){
        return error = "Contraseña es requerida"
    }

    return error
}
