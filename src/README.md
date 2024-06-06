## Uruchomienie
1. Sklonowanie repozytorium
```
git clone https://gitlab-stud.elka.pw.edu.pl/TKOM_24L_AM/Pawel_Rogoz/tkom24l.git
```
2. Przejście na gałąź: "etap_drugi"
```
git checkout etap_drugi
```
3. Pobranie pakietów
```
pip install -r requirements.txt
```
4. Uruchomienie pliku lexer:
#### Argumenty wywołania
* obowiązkowe

    Ścieżka do pliku lub string
    
    Przykład:

```
python3 src/lexer/lexer.py "int a = 1;"
```

```
python3 src/lexer/lexer.py src/lexer/main.pr
```

* opcjonalne
    
    Przy pomocy flagi --max_digit i --max_string możemy określić maksymalną ilość znaków przyjmowanych przy tworzeniu liczby / stringa

    Przykład

```
python3 src/lexer/lexer.py src/lexer/main.pr --max_digit 3 --max_string 300
```
5. Uruchomienie testów jednostkowych
```
pytest
```