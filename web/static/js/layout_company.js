let HTMLLI = document.querySelector('.employee');
let HTMLSubmenu = document.querySelector('.sub_menu');
let HTMLbtnBar = document.querySelector('.header-company');
let HTMLSideBar = document.querySelector('.nav-company');
let HTMLHeader = document.querySelector('.header-company')
let HTMLDropDown = document.querySelector('.dropdown');


HTMLLI.addEventListener('click', showSubMenu);
HTMLbtnBar.addEventListener('click', showSideBar);
HTMLHeader.addEventListener('click', showDropDown);

// Muesta el submenu cuando se realiza clic en empleados
function showSubMenu(e){  
        HTMLSubmenu.classList.toggle('active')
}

// Muestra o oculta el menu, cuando se realiza clic en el boton de menu
function showSideBar(e){
        if(e.target.id == 'btnBars'){
                HTMLSideBar.classList.toggle('active');
        }
}


function showDropDown(e){
        if(e.target.className == 'nameUser' || e.target.id == 'imgPerfil'){
                HTMLDropDown.classList.toggle('active')

        }
}

// Muestra el submenu cuando estamos en la pagina registrar usuario
window.addEventListener("load", loadSubMenu);

function loadSubMenu(){
        url = window.location.pathname
        if(url == '/register_personal'){
                showSubMenu()
        }

        if(url == '/list_of_employees'){
                showSubMenu()
        }
}
