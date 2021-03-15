from enums import wears_helmet_dict, age_dict
from entry import Entry
from helpers import keyword_list_human_attributes

class Human(Entry):

    def __init__(self, data):

        super().__init__(data)
        data_valid = True
        if 'attributes' in data.keys():
            data_valid = set(keyword_list_human_attributes).issubset(set(data['attributes'].keys()))
        if data_valid:
            self.age = age_dict[data['attributes']['age']]
            self.bicycle_id = data['attributes']['rides_on_bicycle']
            if self.bicycle_id != '':
                self.wears_helmet = wears_helmet_dict[data['attributes']['wears_helmet']]
            else:
                self.wears_helmet = None
        else:
            self.is_valid = False
            self.age = None
            self.bicycle_id = None
            self.wears_helmet = None

        
    def generate_human_dict(self):
        return {
            'HUMAN_ID' : self.human_id,
            'POSITION' : self.position,
            'ORIENTATION' : self.orientation,
            'SIZE' : self.size,
            'WEARS_HELMET' : self.wears_helmet,
            'AGE' : self.age 
        }






