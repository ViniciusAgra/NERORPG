function toggleMenu() {
    const nav = document.querySelector('nav ul');
    nav.classList.toggle('active');
}

document.addEventListener("DOMContentLoaded", () => {
    const titulo = document.querySelector("h1");
    const texto = " N.E.R.O.";
    let index = 0;

    titulo.textContent = ""; // Limpa o conteúdo inicial

    function digitar() {
        if (index < texto.length) {
            titulo.textContent += texto[index];
            index++;
            setTimeout(digitar, 100);
        } else {
            subirTituloEExibirTexto();
        }
    }

    digitar();

    // Controle da exibição da barra de rolagem
    const scrollContainer = document.getElementById("scroll-container");
    const scrollZone = document.querySelector(".scroll-hover-zone");

    // Oculta a barra por padrão
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

function subirTituloEExibirTexto() {
    const titulo = document.querySelector("h1");
    titulo.style.transform = "translateY(-100px)";
    titulo.style.opacity = "0";

    setTimeout(() => {
        const descricao = document.getElementById("descricao");
        descricao.classList.add("visible");

        const textoDescricao = `
        
Fundada em 451 E.C, a Neyt Eter Rognus Opomun (Novo Caminho do Destino Universal), mais conhecida como N.E.R.O., é uma instituição de segurança interdimensional dedicada à proteção e manutenção da ordem no Plano Terreno.

Desde sua fundação, Adam Zephyros enxergou na corporação um imenso potencial para zelar pela paz. No entanto, após sua morte em 1128 E.C, a N.E.R.O. expandiu seus objetivos, passando a atuar não apenas na segurança pública e privada, mas também no avanço tecnológico humano, sempre em equilíbrio com o desenvolvimento e a cooperação entre as demais raças que habitam o Plano Terreno.

Atualmente, a corporação é liderada por Sete (7), presidente e diretora executiva, sendo a terceira governante da organização desde o falecimento de seu fundador. Em 3036, a N.E.R.O. conta com 46 sedes espalhadas pelo mundo, com sua matriz e centro de comando operacional situados em Londres, Inglaterra, União Europeia. Além disso, dispõe de meios de transporte avançados que garantem locomoção entre todas as unidades, desde A1 até F4, incluindo bases em Vênus e Marte.

No dia 21 de maio de 3036, a N.E.R.O. completará 2.585 anos de existência, consolidando-se como a maior e mais influente empresa de segurança pública e privada do mundo.`;

        descricao.textContent = textoDescricao;
    }, 1000);
}
