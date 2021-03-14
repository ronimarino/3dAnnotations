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
        self.annotation_id = data['annotationId']
        self.temporal_id = data['temporalId']
        self.frame_id = data['frameId']
        self.label = data['label']
        self.position = [-data['z'], -data['x'], data['y']] # converting to customer CS
        # UAI y = yaw, x = roll, z = pitch UAI
        orientation = (data['yaw'] * np.pi / 180., data['pitch'] * np.pi / 180., data['roll'] * np.pi / 180.) # yaw, pitch, roll
        self.orientation = euler_to_quaternion(orientation[0], orientation[1], orientation[2])
        self.size = [data['width'], data['length'], data['height']] # converting to customer CS
        self.status = status_dict[data['attributes']['status']]
        self.b_type = type_dict[data['attributes']['type']]



