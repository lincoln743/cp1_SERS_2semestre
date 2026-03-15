#!/usr/bin/env python3
"""
Executa as 3 versões do benchmark e depois gera os gráficos.
"""

from __future__ import annotations
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

SCRIPTS = [
    "lista_dinamica_benchmark.py",
    "lista_ligada_benchmark.py",
    "tabela_hash_benchmark.py",
    "gerar_graficos.py",
]


def main():
    for script in SCRIPTS:
        print(f"\nExecutando: {script}")
        subprocess.run([sys.executable, str(BASE_DIR / script)], check=True)

    print("\nProcesso finalizado.")


if __name__ == "__main__":
    main()
