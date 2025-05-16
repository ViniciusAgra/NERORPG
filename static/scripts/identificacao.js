document.addEventListener("DOMContentLoaded", () => {
    const searchButton = document.getElementById("searchButton");
    const searchInput = document.getElementById("searchInput");

    searchButton.addEventListener("click", () => {
        const termo = searchInput.value.trim();
        if (termo) {
            console.log("Buscar por:", termo);
            // Você pode substituir por uma requisição futura
            alert("Busca simulada por: " + termo);
        }
    });
});

function toggleMenu() {
    const nav = document.querySelector('nav ul');
    nav.classList.toggle('active');
}
