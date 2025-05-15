from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, abort, send_file
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
import sqlite3
import os
from functools import wraps

app = Flask(__name__, static_folder='static', template_folder='pages')
app.secret_key = os.urandom(24)

DB_PATH = os.path.join('data', 'users.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('erro_401'))
        return f(*args, **kwargs)
    return decorated_function

def patente_minima(nivel_minimo):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            patente_nome = session.get('patente')
            if not patente_nome:
                return abort(403)

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT nivel FROM patentes WHERE nome = ?', (patente_nome,))
            resultado = cursor.fetchone()
            conn.close()

            if not resultado:
                return abort(403)

            nivel_usuario = resultado['nivel']
            if nivel_usuario > nivel_minimo:
                return abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobrebasic():
    return render_template('sobrebasic.html')

@app.route('/inicio')
@login_required
def inicio():
    nome = session.get('nome')
    tocar_audio = session.pop('tocar_audio', False)
    return render_template('inicio.html', nome=nome, tocar_audio=tocar_audio)

@app.route('/inicio/sobre')
@login_required
def sobre():
    return render_template('sobre.html')

@app.route('/inicio/identificacao')
@login_required
def identificacao():
    return render_template('identificacao.html')

@app.route('/inicio/atribuicoes')
@login_required
def atribuicoes():
    return render_template('atribuicoes.html')

@app.route('/inicio/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@app.route('/login', methods=['POST'])
def login():
    identificador = request.form['identificador']
    senha = request.form['senha']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE identificador = ? AND senha = ?', (identificador, senha))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['usuario_id'] = user['identificador']
        session['nome'] = user['nome']
        session['email'] = user['email']
        session['patente'] = user['patente']
        session['tocar_audio'] = True
        return jsonify(success=True)
    else:
        return jsonify(success=False, message='Agente não localizado no sistema.')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/inicio/cadastro', methods=['GET', 'POST'])
@login_required
@patente_minima(1)
def cadastro():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        identificador = request.form['identificador']
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        patente = request.form['patente']

        try:
            cursor.execute('''
                INSERT INTO users (identificador, nome, email, senha, patente)
                VALUES (?, ?, ?, ?, ?)''',
                (identificador, nome, email, senha, patente)
            )
            conn.commit()
            flash('Cadastro realizado com sucesso.')
        except sqlite3.IntegrityError as e:
            if "users.email" in str(e):
                flash('Erro: Este e-mail já está em uso.')
            elif "users.identificador" in str(e):
                flash('Erro: Este identificador já está em uso.')
            else:
                flash('Erro ao cadastrar.')
    # Sempre buscar as patentes, mesmo no POST, para exibir a lista caso precise mostrar o formulário de novo
    cursor.execute('SELECT * FROM patentes ORDER BY nivel ASC')
    patentes = cursor.fetchall()
    conn.close()

    return render_template('cadastro.html', patentes=patentes)

# Buscar dados de um usuário pelo identificador
@app.route('/api/usuario/<identificador>', methods=['GET'])
@login_required
@patente_minima(1)
def buscar_usuario(identificador):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE identificador = ?', (identificador,))
    usuario = cursor.fetchone()
    conn.close()
    if usuario:
        return jsonify(dict(usuario))
    return jsonify({'erro': 'Usuário não encontrado'}), 404

# Atualizar dados de um usuário
@app.route('/api/usuario/<identificador>', methods=['POST'])
@login_required
@patente_minima(1)
def atualizar_usuario(identificador):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE users SET nome = ?, email = ?, senha = ?, patente = ?
            WHERE identificador = ?
        ''', (data['nome'], data['email'], data['senha'], data['patente'], identificador))
        conn.commit()
        return jsonify({'success': True})
    except sqlite3.IntegrityError as e:
        return jsonify({'success': False, 'erro': str(e)})
    finally:
        conn.close()

# Excluir um usuário
@app.route('/api/usuario/<identificador>', methods=['DELETE'])
@login_required
@patente_minima(1)
def excluir_usuario_ajax(identificador):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE identificador = ?', (identificador,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/usuarios/relatorio')
@login_required
@patente_minima(1)
def gerar_relatorio_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT identificador, nome, email, patente, senha FROM users ORDER BY nome ASC')
    usuarios = cursor.fetchall()
    conn.close()

    # Cabeçalho da tabela
    data = [["Identificador", "Nome", "Email", "Patente", "Senha"]]
    for user in usuarios:
        data.append([
            user["identificador"],
            user["nome"],
            user["email"],
            user["patente"],
            user["senha"]
        ])

    # Criar o PDF em memória
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    tabela = Table(data)

    # Estilo temático escuro
    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#101010")),  # Cabeçalho preto
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#00FFFF")),  # Texto ciano no cabeçalho
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#1e1e1e")),  # Fundo linhas
        ("TEXTCOLOR", (0, 1), (-1, -1), colors.whitesmoke),           # Texto linhas
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#00FFFF")),  # Linhas ciano
    ])
    tabela.setStyle(style)

    doc.build([tabela])
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="Relatório Agentes NERO.pdf"
    )

@app.route('/inicio/secret')
@login_required
def secret():
    return render_template('secret.html')

@app.route('/secret')
def secret():
    return render_template('secret.html')

# ROTAS DE ERROS PERSONALIZADAS
@app.route('/erro_401')
def erro_401():
    return render_template('erro_401.html'), 401

@app.route('/erro_403')
def erro_403():
    return render_template('erro_403.html'), 403

@app.route('/erro_404')
def erro_404():
    return render_template('erro_404.html'), 404

@app.route('/erro_408')
def erro_408():
    return render_template('erro_408.html'), 408

@app.route('/erro_429')
def erro_429():
    return render_template('erro_429.html'), 429

@app.route('/erro_500')
def erro_500():
    return render_template('erro_500.html'), 500

@app.route('/erro_503')
def erro_503():
    return render_template('erro_503.html'), 503

# MANIPULADORES DE ERROS QUE REDIRECIONAM PARA AS ROTAS ACIMA
@app.errorhandler(401)
def handle_401(e):
    return redirect(url_for('erro_401'))

@app.errorhandler(403)
def handle_403(e):
    return redirect(url_for('erro_403'))

@app.errorhandler(404)
def handle_404(e):
    return redirect(url_for('erro_404'))

@app.errorhandler(408)
def handle_408(e):
    return redirect(url_for('erro_408'))

@app.errorhandler(429)
def handle_429(e):
    return redirect(url_for('erro_429'))

@app.errorhandler(500)
def handle_500(e):
    return redirect(url_for('erro_500'))

@app.errorhandler(503)
def handle_503(e):
    return redirect(url_for('erro_503'))

@app.route('/testar/<int:codigo>')
def testar_erro(codigo):
    abort(codigo)

# INÍCIO DO SERVIDOR
if __name__ == '__main__':
    app.run(debug=True)
