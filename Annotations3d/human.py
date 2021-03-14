from enums import *
from entry import Entry

class Human(Entry):

    def __init__(self, data):

        super().__init__(data)
        self.age = age_dict[data['attributes']['age']]
        self.bicycle_id = data['attributes']['rides_on_bicycle']
        if self.bicycle_id != '':
            self.wears_helmet = wears_helmet_dict[data['attributes']['wears_helmet']]
        else:
            self.wears_helmet = 'null'

        
    def generate_human_dict(self):
        return {
            'HUMAN_ID' : self.human_id,
            'POSITION' : self.position,
            'ORIENTATION' : self.orientation,
            'SIZE' : self.size,
            'WEARS_HELMET' : self.wears_helmet,
            'AGE' : self.age 
        }






