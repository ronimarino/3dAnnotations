from helpers import *
from enums import *
from entry import Entry

class Bicycle(Entry):

    def __init__(self, data):
        super().__init__(data)
        self.status = status_dict[data['attributes']['status']]
        self.b_type = type_dict[data['attributes']['type']]



