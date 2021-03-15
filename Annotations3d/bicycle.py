from enums import status_dict, type_dict
from entry import Entry
from helpers import keyword_list_bike_attributes



class Bicycle(Entry):


    def __init__(self, data):
        super().__init__(data)
        data_valid = set(keyword_list_bike_attributes).issubset(set(data['attributes'].keys()))
        if data_valid:
            self.status = status_dict[data['attributes']['status']]
            self.b_type = type_dict[data['attributes']['type']]
        else:
            self.status = None
            self.b_type = None

    
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



