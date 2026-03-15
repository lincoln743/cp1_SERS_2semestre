#!/usr/bin/env python3
"""
Versão 3: tabela hash (dict do Python)
Mede:
- tempo de execução
- proxy de energia (tempo de CPU)
- pico de memória
"""

from __future__ import annotations
import json
import random
import time
import tracemalloc
from pathlib import Path

N_INSERT = 100_000
N_SEARCH = 50_000
N_REMOVE = 20_000
SEED = 42


def benchmark_hash_table() -> dict:
    rng = random.Random(SEED)

    insert_values = list(range(N_INSERT))
    search_values = rng.sample(insert_values, N_SEARCH)
    remove_values = rng.sample(insert_values, N_REMOVE)

    tracemalloc.start()
    start_wall = time.perf_counter()
    start_cpu = time.process_time()

    # a) Inserção
    data = {}
    for value in insert_values:
        data[value] = value

    # b) Busca
    found = 0
    for value in search_values:
        if value in data:   # busca média O(1)
            found += 1

    # c) Remoção
    removed = 0
    for value in remove_values:
        if value in data:
            del data[value]
            removed += 1

    cpu_time = time.process_time() - start_cpu
    wall_time = time.perf_counter() - start_wall
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    result = {
        "structure": "Tabela hash",
        "language": "Python",
        "insert_operations": N_INSERT,
        "search_operations": N_SEARCH,
        "remove_operations": N_REMOVE,
        "found_items": found,
        "removed_items": removed,
        "remaining_items": len(data),
        "execution_time_seconds": wall_time,
        "cpu_time_seconds": cpu_time,
        "energy_proxy_cpu_seconds": cpu_time,
        "peak_memory_mb": peak_mem / (1024 * 1024),
        "current_memory_mb": current_mem / (1024 * 1024),
        "methodology": {
            "time": "time.perf_counter()",
            "cpu_proxy": "time.process_time()",
            "memory": "tracemalloc peak"
        }
    }
    return result


def save_result(result: dict) -> None:
    output_dir = Path(__file__).resolve().parent
    output_file = output_dir / "resultado_tabela_hash.json"
    output_file.write_text(json.dumps(result, indent=4, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    result = benchmark_hash_table()
    save_result(result)

    print("\n=== RESULTADO: TABELA HASH ===")
    print(f"Tempo de execução: {result['execution_time_seconds']:.6f} s")
    print(f"Proxy de energia (CPU): {result['energy_proxy_cpu_seconds']:.6f} s")
    print(f"Pico de memória: {result['peak_memory_mb']:.6f} MB")
    print(f"Itens encontrados: {result['found_items']}")
    print(f"Itens removidos: {result['removed_items']}")
    print(f"Itens restantes: {result['remaining_items']}")
    print("\nArquivo gerado: resultado_tabela_hash.json")
