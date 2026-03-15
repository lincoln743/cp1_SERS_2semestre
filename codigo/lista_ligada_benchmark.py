#!/usr/bin/env python3
"""
Versão 2: lista ligada (linked list)
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


class Node:
    __slots__ = ("value", "next")

    def __init__(self, value: int, next: "Node | None" = None) -> None:
        self.value = value
        self.next = next


class LinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None
        self.tail: Node | None = None
        self.length = 0

    def append(self, value: int) -> None:
        node = Node(value)
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            assert self.tail is not None
            self.tail.next = node
            self.tail = node
        self.length += 1

    def contains(self, target: int) -> bool:
        current = self.head
        while current is not None:
            if current.value == target:
                return True
            current = current.next
        return False

    def remove_values_in_set(self, values_to_remove: set[int]) -> int:
        removed = 0

        while self.head is not None and self.head.value in values_to_remove:
            self.head = self.head.next
            removed += 1
            self.length -= 1

        current = self.head
        while current is not None and current.next is not None:
            if current.next.value in values_to_remove:
                current.next = current.next.next
                removed += 1
                self.length -= 1
            else:
                current = current.next

        self.tail = self.head
        if self.tail is not None:
            while self.tail.next is not None:
                self.tail = self.tail.next

        return removed


def benchmark_linked_list() -> dict:
    rng = random.Random(SEED)

    insert_values = list(range(N_INSERT))
    search_values = rng.sample(insert_values, N_SEARCH)
    remove_values = set(rng.sample(insert_values, N_REMOVE))

    tracemalloc.start()
    start_wall = time.perf_counter()
    start_cpu = time.process_time()

    # a) Inserção
    data = LinkedList()
    for value in insert_values:
        data.append(value)

    # b) Busca
    found = 0
    for value in search_values:
        if data.contains(value):  # busca linear
            found += 1

    # c) Remoção
    removed = data.remove_values_in_set(remove_values)

    cpu_time = time.process_time() - start_cpu
    wall_time = time.perf_counter() - start_wall
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    result = {
        "structure": "Lista ligada",
        "language": "Python",
        "insert_operations": N_INSERT,
        "search_operations": N_SEARCH,
        "remove_operations": N_REMOVE,
        "found_items": found,
        "removed_items": removed,
        "remaining_items": data.length,
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
    output_file = output_dir / "resultado_lista_ligada.json"
    output_file.write_text(json.dumps(result, indent=4, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    result = benchmark_linked_list()
    save_result(result)

    print("\n=== RESULTADO: LISTA LIGADA ===")
    print(f"Tempo de execução: {result['execution_time_seconds']:.6f} s")
    print(f"Proxy de energia (CPU): {result['energy_proxy_cpu_seconds']:.6f} s")
    print(f"Pico de memória: {result['peak_memory_mb']:.6f} MB")
    print(f"Itens encontrados: {result['found_items']}")
    print(f"Itens removidos: {result['removed_items']}")
    print(f"Itens restantes: {result['remaining_items']}")
    print("\nArquivo gerado: resultado_lista_ligada.json")
