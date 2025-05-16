document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('searchButton');
    const input = document.getElementById('searchInput');

    searchBtn.addEventListener('click', () => {
        const codigo = input.value.trim();

        if (codigo === '') {
            alert('Digite um código de consulta.');
            return;
        }

        fetch(`/consulta/${codigo}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Código não encontrado');
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('usuarioNome').textContent = data.nome_usuario;
                document.getElementById('nomeOriginal').textContent = data.nome_original;

                const arquivoURL = `/static/uploads/documentos/${data.nome_armazenado}`;
                const downloadLink = document.getElementById('downloadLink');
                downloadLink.href = arquivoURL;

                const previewArea = document.getElementById('previewArea');
                previewArea.innerHTML = ''; // Limpa conteúdo anterior

                const extensao = data.nome_armazenado.split('.').pop().toLowerCase();

                if (['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'].includes(extensao)) {
                    const img = document.createElement('img');
                    img.src = arquivoURL;
                    img.alt = 'Visualização';
                    img.style.maxWidth = '100%';
                    img.style.maxHeight = '300px';
                    previewArea.appendChild(img);
                } else if (extensao === 'pdf') {
                    const iframe = document.createElement('iframe');
                    iframe.src = arquivoURL;
                    iframe.width = '100%';
                    iframe.height = '400px';
                    iframe.style.border = '1px solid #ccc';
                    previewArea.appendChild(iframe);
                } else {
                    const msg = document.createElement('p');
                    msg.textContent = 'Visualização não suportada para este tipo de arquivo.';
                    previewArea.appendChild(msg);
                }

                // Exibe o popup
                document.getElementById('popup').classList.remove('hidden');
            })
            .catch(error => {
                alert('Consulta não encontrada ou erro ao buscar dados.');
                console.error(error);
            });
    });
});

function fecharPopup() {
    document.getElementById('popup').classList.add('hidden');
}
