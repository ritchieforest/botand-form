class RabinKarp:
    def __init__(self, pattern, prime=101, base=256):
        self.pattern = pattern
        self.m = len(pattern)
        self.prime = prime
        self.base = base
        self.pattern_hash = self._hash(pattern)
        self.base_m = pow(base, self.m - 1, prime)
        self.current_hash = 0

    def _hash(self, s):
        """Calcula el hash de la cadena s usando el algoritmo de Rabin-Karp."""
        hash_value = 0
        for char in s:
            hash_value = (self.base * hash_value + ord(char)) % self.prime
        return hash_value

    def search(self, text):
        """Busca todas las ocurrencias del patrón en el texto usando el algoritmo de Rabin-Karp."""
        n = len(text)
        result = []
        if self.m > n:
            return result

        # Calcula el hash del primer fragmento del texto
        self.current_hash = self._hash(text[:self.m])

        for i in range(n - self.m + 1):
            if self.current_hash == self.pattern_hash:
                # Verifica la coincidencia real de la subcadena
                if text[i:i + self.m] == self.pattern:
                    result.append(i)

            # Calcula el hash del siguiente fragmento del texto
            if i < n - self.m:
                self.current_hash = (self.base * (self.current_hash - ord(text[i]) * self.base_m) + ord(text[i + self.m])) % self.prime
                # Asegúrate de que el hash sea positivo
                if self.current_hash < 0:
                    self.current_hash += self.prime

        return result

# Ejemplo de uso
if __name__ == "__main__":
    text = "ababcababcabcabc"
    pattern = "abc"

    rk = RabinKarp(pattern)
    occurrences = rk.search(text)
    print("Ocurrencias encontradas en las posiciones:", occurrences)
