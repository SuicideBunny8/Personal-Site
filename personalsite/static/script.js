const menuToggleBtn = document.getElementsByClassName("menu-icon")[0];
const navMenuLinks = document.getElementsByClassName("nav-menu")[0];

menuToggleBtn.addEventListener('click', () => {
    navMenuLinks.classList.toggle('active');
})