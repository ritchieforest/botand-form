class BoyerMoore:
    def __init__(self, pattern):
        self.pattern = pattern
        self.m = len(pattern)
        self.bad_char = self._build_bad_char_table(pattern)

    def _build_bad_char_table(self, pattern):
        """Construye la tabla de caracteres malos para el algoritmo de Boyer-Moore."""
        bad_char_table = {}
        for i, char in enumerate(pattern):
            bad_char_table[char] = i
        return bad_char_table

    def search(self, text):
        """Busca todas las ocurrencias del patrón en el texto."""
        n = len(text)
        result = []
        s = 0  # Desplazamiento del patrón sobre el texto

        while s <= n - self.m:
            j = self.m - 1

            # Compara el patrón con el texto desde el final
            while j >= 0 and self.pattern[j] == text[s + j]:
                j -= 1

            # Si el patrón se encontró, agrega la posición a los resultados
            if j < 0:
                result.append(s)
                # Desplaza el patrón según la tabla de caracteres malos
                s += (self.m - self.bad_char.get(text[s + self.m], -1)) if s + self.m < n else 1
            else:
                # Desplaza el patrón según la tabla de caracteres malos
                s += max(1, j - self.bad_char.get(text[s + j], -1))

        return result
import difflib

class TextComparer:
    def __init__(self, text1, text2):
        self.text1 = text1.split()
        self.text2 = text2.split()

    def compare(self):
        """Compara los dos textos y devuelve un informe de las diferencias."""
        diff = difflib.unified_diff(self.text1, self.text2, fromfile='text1', tofile='text2')
        return '\n'.join(diff)

    def get_changes(self):
        """Devuelve un informe detallado de las diferencias en un formato de líneas modificadas."""
        d = difflib.Differ()
        diff = list(d.compare(self.text1, self.text2))
        print(diff)
        return '\n'.join(diff)

# Ejemplo de uso
if __name__ == "__main__":
    text = "Me gustaria añadir un producto AFINADOR CROMATICO PINZA MCT6 de categoria MAGMA, que tenga el precio 5909.3 y el proveedor sea ALEYMAR, con un stock 383, con un codigo de proveedor 20 y el codigo interno para el producto 120500 para la marca MAGMA"
    text1="Me gustaria añadir un producto {0} de categoria {1}, que tenga el precio {2} y el proveedor sea {3}, con un stock {4}, con un codigo de proveedor {5} y el codigo interno para el producto {6} para la marca {7}"
    comparer = TextComparer(text, text1)

    
    # print("Diferencias unificadas:")
    # print(comparer.compare())
    
    print("\nCambios detallados:")
    print(comparer.get_changes())
    pattern = "producto"

    bm = BoyerMoore(pattern)
    occurrences = bm.search(text)
    print("Ocurrencias encontradas en las posiciones:", occurrences)

