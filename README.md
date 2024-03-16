# TKOM24L

### Paweł Rogóż

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

    // utworzenie nowej pary
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
```
int main()
{
    int price = 3;
    float fullPrice = (float) price; // fullPrice = 3.00
}
```

* Zmienne przekazywane przez wartość
```
// zmienne przekazywane przez wartość
int addOne(int number)
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
classInitialization = "new", className, "(", arguments, ")"

assignmentOrCall = id, ( ( "(", arguments, ")" | { ".", id, "(", arguments, ")" } ) | "=" expression ), ";"

ifStatement = "if", "(", expression, ")", body, { "else if", "(", expression, ")", body }, [ "else", body]
whileLoop = "while", "(", expression, ")", body
return = "return", expression, ";"

expression = conjuction, { "||", conjuction }
conjuction = relationTerm, { "&&", relationTerm }
relationTerm = additiveTerm, [ relationOperator, additiveTerm ]
additiveTerm = multiplicativeTerm, { ( "+" | "-" ), multiplicativeTerm }
multiplicativeTerm = unaryApplication, { ( "*" | "/" ), unaryApplication }
unaryApplication = [ ( "-" | "!" ) ], castingTerm
castingTerm = [ "(", type ,")" ], term
term = literal | idOrCall | "(", expression, ")" | linqOperation

literal = bool | string | number | floatNumber
idOrCall = id, [ ( "(", arguments, ")" | { ".", id, "(", arguments, ")" } ) ]

arguments = [ expression, { ",", expression } ]

linqOperation = "from", expression, [ "where", expression ], [ "orderby", expression ], "select", expression, ";"

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
| () | 7 | od lewej |
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
| || | 1 | od lewej |

#### Rzutowanie Typów
| Typ 1 | Typ 2 | Operacja | Typ wynikowy |
| ------ | ------ | ----- | ----- |
| string | int | + | string |
| string | float | + | string |
| string | bool | + | string |
| int | float | + | float

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
* Słowa Kluczowe
    * ```If```
    * ```Else```
    * ```While```
    * ```Return```
    * ```Select```
    * ```From```
    * ```Where```
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
    * ```Colon```
    * ```Semicolon```
    * ```Comma```
* Wartości i typy
    * ```Id```
    * ```Comment```
    * ```StringValue```
    * ```IntValue```
    * ```FloatValue```
    * ```BoolValue```
