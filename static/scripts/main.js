function toggleMenu() {
    const nav = document.querySelector('nav ul');
    nav.classList.toggle('active');
}

// Lida com a animação de digitar N.E.R.O.
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

// Espera o primeiro clique do usuário para iniciar a animação
function esperarCliqueParaAnimar() {
    const iniciar = () => {
        subirTituloEExibirTexto();
        document.removeEventListener("click", iniciar);
    };

    document.addEventListener("click", iniciar);
}

// Animação do título subindo e exibição do formulário
function subirTituloEExibirTexto() {
    const titulo = document.querySelector("h1");
    titulo.style.transform = "translateY(-100px)";
    titulo.style.opacity = "0";

    const audio = document.getElementById("boas-vindas");
    if (audio) {
        audio.play().catch(err => {
            console.warn("Áudio de boas-vindas bloqueado:", err);
        });
    }

    setTimeout(() => {
        const loginFormContainer = document.getElementById("login-form");
        loginFormContainer.classList.remove("hidden");

        requestAnimationFrame(() => {
            loginFormContainer.classList.add("visible");

            // Habilita o botão somente após o formulário aparecer
            const loginButton = loginFormContainer.querySelector("button[type='submit']");
            if (loginButton) {
                loginButton.disabled = false;
            }
        });
    }, 1000);
}

// Lida com o envio do formulário e Easter Egg
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

// Desativa sugestão de preenchimento automático até o usuário começar a digitar
document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('#loginForm input');

    inputs.forEach(input => {
        input.setAttribute('autocomplete', 'off');

        input.addEventListener('input', () => {
            input.setAttribute('autocomplete', 'on');
        });
    });
});
