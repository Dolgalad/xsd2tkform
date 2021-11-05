"""Simple type value list definition
"""

class List:
    def __init__(self, item_type=None):
        self.item_type = None
    def __str__(self):
        return "List(item_type={})".format(self.item_type)
