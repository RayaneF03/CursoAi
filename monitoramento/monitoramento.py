# ============================================
# Sistema de Monitoramento Industrial - Têxtil
# Desenvolvido em Python
# ============================================

import csv
from datetime import datetime
from collections import defaultdict

# -----------------------------
# Dados simulados de produção
# -----------------------------
dados_producao = [
    [1, "Tear-01", "Manhã", 1200, "2026-05-25"],
    [2, "Tear-02", "Manhã", 980, "2026-05-25"],
    [3, "Tear-03", "Tarde", 1500, "2026-05-25"],
    [4, "Tear-01", "Noite", 1100, "2026-05-25"],
    [5, "Tear-02", "Tarde", 1340, "2026-05-25"],
    [6, "Tear-03", "Noite", 1700, "2026-05-25"],
]

# -----------------------------
# Criando arquivo CSV
# -----------------------------
nome_arquivo = "producao_textil.csv"

with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
    escritor = csv.writer(arquivo)

    # Cabeçalho
    escritor.writerow([
        "ID",
        "maquina",
        "turno",
        "pecas_produzidas",
        "data"
    ])

    # Dados
    escritor.writerows(dados_producao)

print(f"\nArquivo CSV '{nome_arquivo}' criado com sucesso!\n")

# -----------------------------
# Relatório no terminal
# -----------------------------

total_por_maquina = defaultdict(int)
total_por_turno = defaultdict(int)

for registro in dados_producao:
    _, maquina, turno, pecas, _ = registro

    total_por_maquina[maquina] += pecas
    total_por_turno[turno] += pecas

# Melhor turno
melhor_turno = max(total_por_turno, key=total_por_turno.get)

# -----------------------------
# Exibição do relatório
# -----------------------------
print("======================================")
print(" RELATÓRIO DE PRODUÇÃO INDUSTRIAL ")
print("======================================\n")

print("Total produzido por máquina:\n")

for maquina, total in total_por_maquina.items():
    print(f"{maquina}: {total} peças")

print("\n--------------------------------------")

print("\nProdução por turno:\n")

for turno, total in total_por_turno.items():
    print(f"{turno}: {total} peças")

print("\n--------------------------------------")

print(
    f"\nMelhor desempenho: "
    f"Turno {melhor_turno} "
    f"com {total_por_turno[melhor_turno]} peças produzidas."
)

print("\n======================================")