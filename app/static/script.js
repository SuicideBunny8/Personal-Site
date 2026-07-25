// mobile nav bar toggle
const menuToggleBtn = document.getElementsByClassName("menu-icon")[0];
const navMenuLinks = document.getElementsByClassName("nav-menu")[0];

menuToggleBtn.addEventListener('click', () => {
    navMenuLinks.classList.toggle('active');
})

// message box timeout
const message_timeout = setTimeout(poof, 10000);

function poof() {
    var items = document.getElementsByClassName("message-box");
    console.log(items);
    if (items.length > 0) {
        var element = items[0];

        var op = 1;  // initial opacity
        var timer = setInterval(function () {
            if (op <= 0.1){
                clearInterval(timer);
                element.style.display = 'none';
            }
            element.style.opacity = op;
            element.style.filter = 'alpha(opacity=' + op * 100 + ")";
            op -= op * 0.1;
        }, 50);
    }
}