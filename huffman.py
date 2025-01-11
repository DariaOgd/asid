from collections import Counter
import os
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
    Q = [(char, freq, None, None) for char, freq in C.items()]
    buduj_kopiec(Q)
    for _ in range(1, n):
        z_left = extract_min(Q)
        z_right = extract_min(Q)
        z_freq = z_left[1] + z_right[1]
        z = (None, z_freq, z_left, z_right)
        dodaj_do_kopca(Q, z)
    return extract_min(Q)

#slownik
def generuj_huffmana(node):
    kody = {}
    stos = [(node, "")]
    while stos:
        current, code = stos.pop()
        char, _, left, right = current
        if char:
            kody[char] = code
        else:
            if right:
                stos.append((right, code + "1"))
            if left:
                stos.append((left, code + "0"))
    return kody

def zlicz_znaki(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    czestotliwosc = Counter(text)
    return text, dict(czestotliwosc)

# kompresja
def huffman_binarnie(output_file, codes, encoded_text):
    slownik = ', '.join(f"'{char}':'{code}'" for char, code in codes.items())
    binarnie = int(encoded_text, 2).to_bytes((len(encoded_text) + 7) // 8, 'big')
    with open(output_file, 'wb') as file:
        file.write(f"{slownik}\n".encode('utf-8'))
        file.write(binarnie)

# funkcja pomocniczna - nie do sprawdzenia
def compare_file_sizes(input_file, compressed_file):
    input_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(compressed_file)
    print(f"Rozmiar pliku wejściowego: {input_size} bajtów")
    print(f"Rozmiar pliku skompresowanego: {compressed_size} bajtów")

def kompresuj_plik(plik_wejsciowy, plik_wyjsciowy):
    tekst, freq = zlicz_znaki(plik_wejsciowy)
    drzewo_huffmana = huffman(freq)
    kody = generuj_huffmana(drzewo_huffmana)
    zakodowany_tekst = ''.join(kody[znak] for znak in tekst)
    huffman_binarnie(plik_wyjsciowy, kody, zakodowany_tekst)
    compare_file_sizes(plik_wejsciowy, plik_wyjsciowy)

def main():
    input = "input.txt"
    skompersowany = "skompersowany.txt"
    kompresuj_plik(input, skompersowany)

main()
