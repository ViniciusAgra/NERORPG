async function buscarUsuario() {
  const id = document.getElementById('buscar_identificador').value.trim();
  if (!id) return alert("Informe um identificador.");

  try {
    const res = await fetch(`/api/usuario/${id}`);
    const dados = await res.json();

    if (res.ok) {
      document.getElementById('edit_identificador').value = dados.identificador;
      document.getElementById('edit_nome').value = dados.nome;
      document.getElementById('edit_email').value = dados.email;
      document.getElementById('edit_senha').value = dados.senha;
      document.getElementById('edit_patente').value = dados.patente;
      document.getElementById('editar_form').style.display = 'block';
    } else {
      alert(dados.erro || "Usuário não encontrado.");
    }
  } catch (err) {
    alert("Erro ao buscar usuário.");
    console.error(err);
  }
}

async function editarUsuario(event) {
  event.preventDefault();

  const id = document.getElementById('edit_identificador').value;
  const data = {
    nome: document.getElementById('edit_nome').value,
    email: document.getElementById('edit_email').value,
    senha: document.getElementById('edit_senha').value,
    patente: document.getElementById('edit_patente').value,
  };

  try {
    const res = await fetch(`/api/usuario/${id}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const result = await res.json();
    alert(result.success ? 'Usuário atualizado.' : 'Erro: ' + (result.erro || 'Falha desconhecida'));
  } catch (err) {
    alert("Erro ao atualizar.");
    console.error(err);
  }
}

async function excluirUsuario() {
  const id = document.getElementById('edit_identificador').value;
  if (!confirm("Deseja realmente excluir este usuário?")) return;

  try {
    const res = await fetch(`/api/usuario/${id}`, { method: 'DELETE' });
    const result = await res.json();

    if (result.success) {
      alert("Usuário excluído.");
      document.getElementById('editar_form').reset();
      document.getElementById('editar_form').style.display = 'none';
    } else {
      alert("Erro ao excluir usuário.");
    }
  } catch (err) {
    alert("Erro ao excluir.");
    console.error(err);
  }
}

function gerarRelatorio() {
  fetch('/usuarios/relatorio')
    .then(response => {
      if (!response.ok) throw new Error('Erro ao gerar relatório');
      return response.blob();
    })
    .then(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'Relatório Agentes NERO.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
    })
    .catch(error => {
      alert('Erro ao baixar relatório: ' + error.message);
    });
}
