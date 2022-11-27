const hamburger = document.getElementById("hamburger");

hamburger.onclick = () => {
    document.getElementById("hero").classList.add("sidebar-activate");
    document.body.classList.add('side-bar-activate-body');
    document.getElementById("page").classList.add('side-bar-activate-body');
    document.getElementById("hero").classList.add('side-bar-activate-body');
}

const sidebarBack = document.getElementById("side-back");

sidebarBack.onclick = () => {
    document.getElementById("hero").classList.remove("sidebar-activate");
    document.body.classList.remove('side-bar-activate-body');
}

