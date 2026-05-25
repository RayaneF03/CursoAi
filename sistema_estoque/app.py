"""
╔══════════════════════════════════════════════════════════════╗
║  SENAI Jaú — API de Estoque (servidor Flask + leitura CSV)   ║
║  Arquivo: app.py                                             ║
║  Como rodar: python app.py                                   ║
╚══════════════════════════════════════════════════════════════╝

PROMPT usado para criar este script:
"Crie uma API Flask simples que lê um arquivo CSV de estoque chamado
'estoque_producao.csv', expõe uma rota GET /api/estoque que retorna
os dados em JSON, e outra rota POST /api/estoque para adicionar itens.
Use flask-cors para permitir acesso do HTML local."
"""

import csv
import json
import os
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS

# ─── Configuração ────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)  # Permite que o HTML abra no navegador sem erro de CORS

ARQUIVO_CSV = 'estoque_producao.csv'

# ─── Funções auxiliares ───────────────────────────────────────────────

def ler_estoque():
    """Lê o CSV e retorna lista de dicionários."""
    if not os.path.exists(ARQUIVO_CSV):
        print(f"[AVISO] Arquivo '{ARQUIVO_CSV}' não encontrado.")
        return []

    produtos = []
    with open(ARQUIVO_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for linha in reader:
            # Converte tipos numéricos
            try:
                linha['id_produto']          = int(linha['id_produto'])
                linha['quantidade_estoque']  = int(linha['quantidade_estoque'])
                linha['quantidade_minima']   = int(linha['quantidade_minima'])
                linha['preco_unitario']      = float(linha['preco_unitario'])
            except (ValueError, KeyError):
                pass  # Mantém como string se der erro
            produtos.append(linha)
    return produtos


def salvar_estoque(produtos):
    """Salva lista de produtos de volta no CSV."""
    if not produtos:
        return
    campos = list(produtos[0].keys())
    with open(ARQUIVO_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(produtos)


def calcular_status(qtd_estoque, qtd_minima):
    """Define o status com base nos valores."""
    if qtd_estoque < qtd_minima:
        return 'ABAIXO_MINIMO'
    return 'OK'


# ─── Rotas da API ─────────────────────────────────────────────────────

@app.route('/')
def home():
    return jsonify({
        'sistema': 'SENAI Jaú - Controle de Estoque',
        'versao': '1.0',
        'rotas': {
            'GET  /api/estoque':          'Lista todos os produtos',
            'POST /api/estoque':          'Adiciona novo produto',
            'PUT  /api/estoque/<id>':     'Atualiza produto',
            'DELETE /api/estoque/<id>':   'Remove produto',
            'GET  /api/criticos':         'Lista produtos abaixo do mínimo',
            'GET  /api/resumo':           'Resumo geral do estoque',
        }
    })


@app.route('/api/estoque', methods=['GET'])
def listar_estoque():
    """Retorna todos os produtos do CSV em JSON."""
    produtos = ler_estoque()
    return jsonify(produtos)


@app.route('/api/estoque', methods=['POST'])
def adicionar_produto():
    """Adiciona um novo produto ao CSV."""
    dados = request.get_json()

    # Campos obrigatórios
    campos_obrigatorios = [
        'nome_produto', 'categoria', 'quantidade_estoque',
        'quantidade_minima', 'unidade', 'preco_unitario', 'fornecedor'
    ]
    for campo in campos_obrigatorios:
        if campo not in dados:
            return jsonify({'erro': f"Campo obrigatório ausente: '{campo}'"}), 400

    produtos = ler_estoque()

    # Gera novo ID (máximo + 1)
    novo_id = max((p['id_produto'] for p in produtos), default=1000) + 1

    novo_produto = {
        'id_produto':          novo_id,
        'nome_produto':        dados['nome_produto'],
        'categoria':           dados['categoria'],
        'quantidade_estoque':  int(dados['quantidade_estoque']),
        'quantidade_minima':   int(dados['quantidade_minima']),
        'unidade':             dados['unidade'],
        'preco_unitario':      float(dados['preco_unitario']),
        'fornecedor':          dados['fornecedor'],
        'ultima_atualizacao':  datetime.now().strftime('%Y-%m-%d'),
        'linha_producao':      dados.get('linha_producao', 'Geral'),
        'status':              calcular_status(
                                   int(dados['quantidade_estoque']),
                                   int(dados['quantidade_minima'])
                               ),
    }

    produtos.append(novo_produto)
    salvar_estoque(produtos)

    print(f"[OK] Produto adicionado: {novo_produto['nome_produto']} (ID {novo_id})")
    return jsonify({'mensagem': 'Produto adicionado com sucesso!', 'produto': novo_produto}), 201


@app.route('/api/estoque/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    """Atualiza quantidade ou outros campos de um produto."""
    dados    = request.get_json()
    produtos = ler_estoque()

    for i, p in enumerate(produtos):
        if p['id_produto'] == produto_id:
            # Atualiza somente os campos enviados
            for chave, valor in dados.items():
                produtos[i][chave] = valor

            # Recalcula status
            produtos[i]['status'] = calcular_status(
                int(produtos[i]['quantidade_estoque']),
                int(produtos[i]['quantidade_minima'])
            )
            produtos[i]['ultima_atualizacao'] = datetime.now().strftime('%Y-%m-%d')
            salvar_estoque(produtos)
            print(f"[OK] Produto {produto_id} atualizado.")
            return jsonify({'mensagem': 'Produto atualizado!', 'produto': produtos[i]})

    return jsonify({'erro': f'Produto {produto_id} não encontrado.'}), 404


@app.route('/api/estoque/<int:produto_id>', methods=['DELETE'])
def remover_produto(produto_id):
    """Remove um produto do CSV."""
    produtos = ler_estoque()
    originais = len(produtos)
    produtos  = [p for p in produtos if p['id_produto'] != produto_id]

    if len(produtos) == originais:
        return jsonify({'erro': f'Produto {produto_id} não encontrado.'}), 404

    salvar_estoque(produtos)
    print(f"[OK] Produto {produto_id} removido.")
    return jsonify({'mensagem': f'Produto {produto_id} removido com sucesso.'})


@app.route('/api/criticos', methods=['GET'])
def produtos_criticos():
    """Retorna apenas produtos abaixo do estoque mínimo."""
    produtos  = ler_estoque()
    criticos  = [p for p in produtos if p.get('status') == 'ABAIXO_MINIMO']
    return jsonify({'total_criticos': len(criticos), 'produtos': criticos})


@app.route('/api/resumo', methods=['GET'])
def resumo():
    """Retorna estatísticas gerais do estoque."""
    produtos  = ler_estoque()
    total     = len(produtos)
    criticos  = sum(1 for p in produtos if p.get('status') == 'ABAIXO_MINIMO')
    valor_total = sum(
        float(p.get('preco_unitario', 0)) * int(p.get('quantidade_estoque', 0))
        for p in produtos
    )
    categorias = list(set(p.get('categoria', '') for p in produtos))

    return jsonify({
        'total_produtos':   total,
        'estoque_ok':       total - criticos,
        'abaixo_minimo':    criticos,
        'valor_total_rs':   round(valor_total, 2),
        'total_categorias': len(categorias),
        'categorias':       sorted(categorias),
    })


# ─── Iniciar servidor ─────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 55)
    print("  SENAI Jaú — Sistema de Estoque")
    print("  Servidor rodando em: http://localhost:5000")
    print("  Para parar: Ctrl + C")
    print("=" * 55)
    app.run(debug=True, host='0.0.0.0', port=5000)
