from src.scanner.scanner import Scanner
from io import StringIO

if __name__ == "__main__":
    scanner = Scanner(StringIO("int a = 1;"))
    print("Hello world")