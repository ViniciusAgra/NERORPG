// script.js

function toggleMenu() {
    const nav = document.querySelector('nav ul');
    nav.classList.toggle('active');
}

document.addEventListener("DOMContentLoaded", () => {
    const menuButton = document.querySelector(".menu-toggle");
    menuButton.addEventListener("click", toggleMenu);
});

document.addEventListener("DOMContentLoaded", function () {
    const titulo = document.querySelector("h1");
    const texto = " N.E.R.O.";
    let index = 0;

    titulo.textContent = ""; // Limpa o conteúdo inicial

    function digitar() {
        if (index < texto.length) {
            titulo.textContent += texto[index];
            index++;
            setTimeout(digitar, 100); // Tempo entre cada letra
        }
    }

    digitar();
});