import sqlite3
import os

# Cria a pasta do banco se não existir
os.makedirs('data', exist_ok=True)
conn = sqlite3.connect('data/users.db')
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

        # Nível 2
        ("Conselho de Guarnição", 2),

        # Nível 3 — Exército (Ex)
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

        # Nível 3 — Marinha (Ma)
        ("Almirante", 3),
        ("Almirante de Esquadra", 4),
        ("Vice-Almirante", 5),
        ("Contra-Almirante", 6),
        ("Capitão de Mar e Guerra", 7),
        ("Capitão de Fragata", 8),
        ("Capitão de Corveta", 9),
        ("Capitão-Tenente", 10),
        ("1º Tenente (Marinha)", 11),
        ("2º Tenente (Marinha)", 12),
        ("Guarda-Marinha", 13),
        ("Suboficial (Marinha)", 14),
        ("1º Sargento (Marinha)", 15),
        ("2º Sargento (Marinha)", 16),
        ("3º Sargento (Marinha)", 17),
        ("Cabo (Marinha)", 18),
        ("Marinheiro", 19),

        # Nível 3 — Aeronáutica (Ae)
        ("Tenente-Brigadeiro", 3),
        ("Major-Brigadeiro", 4),
        ("Brigadeiro", 5),
        ("Coronel (FAB)", 7),
        ("Tenente-Coronel (FAB)", 8),
        ("Major (FAB)", 9),
        ("Capitão (FAB)", 10),
        ("1º Tenente (FAB)", 11),
        ("2º Tenente (FAB)", 12),
        ("Aspirante (FAB)", 13),
        ("Suboficial (FAB)", 14),
        ("1º Sargento (FAB)", 15),
        ("2º Sargento (FAB)", 16),
        ("3º Sargento (FAB)", 17),
        ("Cabo (FAB)", 18),
        ("Soldado (FAB)", 19)
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

conn.commit()
conn.close()
