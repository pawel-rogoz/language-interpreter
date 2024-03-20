# TKOM24L
Paweł Rogóż
### Elementy dokumentu
[[*TOC*]]

#### Temat projektu:
Język z wbudowanym typem słownika z określoną kolejnością elementów. Kolejność elementów w słowniku jest tożsama z kolejnością wstawiania do niego elementów. Możliwe są podstawowe operacje na słowniku (dodawanie, usuwanie, wyszukiwanie elementów wg klucza, sprawdzanie, czy dany klucz znajduje się w słowniku itd.), iterowanie po elementach oraz wykonywanie na słowniku zapytań w stylu LINQ.

###### Cechy języka:
 - język typowany statycznie, silnie

#### Założenia:
 - język zostanie zaimplementowany w języku Python
 - język posiada trzy wbudowane klasy: ```List``` , ```Pair``` , ```Dict``` 
 - typy języka: ```string```, ```int```, ```bool```, ```float```
 - język udostępnia instrukcję warunkową ```if else```
 - język udostępnia pętlę ```while```
 - każdy program musi posiadać funkcję ```main```
 - język pozwala na tworzenie oraz wywoływanie funkcji (posiada typ void dla funkcji, które nie zwracają żadnych wartości)
 - język pozwala na tworzenie komentarzy
 - maksymalna długość stringa: 256
 - maksymalna wielkość liczby: 10 cyfr

#### Klasa ```List```
 - tworzenie instancji klasy:
```
List<int> przykladowa_lista = new List();
```
 - instancja może też zostać zainicjowana wraz z początkowymi wartościami:
```
List<int> przykladowa_lista = new List(1,2,3);
```
- metody klasy:
1. length() - metoda zwraca długość listy
2. forEach() - metoda pozwala na iterowanie po wszystkich elementach listy
3. push() - dodaje element na koniec listy
4. pop() - usuwa element z końca listy
5. [ index ] - klasa umożliwia pobieranie / ustawianie wartości dla danego indeksu
```
int number = przykladowa_lista[0]; // number: 1
przykladowa_lista[0] = 2; // przykladowa_lista: 2,2,3
```

#### Klasa ```Pair```
 - tworzenie instancji klasy:
```
Pair<string,int> przykladowa_para = new Pair("age", 10);
```
 - instancja musi zostać zainicjowana wraz z początkowymi wartościami
 - metody klasy:
1. key() - zwraca klucz pary
2. value() - zwraca wartość pary

#### Klasa ```Dict```
 - tworzenie instancji klasy:
```
Dict<string,int> przykladowy_slownik = new Dict();
```
 - instancja może też zostać zainicjowana wraz w początkowymi wartościami:
 ```
 Dict<string,int> przykladowy_slownik = new Dict("age": 10);
 ```
 - metody klasy:

|   Metoda    | Opis    |   Parametry wywołania |   Typ zwracanej wartości    |
|   :---    |   :---    |   :---    |   :---    |
| keys()      | Zwraca wszystkie klucze występujące w słowniku       | brak   | List
| values()   | Zwraca wszystkie wartości występujące w słowniku         | brak | List |
| add()   | Dodaje nową parę klucz-wartość do słownika | Pair<x,y> para | brak |
| remove()   | Usuwa parę ze słownika | klucz, np: 1 | brak |
| forEach()   | Iterowanie po parach występujących w słowniku| funkcja, która ma być wywołana na danej parze | Zgodna z typem funkcji podanej w parametrze wywołania |
| isKey()   | Sprawdzenie, czy dany klucz znajduje się w słowniku | klucz, np: 1 | bool |
| length() | Zwraca ilość elementów w słowniku | brak | Int |
| [key] | Pozwala na pobieranie i ustawianie wartości znajdujących się w słowniku pod danym kluczem | key | Zgodna z typem wartości |
```
int age = przykladowy_slownik["age"]; // age: 10
przykladowy_slownik["age"] = 20; // przykladowy_slownik: ("age": 20)
```

#### Sposób uruchomienia
Program będzie aplikacją konsolową, jego argumentem wywołania jest ścieżka do pliku zawierającego kod źródłowy
```
python3 interpreter.py kod_zdrodlowy.txt
```

#### Obsługa błędów
Program będzie zwracać kod błędu, oraz wiersz i kolumnę, w których ten błąd występuje:

Przykład:
```
ERROR: Can't assign 'string' for type 'int', at: line 10, column 3
```
Przykładowe błędy:
* Pobieranie / ustawianie przez indeks
```
int main()
{
    string xyz = "xyz";
    List<int> przykladowa_lista = new List(1,2,3,4,5);

    przykladowa_lista[xyz] = 10;
}
```

```
ERROR: index must be type 'int', at line 6, column 19
```

* Długość cyfry większa od 10
```
int main()
{
    int number = 10000000000;
}
```

```
ERROR: int too big (max 999999999), at line 3, column 14
```

* Długość stringa wieksza od 256
```
int main()
{
    string name = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
}
```

```
ERROR: string too long (max 256), at line 3, column 10
```

* Inicjalizacja z wartością innego typu
```
int main()
{
    string name = 1;
}
```

```
ERROR: Can't assign type 'int' for 'string', at line 3, column 14
```

* Redefinicja zmiennych
```
int main()
{
    string name = "Anna";
    name = 1;
}
```

```
ERROR: Can't assign type 'int' for 'string', at line 4, column 7
```

* Wywołanie funkcji ze zbyt małą liczbą argumentów
```
int addOne(int number)
{
    number += 1;
}

int main()
{
    addOne();
}
```

```
ERROR: addOne takes 1 argument, 0 given, at line 8, column 0
```

* Próba rzutowania typów niemożliwych do zrzutowania
```
int main()
{
    string name = "Anna";
    int number = (int) name;
}
```

```
ERROR: Can't cast string to int, at line 4, column 20
```

* Operacje LINQ - przypisanie do zmiennej nieodpowiedniego typu
```
int main()
{
    List<int> liczby = new List(0,1,2,3);

    int wiekszeOdJednego = select liczba where liczba > 1 from liczby;
}
```

```
ERROR: Can't assign 'List' to 'int', at line 5, column 25
```

* Brak średnika
```
int main()
{
    string imie = 'Anna'
}
```

```
ERROR: ';' expected, at line 3, column 20
```

#### Przykładowe kody źródłowe
* Podstawowe operacje
```
void wypiszPare(Pair<string,int> para)
{
    print("Klucz: " + para.key() + ", wartość: " + para.value());
}

int main()
{
    // typy zmiennych w języku
    int wiek = 10;
    float pi = 3.14;
    bool czyJestKluczem = true;
    string imie = "Jan";

    // rzutowania zmiennych
    int waga = (int) 85.5; // waga: 85
    float wagaFloat = (float) waga; //wagaFloat: 85.00
    int czyJestPuste = (int) true;
    string numer = (string) 10;

    // utworzenie nowych par
    Pair<string,string> krajPierwszy = new Pair("Anglia", "Londyn");
    Pair<string,string> krajDrugi = new Pair("Polska", "Warszawa");
    Pair<string,string> krajTrzeci = new Pair("Niemcy", "Berlin");

    // utworzenie nowego słownika
    Dict<string,string> stoliceKrajow = new Dict(krajPierwszy, krajDrugi);

    // dodawanie elementów do słownika
    stoliceKrajow.add(krajTrzeci);

    // usuwanie elementów ze słownika
    stoliceKrajow.remove("Anglia");

    // metody: keys() oraz values()
    List<string> kraje = stolice.keys();
    List<string> stolice = stolice.values();

    // metoda forEach()
    stoliceKrajow.forEach(wypiszPanstwo());

    while (wiek < 15)
    {
        wiek = wiek + 1;
    }

    return 0;
}
```

* Rzutowanie Typów
Tabela pokazująca możliwe sposoby rzutowania typów jest umieszczona niżej
```
int main()
{
    int price = 3;
    float fullPrice = (float) price; // fullPrice = 3.00
    fullPrice = 3.45;
    int backToPrice = (int) fullPrice; // fullPrice = 3
}
```

* Widoczność zmiennych
Zmienne w pliku mają zakres blokowy, w związku z czym zmienna 'age' nie jest widoczna z poziomu funkcji
```
int main()
{
    int number = 3;

    if (true)
    {
        int age = 10;
        number = number + 1;
    }

    print(age); // ERROR: 'age' is not defined
    print(number); // 4
    
}
```

* Zmienne przekazywane przez wartość
Jako, że zmienne przekazywane są przez wartość, podanie zmiennej 'number' jako parametr wywołania funkcji addOne nie zmieni jej wartości
```
// zmienne przekazywane przez wartość
void addOne(int number)
{
    number = number + 1;
}

int main()
{
    int number = 3;
    addOne(number);
    print(number); // 3, brak zmian
}
```

* Zmienne niemutowalne
Przykład poniżej ukazuje, że zmiana wartości dla klucza "Anglia" nie zmieni wartości zapisanej w słowniku stoliceKrajow
```
int main()
{
    Pair<string,string> krajPierwszy = new Pair("Anglia", "Londyn");

    Dict<string,string> stoliceKrajow = new Dict(krajPierwszy);

    stoliceKrajow["Anglia"] = "XYZ"; // krajPierwszy["Anglia"] = Londyn
}
```

* Funkcje rekurencyjne
```
int fibonacci(int n)
{
    if (n < 3)
    {
        return 1;
    }

    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main()
{
    fib(5);
}
```

* Operacje LINQ - WHERE, List
Operacje LINQ można używać tylko do przypisania wartości do zmiennej. Użycie słów kluczowych WHERE, oraz ORDERBY jest opcjonalne, w przeciwieństwie do SELECT i FROM. Operacja zwraca wszystkie elementy spełniające podany warunek
```
int main()
{
    List<int> liczby = new List(0,1,2,3);

    List<int> wiekszeOdJeden = select liczba where liczba > 1 from liczby; // 2,3
}
```

* Operacje LINQ - ORDER BY, List
Słowa kluczowe ASC, DESC umożliwiają sortowanie wyników rosnąco / malejąco
```
int main()
{
    List<int> liczby = new List(1, 4, 3, 0, 2);

    List<int> wiekszeOdJeden = select liczba where liczba > 1 orderby liczba ASC from liczby; // 2,3,4
}
```

* Operacje LINQ - WHERE, Dict
```
int main()
{
    Pair<string,int> oszczednosciJacka = new Pair("Jacek", 100);
    Pair<string,int> oszczednosciMarcina = new Pair("Marcin", 250);
    Pair<string,int> oszczednosciKrzysztofa = new Pair("Krzysztof", 150);

    Dict<string,int> oszczednosci = new Dict(oszczednosciJacka, oszczednosciMarcina, oszczednosciKrzysztofa);

    List<Pair<string,int>> wiekszeOdDwustu = select pair where pair.value() > 200 from oszczednosci; // [("Marcin", 250)]
}
```

* Operacje LINQ - ORDER BY, Dict
W przypadku słowników operujemy na umieszczonych w nich parach. Możemy zwracać cała parę lub jej składowe (key, value). Wynik zapytania umieszczony jest w nowej liście
```
int main()
{
    Pair<string,int> oszczednosciJacka = new Pair("Jacek", 100);
    Pair<string,int> oszczednosciMarcina = new Pair("Marcin", 250);
    Pair<string,int> oszczednosciKrzysztofa = new Pair("Krzysztof", 150);

    Dict<string,int> oszczednosci = new Dict(oszczednosciJacka, oszczednosciMarcina, oszczednosciKrzysztofa);

    List<Pair<string,int>> wiekszeOdStu = select pair where pair.value() > 200 orderby pair.key() ASC from oszczednosci; // [("Krzysztof", 150), ("Marcin", 250)]
}
```

#### Formalna specyfikacja i składnia (EBNF):
##### Część składniowa
```
program = { functionDefinition }

functionDefinition = functionType, id, "(", [ functionArgument, { ",", functionArgument } ], ")", body

body = "{", { statement }, "}"
functionArgument = declaration

statement = { initialization
            | assignmentOrCall
            | return
            | ifStatement
            | whileLoop
            }

initialization = declaration, [ assignment ], ";"
declaration = type, id
assignment = "=", ( expression | classInitialization )
classInitialization = "new", className, "(", parameters, ")"

assignmentOrCall = idOrCall, [ "=", expression ], ";"

ifStatement = "if", "(", expression, ")", body, [ { "else if", "(", expression, ")", body }, "else", body ]
whileLoop = "while", "(", expression, ")", body
return = "return", expression, ";"

expression = conjuction, { "||", conjuction }
conjuction = relationTerm, { "&&", relationTerm }
relationTerm = additiveTerm, [ relationOperator, additiveTerm ]
additiveTerm = multiplicativeTerm, { ( "+" | "-" ), multiplicativeTerm }
multiplicativeTerm = unaryApplication, { ( "*" | "/" ), unaryApplication }
unaryApplication = [ ( "-" | "!" ) ], castingIndexingTerm
castingIndexingTerm = [ "(", type ,")" ], term, [ "[", expression, "]" ]
term = literal | idOrCall | "(", expression, ")" | linqOperation

literal = bool | string | number | floatNumber
idOrCall = id, [ { [ ".", id ], "(", parameters, ")", } ], [ "[", expression, "]" ]

parameters = [ expression, { ",", expression } ]

linqOperation = "from", expression, [ "where", expression ], [ "orderby", expression, ( "ASC", "DESC" ) ], "select", expression, ";"

id = letter, { letter }
```

##### Część leksykalna
```
type = "int"
    | "float"
    | "string"
    | "bool"
    | classType
classType = className, "<", type, [ "," type ], ">"
className = "Dict" | "List" | "Pair"
funcType = "void" | type
relationOperator = ">", "<", ">=", "<=", "==", "!="

bool = "true" | "false"
nonZeroDigit = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
digit = "0" | nonZeroDigit
letter = "a-z" | "A-Z"
number = nonZeroDigit, { digit }
floatNumber = ( "0" | nonZeroDigit, { digit } ), ".", digit, { digit }
string = '"', { letter | digit }, '"'
```

#### Priorytety Operatorów

| Operator | Priorytet | Łączność |
| ------ | ------ | ----- |
| () | 8 | brak |
| [] | 7 | brak |
| ! | 6 | brak |
| - (unarnie) | 6 | brak |
| * | 5 | od lewej |
| / | 5 | od lewej |
| + | 4 | od lewej |
| - (binarnie) | 4 | od lewej |
| > | 3 | brak |
| < | 3 | brak |
| >= | 3 | brak |
| <= | 3 | brak |
| == | 3 | brak |
| != | 3 | brak |
| && | 2 | od lewej |
| \|\| | 1 | od lewej |

#### Rzutowanie Typów
| Typ Podstawowy | Typ Rzutowania | Działanie | Przykład
| ------ | ------ | ----- | ----- |
| int | string | "{int}" | ```string liczba = (string) 1; // liczba: "1"```|
| float | string | "{float}" | ```string liczba = (string) 1.5; // liczba: "1.5"```|
| bool | string | "( true \| false)" | ```string isEmpty = (string) true; // isEmpty: "true"```
| float | int | ```Math.floor(float)``` | ```int liczba = (int) 1.5; // liczba: 1``` |
| bool | int | ```0 \| 1``` | ```int liczba = (int) true; //liczba: 1``` |

#### Tokeny
Rodzaje tokenów:
* Operatory Porównania
    * ```Greater```
    * ```Less```
    * ```GreaterEqual```
    * ```LessEqual```
    * ```Equal```
    * ```NotEqual```
* Operatory Arytmetyczne
    * ```Plus```
    * ```Minus```
    * ```Multiply```
    * ```Divide```
* Operatory Logiczne
    * ```And```
    * ```Or```
    * ```Negate```
* Nawiasowanie
    * ```RoundOpen```
    * ```RoundClose```
    * ```CurlyOpen```
    * ```CurlyClose```
    * ```SquareOpen```
    * ```SquareClose```
* Słowa Kluczowe
    * ```If```
    * ```Else```
    * ```While```
    * ```Return```
    * ```Select```
    * ```From```
    * ```Where```
    * ```New```
* Operacje LINQ
    * ```Select```
    * ```Where```
    * ```From```
    * ```OrderBy```
    * ```ASC```
    * ```DESC```
* Typy
    * ```Int```
    * ```Float```
    * ```Bool```
    * ```String```
    * ```Pair```
    * ```List```
    * ```Dict```
* Przypisanie
    * ```Assign```
* Podział
    * ```Dot```
    * ```Semicolon```
    * ```Comma```
* Wartości i typy
    * ```Id```
    * ```Comment```
    * ```StringValue```
    * ```IntValue```
    * ```FloatValue```
    * ```BoolValue```
* Strumień tekstowy
    * ```EOT```

Struktura interpretera
* Tokeny
    * token zawierać będzie typ tokenu (jeden z powyższych), jego pozycję (wiersz, kolumna, odległość od początku pliku w bajtach), oraz wartość, która będzie definiowana tylko dla niektórych typów tokenów (np. BoolValue), a domyślnie zdefiniowana na None
* Analiza strumieni wejścia
    * klasa Scanner - pobiera pojedynczo znaki ze źródła
    * metody klasy:
        * next() - pobiera następny znak
        * current() - zwraca obecny znak
        * position() - zwraca pozycję (wiersz, kolumna, odległość)
* Analiza leksykalna
    * klasa Lexer - otrzymuje znaki od obiektu Scanner, z otrzymanych znaków tworzy tokeny
    * metody klasy:
        * next() - tworzy kolejny token
        * current() - zwraca ostatnio utworzony token
        * position() - zwraca pozycję ostatniego tokena
    * klasa Filter - pośrednik w komunikacji między lekserem a parserem, odpowiada za przesyłanie tylko wartościowych z punktu widzenia Parsera tokenów, (np pomija token Comment)
* Analiza składniowa
    * klasa Parser - z otrzymanych od klasy Lexer tokenów tworzy drzewa AST
    * metody klasy:
        * parse() - tworzy drzewo AST
* Analiza semantyczna
    * klasa SemanticChecker - sprawdza dane drzewo AST pod względem błędów semantycznych
    * metody klasy:
        * check() - sprawdzenie drzewa
* Interpretacja
    * Interpreter - wykonuje instrukcje z drzewa AST
    * metody klasy:
        * interpret() - wykonuje instrukcje z drzewa AST, zwraca wartość z funkcji main lub błędy powstałe przy interpretacji
