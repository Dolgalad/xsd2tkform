"""Annotations

"""

class Annotation:
    def __init__(self, docs={}):
        self.documentation = docs # dictionary where keys are language tags and values are documentation text
    def languages(self):
        return [k for k in self.documentation]
    def __eq__(self, e):
        return self.docs==e.docs
    def __str__(self):
        return "Annotation(languages={})".format(self.languages())

