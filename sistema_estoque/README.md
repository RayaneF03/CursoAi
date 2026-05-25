# 📦 SENAI Jaú — Sistema de Controle de Estoque

Sistema web simples e moderno para controle de estoque industrial,
desenvolvido com Python (Flask) e HTML/Tailwind CSS.

---

## 🗂️ Estrutura do Projeto

```
senai-estoque/
│
├── index.html              ← Landing page (interface visual)
├── app.py                  ← Servidor Flask (API de dados)
├── banco.py                ← Criação e importação do banco SQLite
├── estoque_producao.csv    ← Planilha com os dados de estoque
├── estoque.db              ← Banco de dados (gerado automaticamente)
└── README.md               ← Este arquivo
```

---

## 📋 Campos do Sistema

| Campo                | Descrição                              |
|----------------------|----------------------------------------|
| `id_produto`         | Código único do produto                |
| `nome_produto`       | Nome do item                           |
| `categoria`          | Grupo do produto (Fixadores, EPI...)   |
| `quantidade_estoque` | Quanto tem em estoque agora            |
| `quantidade_minima`  | Quantidade mínima antes de alertar     |
| `unidade`            | Tipo de medida (un, m, lt, par)        |
| `preco_unitario`     | Valor por unidade em R$                |
| `fornecedor`         | Nome do fornecedor                     |
| `ultima_atualizacao` | Data da última mudança                 |

---

## 🚀 Como Ativar (passo a passo)

### 1. Instalar o Python

Baixe em: https://www.python.org/downloads/
Na instalação, **marque a opção "Add Python to PATH"**.

Verifique se funcionou (abra o Prompt de Comando / Terminal):
```
python --version
```

---

### 2. Instalar as bibliotecas necessárias

Abra o terminal na pasta do projeto e rode:

```bash
pip install flask flask-cors
```

---

### 3. Criar o banco de dados

Na mesma pasta do projeto, execute:

```bash
python banco.py
```

✅ O terminal vai mostrar um relatório com os produtos importados.
O arquivo `estoque.db` será criado automaticamente.

---

### 4. Iniciar o servidor

```bash
python app.py
```

Você verá:
```
=======================================================
  SENAI Jaú — Sistema de Estoque
  Servidor rodando em: http://localhost:5000
  Para parar: Ctrl + C
=======================================================
```

---

### 5. Abrir no navegador

**Opção A — Com a API rodando:**
Abra o arquivo `index.html` no navegador enquanto o `app.py` está
rodando. Os dados vêm direto da API em tempo real.

**Opção B — Somente visual (sem Python):**
Abra `index.html` normalmente — ele usa dados embutidos de exemplo
automaticamente quando a API não está disponível.

---

## 🔗 Rotas da API

Com o servidor rodando, acesse no navegador ou no Insomnia/Postman:

| Método | Rota                      | O que faz                         |
|--------|---------------------------|-----------------------------------|
| GET    | `/api/estoque`            | Lista todos os produtos           |
| POST   | `/api/estoque`            | Adiciona um novo produto          |
| PUT    | `/api/estoque/<id>`       | Atualiza um produto               |
| DELETE | `/api/estoque/<id>`       | Remove um produto                 |
| GET    | `/api/criticos`           | Lista produtos abaixo do mínimo   |
| GET    | `/api/resumo`             | Resumo geral (totais e valor)     |

**Exemplo — adicionar produto via terminal:**
```bash
curl -X POST http://localhost:5000/api/estoque \
  -H "Content-Type: application/json" \
  -d '{"nome_produto":"Luva de Couro","categoria":"EPI","quantidade_estoque":30,"quantidade_minima":10,"unidade":"par","preco_unitario":12.50,"fornecedor":"SafeWork"}'
```

---

## 💡 Recursos da Interface

- 🔴 **Cores SENAI**: branco, vermelho (#C8102E) e preto
- 📊 **Cards de resumo**: total, OK, críticos e valor total
- 🔍 **Busca em tempo real** por nome ou fornecedor
- 🏷️ **Filtros** por categoria e status
- ⚠️ **Alertas visuais** para produtos abaixo do mínimo
- 📈 **Barra de progresso** do estoque por produto
- 🔄 **Auto-atualização** a cada 30 segundos

---

## 🛠️ Possíveis Erros e Soluções

| Problema                        | Solução                                              |
|---------------------------------|------------------------------------------------------|
| `ModuleNotFoundError: flask`    | Rode `pip install flask flask-cors`                  |
| `python: command not found`     | Reinstale o Python marcando "Add to PATH"            |
| API não carrega no HTML         | Verifique se o `app.py` está rodando                 |
| CSV não encontrado              | Coloque o CSV na mesma pasta que o `banco.py`        |
| Porta 5000 em uso               | Troque `port=5000` por `port=5001` no `app.py`       |

---

## 📁 Prompts Utilizados

Cada arquivo foi criado com um prompt específico:

### 🌐 Landing Page (`index.html`)
> "Crie uma landing page moderna para o sistema de estoque do SENAI Jaú
> usando Tailwind CSS com as cores branco, vermelho (#C8102E) e preto.
> A página deve ter: header com logo, cards de resumo (total, OK,
> críticos, valor), barra de busca + filtros por categoria e status,
> tabela com todos os campos do CSV (id, nome, categoria, estoque,
> mínimo, unidade, preço, fornecedor, data, status), barra de progresso
> por item, badges coloridos de status e atualização automática a cada
> 30 segundos via fetch para uma API Flask em localhost:5000."

---

### 🐍 Servidor Flask (`app.py`)
> "Crie uma API Flask simples que lê um arquivo CSV de estoque chamado
> 'estoque_producao.csv', expõe uma rota GET /api/estoque que retorna
> os dados em JSON, e outras rotas para adicionar, atualizar e remover
> produtos. Use flask-cors para permitir acesso do HTML local. Inclua
> também rotas /api/criticos e /api/resumo."

---

### 🗄️ Banco de Dados (`banco.py`)
> "Crie um script Python que: (1) cria um banco SQLite chamado
> 'estoque.db' com uma tabela 'produtos' contendo os campos do sistema
> de estoque SENAI; (2) importa os dados de um CSV chamado
> 'estoque_producao.csv'; (3) exibe um relatório no terminal mostrando
> total de produtos, itens críticos, valor total do estoque e listagem
> de produtos abaixo do mínimo."

---

### 📖 Documentação (`README.md`)
> "Crie um README completo para um projeto de sistema de estoque
> desenvolvido com Python Flask e HTML Tailwind CSS para o SENAI Jaú.
> Inclua: estrutura de pastas, tabela de campos, passo a passo para
> instalar Python e rodar o projeto, tabela das rotas da API com
> exemplos, lista de recursos da interface, tabela de erros comuns com
> soluções, e os prompts utilizados para criar cada arquivo do sistema."

---

## 🎓 Sobre o Projeto

Desenvolvido como projeto educacional para o **SENAI Jaú**.
Ideal para aprender conceitos de:

- Desenvolvimento web com HTML e CSS
- APIs REST com Python Flask
- Banco de dados com SQLite
- Integração frontend ↔ backend

---

*Sistema de Controle de Estoque Industrial — SENAI Jaú · 2024*
