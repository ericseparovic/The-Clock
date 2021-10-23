let HTMLLI = document.querySelector('.employee');
let HTMLSubmenu = document.querySelector('.sub_menu');
let HTMLbtnBar = document.querySelector('.header_company');
let HTMLSideBar = document.querySelector('.nav_company');


HTMLLI.addEventListener('click', showSubMenu);
HTMLbtnBar.addEventListener('click', showSideBar);

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



// // Muestra el submenu cuando estamos en la pagina registrar usuario
// window.addEventListener("load", hola);

// function hola(e){
//         url = window.location.pathname
//         if(url == '/register_personal'){
//                 showSubMenu()
//         }
// }
