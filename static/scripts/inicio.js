document.addEventListener("DOMContentLoaded", () => {
    const titulo = document.querySelector("h1");
    
    setTimeout(() => {
        titulo.classList.add('visible');
    }, 500);
});

function toggleMenu() {
    const nav = document.querySelector('nav ul');
    nav.classList.toggle('active');
}
