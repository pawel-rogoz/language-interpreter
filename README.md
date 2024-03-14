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
<!-- 1. keys() - zwraca wszystkie klucze ze słownika w formie listy
2. values() - zwraca wszystkie wartości ze słownika w formie listy
3. add() - dodaje nową parę klucz-wartość do słownika
4. remove() - usuwa parę ze słownika na podstawie podanego klucza
5. forEach() - iterowanie po elementach słownika
6. isKey() - sprawdzenie, czy dany klucz znajduje się w słowniku -->

|   Metoda    | Opis    |   Parametry wywołania |   Typ zwracanej wartości    |
|   :---    |   :---    |   :---    |   :---    |
| keys()      | Zwraca wszystkie klucze występujące w słowniku       | brak   | List
| values()   | Zwraca wszystkie wartości występujące w słowniku         | brak | List |
| add()   | Dodaje nową parę klucz-wartość do słownika | Pair<x,y> para | brak |
| remove()   | Usuwa parę ze słownika | klucz, np: 1 | brak |
| forEach()   | Iterowanie po parach występujących w słowniku| funkcja, która ma być wywołana na danej parze | Zgodna z typem funkcji podanej w parametrze wywołania |
| isKey()   | Sprawdzenie, czy dany klucz znajduje się w słowniku | klucz, np: 1 | bool |

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

#### Przykładowy kod źródłowy
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
    Pair<string,int> osobaPierwsza = new Pair("Jan", 17);
    Pair<string,int> osobaDruga = new Pair("Jakub", 34);
    Pair<string,int> osobaTrzecia = new Pair("Maciej", 46);

    // utworzenie nowego słownika
    Dict wiekOsob = new Dict(osobaPierwsza, osobaDruga);

    // dodawanie elementów do słownika
    wiekOsob.add(osobaTrzecia);

    // usuwanie elementów ze słownika
    wiekOsob.remove("Jan");

    // metody: keys() oraz values()
    List<string> imiona = wiekOsob.keys();
    List<string> wiek = wiekOsob.values();

    // metoda forEach()
    wiekOsob.forEach(wypiszPare());

    while (wiek < 15)
    {
        wiek = wiek + 1;
    }

    return 0;
}
```

#### Formalna specyfikacja i składnia (EBNF):
