document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector(".upload-form");
    const fileInput = form.querySelector("input[type='file']");

    form.addEventListener("submit", function (event) {
        const file = fileInput.files[0];
        const maxSize = 1024 * 1024 * 1024; // 1 GB

        if (file && file.size > maxSize) {
            alert("O arquivo é muito grande. O limite é de 1 GB.");
            event.preventDefault(); // Cancela o envio
        }
    });
});
