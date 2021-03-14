# Base class for bicycle and human objects
import numpy as np
from helpers import *
from enums import *

class Entry:

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