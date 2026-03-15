#!/usr/bin/env python3
"""
Gera os 3 gráficos em Python a partir dos arquivos JSON produzidos
pelos benchmarks.
"""

from __future__ import annotations
import json
from pathlib import Path

import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parent

FILES = [
    BASE_DIR / "resultado_lista_dinamica.json",
    BASE_DIR / "resultado_lista_ligada.json",
    BASE_DIR / "resultado_tabela_hash.json",
]


def load_results() -> list[dict]:
    results = []
    for file_path in FILES:
        if not file_path.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {file_path.name}. "
                f"Execute primeiro os 3 benchmarks."
            )
        results.append(json.loads(file_path.read_text(encoding="utf-8")))
    return results


def save_bar_chart(x, y, title, ylabel, output_name):
    plt.figure(figsize=(10, 6))
    plt.bar(x, y)
    plt.title(title)
    plt.xlabel("Estrutura de dados")
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(BASE_DIR / output_name, dpi=300)
    plt.close()


def main():
    results = load_results()

    structures = [item["structure"] for item in results]
    times = [item["execution_time_seconds"] for item in results]
    energies = [item["energy_proxy_cpu_seconds"] for item in results]
    memories = [item["peak_memory_mb"] for item in results]

    save_bar_chart(
        structures,
        times,
        "Comparação do tempo de execução",
        "Tempo (segundos)",
        "grafico_tempo_execucao.png"
    )

    save_bar_chart(
        structures,
        energies,
        "Comparação do consumo energético (proxy de CPU)",
        "Tempo de CPU (segundos)",
        "grafico_energia_proxy.png"
    )

    save_bar_chart(
        structures,
        memories,
        "Comparação do uso de memória",
        "Pico de memória (MB)",
        "grafico_memoria.png"
    )

    print("\nGráficos gerados com sucesso:")
    print("- grafico_tempo_execucao.png")
    print("- grafico_energia_proxy.png")
    print("- grafico_memoria.png")


if __name__ == "__main__":
    main()
