from helpers import *
from enums import *

class Bicycle:
    annotation_id = 0
    bicycle_id = None
    temporal_id = 0
    frame_id = 0
    label = ''
    position = [0, 0, 0]
    orientation = [0,0,0,1]
    size = [1,1,1]
    status = 0
    b_type = 0
    rider_id = 0

    def __init__(self, data):
        self.annotation_id = data.annotation_id
        self.temporal_id = data.temporal_id
        self.frame_id = data.frame_id
        self.label = data.label
        self.position = [-data.position[2], -data.position[0], data.position[1]] # converting to customer CS
        # UAI y = yaw, x = roll, z = pitch UAI
        orientation = [data.orientation[0], data.orientation[1], data.orientation[2]] # yaw, pitch, roll
        self.orientation = euler_to_quaternion(orientation[0], orientation[1], orientation[2])
        #import pdb
        #pdb.set_trace()
        self.size = [data.size[2], data.size[0], data.size[1]]
        self.status = status_dict[data.attributes['status']]
        self.b_type = type_dict[data.attributes['type']]



