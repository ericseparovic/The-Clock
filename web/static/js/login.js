let htmlForm = document.querySelector('form');

// Obtiene los datos del formulario login
htmlForm.addEventListener('submit', getDateForm)

function getDateForm(e) {
    e.preventDefault();

    let form = new FormData(htmlForm)
    let userName = form.get('email')
    let password = form.get('password')

    let messageError = document.querySelector('.emptyFieldsError');

    if(validationForm(userName, password) == false){
        // Mostrar error
        messageError.style.visibility = 'visible';
    } else {
        // Borrar error
        messageError.style.visibility = 'hidden';
    }
}


// Valida que los campos no esten vacios
function validationForm(userName, password){


    if(userName == ""){
        return false
    } else if(password == "") {
        return false
    } else {
        return true
    }
}
