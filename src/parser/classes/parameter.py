class Parameter:
    def __init__(self, type, id):
        self._type = type
        self._id = id

    @property
    def type(self):
        return self._type

    @property
    def id(self):
        return self._id
