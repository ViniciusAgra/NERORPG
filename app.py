from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os

app = Flask(__name__, static_folder='static', template_folder='pages')
app.secret_key = os.urandom(24)

DB_PATH = os.path.join('data', 'users.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/sobreoff')
def sobrebasic():
    return render_template('sobrebasic.html')

@app.route('/identificacao')
def identificacao():
    return render_template('identificacao.html')

@app.route('/atribuicoes')
def atribuicoes():
    return render_template('atribuicoes.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

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
        return jsonify(success=True)
    else:
        return jsonify(success=False, message='Agente não localizado no sistema.')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        identificador = request.form['identificador']
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (identificador, nome, email, senha) VALUES (?, ?, ?, ?)',
                           (identificador, nome, email, senha))
            conn.commit()
            flash('Cadastro realizado com sucesso.')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError as e:
            if "users.email" in str(e):
                flash('Erro: Este e-mail já está em uso.')
            elif "users.identificador" in str(e):
                flash('Erro: Este identificador já está em uso.')
            else:
                flash('Erro ao cadastrar.')
        finally:
            conn.close()

    return render_template('cadastro.html')
