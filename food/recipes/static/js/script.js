const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.hide-menu-mobile');


menuToggle.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    if(menuToggle.classList.contains('fa-bars')){
        menuToggle.classList.remove('fa-bars');
        menuToggle.classList.add('fa-times');
    }
    else{
        menuToggle.classList.remove('fa-times');
        menuToggle.classList.add('fa-bars');
    }
});

