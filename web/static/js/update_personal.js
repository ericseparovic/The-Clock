let btnActualizar = document.querySelector('#btnActualizarPersonal')
let form = document.querySelector('formActualizarPersonal')
btnActualizar.addEventListener('click', update);

function update(e){
    e.preventDefault()
    url = location.href
    print(url)
}