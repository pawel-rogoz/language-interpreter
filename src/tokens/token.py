class Token:
    def __init__(self, type, position, value=None) -> None:
        self.type = type
        self.position = position
        self.value = value

    def __str__(self):
        return f"Token Description:\n\tType: {self.type}\n\tPosition:\n\t\tLine: {self.position.line}\n\t\tColumn: {self.position.column}\n\tValue: {self.value}"
