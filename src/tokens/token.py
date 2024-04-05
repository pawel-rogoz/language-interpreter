class Token:
    def __init__(self, type, position, value = None) -> None:
        self.type = type
        self.position = position
        self.value = value
