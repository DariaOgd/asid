from collections import Counter
import os
from bitarray import bitarray

# kopiec
def napraw_kopiec(heap, i, heap_size):
    left = 2 * i + 1
    right = 2 * i + 2
    smallest = i
    if left < heap_size and heap[left][1] < heap[smallest][1]:
        smallest = left
    if right < heap_size and heap[right][1] < heap[smallest][1]:
        smallest = right
    if smallest != i:
        heap[i], heap[smallest] = heap[smallest], heap[i]
        napraw_kopiec(heap, smallest, heap_size)

def buduj_kopiec(heap):
    heap_size = len(heap)
    for i in range(heap_size // 2 - 1, -1, -1):
        napraw_kopiec(heap, i, heap_size)

def extract_min(heap):
    if len(heap) < 1:
        return None
    min_node = heap[0]
    heap[0] = heap[-1]
    heap.pop()
    napraw_kopiec(heap, 0, len(heap))
    return min_node

def dodaj_do_kopca(heap, x):
    heap.append(x)
    i = len(heap) - 1
    while i > 0 and heap[(i - 1) // 2][1] > heap[i][1]:
        parent = (i - 1) // 2
        heap[i], heap[parent] = heap[parent], heap[i]
        i = parent

# huffman
def huffman(C):
    n = len(C)
    Q = [(char, freq, 'lisc', 'lisc') for char, freq in C.items()]
    buduj_kopiec(Q)
    for _ in range(1, n):
        z_left = extract_min(Q)
        z_right = extract_min(Q)
        z_freq = z_left[1] + z_right[1]
        z = (None, z_freq, z_left, z_right)
        dodaj_do_kopca(Q, z)
    return extract_min(Q)

#slownik
def generuj_slownik_huffmana(node):
    kody = {}
    stos = [(node, "")]
    while stos:
        curr, kod = stos.pop()
        char, _, l, r = curr
        if char:
            kody[char] = kod
        else:
            if r:
                stos.append((r, kod + "1"))
            if l:
                stos.append((l, kod + "0"))
    return kody

def huffman_binarnie(output, kody, zakodowany_tekst):
    skrocony_slownik = '\n'.join(f"{char}:{code}" for char, code in kody.items())
    ba = bitarray(zakodowany_tekst)
    binarnie = ba.tobytes()
    with open(output, 'wb') as file:
        file.write(skrocony_slownik.encode('utf-8') + b'\n')
        file.write(b"Huffman\n")
        file.write(binarnie)
    return skrocony_slownik, binarnie

# funkcja pomocniczna - nie do sprawdzenia
def compare_file_sizes(input_file, compressed_file):
    input_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(compressed_file)
    print(f"Rozmiar pliku wejściowego: {input_size} bajtów")
    print(f"Rozmiar pliku skompresowanego: {compressed_size} bajtów")


def kompresuj_plik(plik_wejsciowy, plik_wyjsciowy):
    with open(plik_wejsciowy, 'r', encoding='utf-8') as file:
        tekst = file.read()
    freq = Counter(tekst)
    drzewo = huffman(freq)
    kody = generuj_slownik_huffmana(drzewo)
    zakodowany_tekst = ''.join(kody[znak] for znak in tekst)
    if len(kody) == 1:
        znak, kod = next(iter(kody.items()))
        zakodowany_tekst = '0' * len(tekst)
        kody = {znak: '0'}
    slownik_string = ','.join(f"{znak}:{kod}" for znak, kod in kody.items())
    ba = bitarray(zakodowany_tekst)
    with open(plik_wyjsciowy, 'wb') as file:
        file.write(slownik_string.encode('utf-8') + b'\n')
        file.write(ba.tobytes())

def main():
    input = "input.txt"
    skompresowany = "skompresowany.txt"
    kompresuj_plik(input, skompresowany)
    compare_file_sizes(input, skompresowany)

main()
