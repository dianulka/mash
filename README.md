# Opis programu
Program ten jest interpreterem języka mash, napisanego przy użyciu narzędzia ANTLR (Another Tool for Language Recognition). Język mash jest prostym językiem skryptowym, który pozwala na wykonywanie podstawowych operacji arytmetycznych, logicznych oraz manipulację zmiennymi. Dodatkowo, język ten wspiera struktury kontrolne, takie jak pętle (while, for) oraz instrukcje warunkowe (if, elif, else).

# Technologie
Program wykorzystuje następujące technologie i narzędzia:

- ANTLR (Another Tool for Language Recognition): Narzędzie do tworzenia parserów dla różnych języków programowania.
- Python: Główny język programowania używany do implementacji interpretera.
- ANTLR4 Runtime for Python: Biblioteka potrzebna do uruchomienia parsera wygenerowanego przez ANTLR w Pythonie.

Pliki projektu
- mash.g4: Plik gramatyki dla języka mash w formacie ANTLR.
- mashLexer.py, mashParser.py, mashVisitor.py: Pliki wygenerowane przez ANTLR na podstawie pliku gramatyki mash.g4.
- mashVisitorCustom.py: Niestandardowy visitor, który implementuje logikę wykonywania kodu w języku mash.
- main.py: Główny plik uruchamiający interpreter.

# Struktura gramatyki
Gramatyka języka mash definiuje następujące elementy:

- Program: Sekwencja instrukcji zakończona końcem pliku (EOF).
- Instrukcje: Mogą być wywołaniami funkcji echo, deklaracjami zmiennych, przypisaniami wartości do zmiennych, oraz strukturami kontrolnymi (if, while, for).
- Wyrażenia: Arytmetyczne, logiczne, porównania, oraz identyfikatory.
- Deklaracje zmiennych: Deklaracja zmiennych typu string_var lub int_var z opcjonalnym przypisaniem wartości.
- Pętle: while oraz for.
- Instrukcje warunkowe: if, elif, else.

Implementacja mashVisitorCustom
Klasa mashVisitorCustom jest implementacją visitora, który odwiedza węzły drzewa parsowania i wykonuje odpowiednie działania. Poniżej opisano niektóre z głównych metod:

- visitProgram: Przetwarza wszystkie instrukcje programu.
- visitEcho_function: Wykonuje funkcję echo, wypisując na standardowe wyjście wartość wyrażenia lub zmiennej.
- visitVar_declar: Deklaruje zmienne i przypisuje im wartości.
- visitAssignment: Przypisuje wartości do wcześniej zadeklarowanych zmiennych.
- visitIf_statement: Wykonuje instrukcję warunkową if-elif-else.
- visitWhile_statement: Wykonuje pętlę while.
- visitFor_statement: Wykonuje pętlę for.

# Przykładowe użycie
Poniżej przedstawiono przykładowy kod w języku mash oraz sposób jego przetworzenia przez interpreter.

Przykładowy kod w języku mash (zapisany w pliku test.mash):

'''
if (x > 5) {
    echo "x is greater than 5"
} elif (x == 5) {
    echo "x is equal to 5"
} else {
    echo "x is less than 5"
}
'''

# Instalacja i uruchomienie
Aby uruchomić interpreter, wykonaj poniższe kroki:

1. Zainstaluj ANTLR4:
'''
pip install antlr4-python3-runtime

2. Wygeneruj pliki parsera za pomocą ANTLR4:
'''
antlr4 -Dlanguage=Python3 mash.g4
'''

3. Uruchom interpreter:
'''
python main.py
'''

# Podsumowanie
Interpreter języka mash jest prostym narzędziem, które ilustruje użycie ANTLR do tworzenia parserów i interpreterów. Program obsługuje podstawowe operacje na zmiennych, wyrażenia arytmetyczne i logiczne, oraz struktury kontrolne, co pozwala na wykonywanie prostych skryptów.
