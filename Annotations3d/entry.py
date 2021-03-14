# Base class for bicycle and human objects
import numpy as np
from helpers import euler_to_quaternion

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

    def flush_data(self, frame_dict, new_frame=False):
        if new_frame:
            frame_dict['BICYCLES'] = []
            frame_dict['HUMANS'] = []

        if self.label == 'HUMAN':
            humans_dict = self.generate_human_dict()
            frame_dict['HUMANS'].append(humans_dict)

        elif self.label == 'BICYCLE':
            bicycles_dict = self.generate_bicycle_dict()
            frame_dict['BICYCLES'].append(bicycles_dict)
            
        