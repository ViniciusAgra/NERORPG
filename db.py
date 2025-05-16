import sqlite3
import os

# Cria a pasta do banco se não existir
os.makedirs('data', exist_ok=True)
conn = sqlite3.connect('data/main.db')
cursor = conn.cursor()

# Tabela de patentes
cursor.execute('''
CREATE TABLE IF NOT EXISTS patentes (
    nome TEXT PRIMARY KEY,
    nivel INTEGER NOT NULL
)
''')
# Inserção das patentes
patentes = [
        # Nível 1
        ("Diretor(a)", 1),
        ("ADM Geral", 1),
        ("Conselho de Guarnição", 2),
        ("Marechal", 3),
        ("General do Exército", 4),
        ("General de Divisão", 5),
        ("General de Brigada", 6),
        ("Coronel", 7),
        ("Tenente-Coronel", 8),
        ("Major", 9),
        ("Capitão", 10),
        ("1º Tenente", 11),
        ("2º Tenente", 12),
        ("Aspirante-a-Oficial", 13),
        ("Subtenente", 14),
        ("1º Sargento", 15),
        ("2º Sargento", 16),
        ("3º Sargento", 17),
        ("Cabo", 18),
        ("Soldado", 19),
        ("Almirante", 3),
        ("Almirante de Esquadra", 4),
        ("Vice-Almirante", 5),
        ("Contra-Almirante", 6),
        ("Capitão de Mar e Guerra", 7),
        ("Capitão de Fragata", 8),
        ("Capitão de Corveta", 9),
        ("Capitão-Tenente", 10),
        ("Guarda-Marinha", 13),
        ("Marinheiro", 19),
        ("Tenente-Brigadeiro", 3),
        ("Major-Brigadeiro", 4),
        ("Brigadeiro", 5),
    ]
cursor.executemany('INSERT OR IGNORE INTO patentes (nome, nivel) VALUES (?, ?)', patentes)

# Tabela de usuários
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    identificador TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT UNIQUE,
    senha TEXT NOT NULL,
    patente TEXT NOT NULL,
    FOREIGN KEY(patente) REFERENCES patentes(nome)
)
''')

# ADM Geral padrão
cursor.execute('''
INSERT OR IGNORE INTO users (identificador, nome, email, senha, patente)
VALUES ('.', 'Vinicius', 'viniciusagra2015@gmail.com', '.', 'ADM Geral')
''')

# Tabela de Uploads
cursor.execute('''
CREATE TABLE uploads (
    uuid TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    nome_original TEXT NOT NULL,
    nome_armazenado TEXT NOT NULL,
    caminho TEXT NOT NULL,
    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(identificador)
)
''')

# Tabela de Consultas
cursor.execute('''
CREATE TABLE IF NOT EXISTS consultas (
    codigo_de_consulta TEXT PRIMARY KEY,
    usuario_editor TEXT NOT NULL,
    link_arquivo TEXT NOT NULL,
    confidencial INTEGER NOT NULL CHECK(confidencial IN (0, 1))
);
''')

conn.commit()
conn.close()
