"""Type definition restrictions

"""

class Restriction:
    def __init__(self, base=None, enum=[]):
        self.base=base
        self.enum=enum
    def __str__(self):
        return "Restriction(base={}, enum={})".format(self.base, self.enum)
    def possible_values(self):
        return self.enum
