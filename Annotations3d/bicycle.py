from enums import status_dict, type_dict
from entry import Entry

class Bicycle(Entry):

    def __init__(self, data):
        super().__init__(data)
        self.status = status_dict[data['attributes']['status']]
        self.b_type = type_dict[data['attributes']['type']]

    
    def generate_bicycle_dict(self):
        return {
            'BICYCLE_ID' : self.bicycle_id,
            'POSITION' : self.position,
            'ORIENTATION' : self.orientation,
            'SIZE' : self.size,
            'STATUS' : self.status,
            'RIDER' : self.rider_id,
            'TYPE' : self.b_type
        }



