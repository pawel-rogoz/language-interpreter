class Block:
    def __init__(self, statements):
        self._statements = statements

    @property
    def statements(self):
        return self._statements
