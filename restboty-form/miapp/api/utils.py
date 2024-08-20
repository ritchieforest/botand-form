import difflib
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

class TextComparer:
    def __init__(self):
        self.text1 = ""
        self.text2 = ""

    def compare(self):
        """Compara los dos textos y devuelve un informe de las diferencias."""
        diff = difflib.unified_diff(self.text1, self.text2, fromfile='text1', tofile='text2')
        return '\n'.join(diff)
    def get_clean_text(text1, text2):
        """
        Elimina las diferencias entre dos textos y devuelve un texto combinado basado en las partes coincidentes.
        """
        d = difflib.Differ()
        diff = list(d.compare(text1.splitlines(), text2.splitlines()))

        # Construir un texto limpio basado en las partes coincidentes
        clean_lines = []
        for line in diff:
            if line.startswith(' '):  # Línea que es común en ambos textos
                clean_lines.append(line[2:])  # Eliminar el prefijo ' '

        # Unir las líneas en un solo texto
        clean_text = '\n'.join(clean_lines)
        return clean_text
    def get_clean_texts(self,text1, text2):
        """
        Elimina las diferencias entre dos textos y devuelve dos textos basados en las partes coincidentes.
        """
        d = difflib.Differ()
        diff = list(d.compare(text1.split(), text2.split()))

        # Inicializar las listas para las partes coincidentes en ambos textos
        clean_text1_lines = []
        clean_text2_lines = []
        # Recorrer las diferencias y construir los textos limpios
        for line in diff:
            if line.startswith(' '):  # Línea que es común en ambos textos
                clean_text1_lines.append(line[2:])  # Eliminar el prefijo ' '
                clean_text2_lines.append(line[2:])  # Eliminar el prefijo ' '
            elif line.startswith('-'):  # Línea que está en text1 pero no en text2
                clean_text1_lines.append('')  # Eliminar del texto 1
            elif line.startswith('+'):  # Línea que está en text2 pero no en text1
                clean_text2_lines.append('')  # Eliminar del texto 2

        # Unir las líneas en un solo texto para cada texto limpio
        clean_text1 = ' '.join(clean_text1_lines)
        clean_text2 = ' '.join(clean_text2_lines)
        
        return clean_text1, clean_text2
    def replace_differences(self,text1, text2):
        """
        Reemplaza las diferencias en text1 con el contenido de text2 y devuelve el texto modificado.
        """
        d = difflib.Differ()
        diff = list(d.compare(text1.split(), text2.split()))

        # Inicializar las listas para las líneas del texto modificado
        modified_lines = []

        for line in diff:
            if line.startswith(' '):  # Línea que es común en ambos textos
                modified_lines.append(line[2:])  # Eliminar el prefijo ' '
            elif line.startswith('-'):  # Línea que está en text1 pero no en text2
                # No hacer nada aquí, ya que esta línea será reemplazada
                pass
            elif line.startswith('+'):  # Línea que está en text2 pero no en text1
                modified_lines.append(line[2:])  # Agregar la línea de text2

        # Unir las líneas en un solo texto modificado
        modified_text = ' '.join(modified_lines)
        
        return modified_text,text2
    def group_differences(self,diff):
        """
        Agrupa las diferencias en pares, donde cada línea añadida se agrupa con las líneas eliminadas subsecuentes.
        """
        grouped_diffs = {}
        current_group = []
        auxPos=""
        for line in diff:
            if line.startswith('-'):
                auxPos=line[2:]
                grouped_diffs[auxPos]=[]
            elif line.startswith('+'):
                grouped_diffs[auxPos].append(line[2:])
 
        return grouped_diffs
    def get_changes(self):
        """Devuelve un informe detallado de las diferencias en un formato de líneas modificadas."""
        d = difflib.Differ()
        diff = list(d.compare(self.text1, self.text2))
        return diff
    def get_maching(self):
        # Crear un comparador
        matcher = difflib.SequenceMatcher(None, self.text1, self.text2)
        # Obtener las secuencias coincidentes
        matches = matcher.get_matching_blocks()
        # Construir una nueva secuencia a partir de los bloques coincidentes
        result1 = []
        result2 = []
        for match in matches:
            result1.extend(self.text1[match.a: match.a + match.size])
            result2.extend(self.text2[match.b: match.b + match.size])

        # Unir los tokens para formar los textos filtrados
        filtered_text1 = " ".join(result1)
        filtered_text2 = " ".join(result2)

        print(f"Texto 1 filtrado: {filtered_text1}")
        print(f"Texto 2 filtrado: {filtered_text2}")

        # Comprobar si los textos filtrados son iguales
        if filtered_text1 == filtered_text2:
            print("Los textos tienen el mismo esquema o estructura.")
        else:
            print("Los textos no tienen el mismo esquema")
    def calculate_similarity(self,text1, text2):
        # Tokenizar los textos en palabras
        tokens1 = text1.split()
        tokens2 = text2.split()

        # Crear un comparador de secuencias
        matcher = difflib.SequenceMatcher(None, tokens1, tokens2)

        # Calcular el ratio de similitud
        similarity_ratio = matcher.ratio()

        # Convertir el ratio a un porcentaje
        similarity_percentage = similarity_ratio * 100

        return similarity_percentage
    def order_with_object(self,obj,text1,text2):
        auxResultado=dict({})
        for item in obj.labels:
            auxResultado[str(item.labelByContext_id)]=""
            text2=text2.replace(str(item.refString),str(item.labelByContext_id)).replace(",","")
        self.text1=text2.split()   
        diff=self.get_changes()
        diferencias_group=self.group_differences(diff)
        for i,item in diferencias_group.items():
            auxResultado[i]=" ".join(item)
        return auxResultado
            
    def calculate_similarity_arr(self,textComparer,textArr):
        try:    
            porc=0
            text1=""
            text2=""
            item=None
            for arr in textArr: 
                Auxporc=self.calculate_similarity(text1=textComparer.lower(),text2=arr.descripcion.lower())
                if Auxporc>porc:
                    porc=Auxporc
                    self.text2=textComparer.lower().replace(",","").split()
                    self.text1=arr.descripcion.lower().split()
                    text1=textComparer.lower().replace(",","")
                    text2=arr.descripcion.lower().replace(",","")
                    item=arr
            return self.order_with_object(item,text1=text1,text2=text2)
        except Exception as err:
            print(str(err))
            pass
        
