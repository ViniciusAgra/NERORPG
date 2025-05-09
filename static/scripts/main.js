function toggleMenu() {
    const nav = document.querySelector('nav ul');
    nav.classList.toggle('active');
}
//Lida Com A Animação De Digitar Da NERO
document.addEventListener("DOMContentLoaded", () => {
    const titulo = document.querySelector("h1");
    const texto = " N.E.R.O.";
    let index = 0;

    titulo.textContent = "";

    function digitar() {
        if (index < texto.length) {
            titulo.textContent += texto[index];
            index++;
            setTimeout(digitar, 100);
        } else {
            esperarCliqueParaAnimar();
        }
    }

    digitar();

    const scrollContainer = document.getElementById("scroll-container");
    const scrollZone = document.querySelector(".scroll-hover-zone");

    scrollContainer.classList.add("scroll-hidden");

    scrollZone.addEventListener("mouseenter", () => {
        scrollContainer.classList.remove("scroll-hidden");
        scrollContainer.classList.add("scroll-visible");
    });

    scrollZone.addEventListener("mouseleave", () => {
        scrollContainer.classList.remove("scroll-visible");
        scrollContainer.classList.add("scroll-hidden");
    });
});

// Espera o primeiro clique do usuário para iniciar animação e som
function esperarCliqueParaAnimar() {
    const iniciar = () => {
        subirTituloEExibirTexto();
        document.removeEventListener("click", iniciar);
    };

    document.addEventListener("click", iniciar);
}
// Lida Com A Animação De Subir E A Render Do Formulario
function subirTituloEExibirTexto() {
    const titulo = document.querySelector("h1");
    titulo.style.transform = "translateY(-100px)";
    titulo.style.opacity = "0";

    // Tocar o áudio de boas-vindas
    const audio = document.getElementById("boas-vindas");
    if (audio) {
        audio.play().catch(err => {
            console.warn("Áudio de boas-vindas bloqueado:", err);
        });
    }

    setTimeout(() => {
        const loginForm = document.getElementById("login-form");
        loginForm.classList.remove("hidden");
        requestAnimationFrame(() => {
            loginForm.classList.add("visible");
        });
    }, 1000);
}

// Lida com login e Easter Egg
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            const formData = new FormData(this);
            const identificador = formData.get('identificador');
            const senha = formData.get('senha');

            const response = await fetch('/login', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                window.location.href = '/inicio';
            } else {
                const errorDiv = document.getElementById('login-error');
                errorDiv.textContent = result.message;
                errorDiv.classList.remove('hidden');

                // Easter egg: se tentativa com "Nero", toca áudio especial
                if (identificador === 'Nero' && senha === 'Nero') {
                    const audio = document.getElementById('easteregg-audio');
                    if (audio) {
                        audio.play().catch(err => console.warn('Erro ao tocar áudio easter egg:', err));
                    }
                }
            }
        });
    }
});

//Lida com o AutoComplete
document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('#loginForm input');

    inputs.forEach(input => {
        input.setAttribute('autocomplete', 'off');

        input.addEventListener('input', () => {
            input.setAttribute('autocomplete', 'on');
        });
    });
});

