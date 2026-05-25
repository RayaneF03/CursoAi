"""
╔══════════════════════════════════════════════════════════════╗
║  SENAI Jaú — Banco de Dados SQLite                           ║
║  Arquivo: banco.py                                           ║
║  Como rodar: python banco.py                                 ║
╚══════════════════════════════════════════════════════════════╝

PROMPT usado para criar este script:
"Crie um script Python que: (1) cria um banco SQLite chamado
'estoque.db' com uma tabela 'produtos' contendo os campos
id_produto, nome_produto, categoria, quantidade_estoque,
quantidade_minima, unidade, preco_unitario, fornecedor,
ultima_atualizacao, linha_producao e status; (2) importa os
dados de um CSV chamado 'estoque_producao.csv'; (3) exibe um
relatório simples no terminal ao final."
"""

import sqlite3
import csv
import os
from datetime import datetime

# ─── Configuração ─────────────────────────────────────────────────────
BANCO_DB    = 'estoque.db'
ARQUIVO_CSV = 'estoque_producao.csv'


def criar_banco():
    """Cria o banco de dados e a tabela de produtos."""
    conn   = sqlite3.connect(BANCO_DB)
    cursor = conn.cursor()

    # Cria a tabela (se não existir)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id_produto          INTEGER PRIMARY KEY,
            nome_produto        TEXT    NOT NULL,
            categoria           TEXT    NOT NULL,
            quantidade_estoque  INTEGER NOT NULL DEFAULT 0,
            quantidade_minima   INTEGER NOT NULL DEFAULT 0,
            unidade             TEXT    NOT NULL,
            preco_unitario      REAL    NOT NULL DEFAULT 0.0,
            fornecedor          TEXT,
            ultima_atualizacao  TEXT,
            linha_producao      TEXT,
            status              TEXT    DEFAULT 'OK',
            criado_em           TEXT    DEFAULT (datetime('now','localtime'))
        )
    ''')
    conn.commit()
    print("[OK] Tabela 'produtos' criada (ou já existia).")
    return conn


def importar_csv(conn):
    """Importa os dados do CSV para o banco."""
    if not os.path.exists(ARQUIVO_CSV):
        print(f"[ERRO] Arquivo '{ARQUIVO_CSV}' não encontrado!")
        print("       Coloque o CSV na mesma pasta e tente novamente.")
        return 0

    cursor      = conn.cursor()
    importados  = 0
    ignorados   = 0

    with open(ARQUIVO_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for linha in reader:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO produtos
                        (id_produto, nome_produto, categoria,
                         quantidade_estoque, quantidade_minima,
                         unidade, preco_unitario, fornecedor,
                         ultima_atualizacao, linha_producao, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    int(linha['id_produto']),
                    linha['nome_produto'],
                    linha['categoria'],
                    int(linha['quantidade_estoque']),
                    int(linha['quantidade_minima']),
                    linha['unidade'],
                    float(linha['preco_unitario']),
                    linha.get('fornecedor', ''),
                    linha.get('ultima_atualizacao', ''),
                    linha.get('linha_producao', ''),
                    linha.get('status', 'OK'),
                ))
                importados += 1
            except Exception as e:
                print(f"  [AVISO] Linha ignorada: {e}")
                ignorados += 1

    conn.commit()
    print(f"[OK] {importados} produto(s) importado(s). {ignorados} ignorado(s).")
    return importados


def exibir_relatorio(conn):
    """Exibe um relatório simples no terminal."""
    cursor = conn.cursor()

    print("\n" + "=" * 55)
    print("  SENAI Jaú — Relatório do Estoque")
    print(f"  Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 55)

    # Total de produtos
    cursor.execute("SELECT COUNT(*) FROM produtos")
    total = cursor.fetchone()[0]
    print(f"\n  Total de produtos cadastrados : {total}")

    # Produtos abaixo do mínimo
    cursor.execute("SELECT COUNT(*) FROM produtos WHERE status = 'ABAIXO_MINIMO'")
    criticos = cursor.fetchone()[0]
    print(f"  Produtos abaixo do mínimo    : {criticos}")

    # Valor total do estoque
    cursor.execute("SELECT SUM(preco_unitario * quantidade_estoque) FROM produtos")
    valor = cursor.fetchone()[0] or 0
    print(f"  Valor total do estoque       : R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

    # Produtos críticos (lista)
    print("\n  ── Produtos Abaixo do Mínimo ──")
    cursor.execute('''
        SELECT id_produto, nome_produto, quantidade_estoque, quantidade_minima, unidade
        FROM produtos
        WHERE status = 'ABAIXO_MINIMO'
        ORDER BY quantidade_estoque ASC
    ''')
    criticos_lista = cursor.fetchall()
    if criticos_lista:
        for p in criticos_lista:
            print(f"  ⚠️  [{p[0]}] {p[1]:<30} {p[2]} {p[4]} (mín: {p[3]})")
    else:
        print("  ✅  Nenhum produto crítico!")

    # Resumo por categoria
    print("\n  ── Categorias ──")
    cursor.execute('''
        SELECT categoria, COUNT(*) as qtd
        FROM produtos
        GROUP BY categoria
        ORDER BY qtd DESC
    ''')
    for cat, qtd in cursor.fetchall():
        print(f"  • {cat:<20} {qtd} produto(s)")

    print("\n" + "=" * 55)
    print(f"  Banco salvo em: {os.path.abspath(BANCO_DB)}")
    print("=" * 55 + "\n")


def buscar_produto(conn, termo):
    """Busca produtos por nome (exemplo de uso do banco)."""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id_produto, nome_produto, quantidade_estoque, unidade, status
        FROM produtos
        WHERE nome_produto LIKE ?
    ''', (f'%{termo}%',))
    return cursor.fetchall()


def atualizar_quantidade(conn, produto_id, nova_quantidade):
    """Atualiza a quantidade de um produto e recalcula o status."""
    cursor = conn.cursor()

    # Busca o mínimo atual
    cursor.execute("SELECT quantidade_minima FROM produtos WHERE id_produto = ?", (produto_id,))
    row = cursor.fetchone()
    if not row:
        print(f"[ERRO] Produto {produto_id} não encontrado.")
        return False

    minimo = row[0]
    novo_status = 'ABAIXO_MINIMO' if nova_quantidade < minimo else 'OK'

    cursor.execute('''
        UPDATE produtos
        SET quantidade_estoque = ?,
            status             = ?,
            ultima_atualizacao = ?
        WHERE id_produto = ?
    ''', (nova_quantidade, novo_status, datetime.now().strftime('%Y-%m-%d'), produto_id))

    conn.commit()
    print(f"[OK] Produto {produto_id}: quantidade → {nova_quantidade} | status → {novo_status}")
    return True


# ─── Execução principal ───────────────────────────────────────────────
if __name__ == '__main__':
    print("\nIniciando configuração do banco de dados...\n")

    conn = criar_banco()
    importar_csv(conn)
    exibir_relatorio(conn)
    conn.close()

    print("[PRONTO] Execute 'python app.py' para iniciar o servidor.\n")
