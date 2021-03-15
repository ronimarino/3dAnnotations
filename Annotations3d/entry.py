# Base class for bicycle and human objects
import numpy as np
from helpers import euler_to_quaternion, keyword_list_general



class Entry:


    def __init__(self, data):
        data_valid = set(keyword_list_general).issubset(set(data.keys()))
        if data_valid:
            self.annotation_id = data['annotationId']
            self.temporal_id = data['temporalId']
            self.frame_id = data['frameId']
            self.label = data['label']
            self.position = [-data['z'], -data['x'], data['y']] # converting to customer CS
            # UAI y = yaw, x = roll, z = pitch UAI
            orientation = (data['yaw'] * np.pi / 180., data['pitch'] * np.pi / 180., data['roll'] * np.pi / 180.) # yaw, pitch, roll
            self.orientation = euler_to_quaternion(orientation[0], orientation[1], orientation[2])
            self.size = [data['width'], data['length'], data['height']] # converting to customer CS
            self.is_valid = True
        else:
            if 'annotationId' in data.keys():
                self.annotation_id = data['annotationId']
            else:
                self.annotation_id = None
            if 'temporalId' in data.keys():
                self.temporal_id = data['temporalId']
            else:
                self.temporal_id = None
            self.frame_id = None
            self.label = None
            self.position = [0., 0., 0.]
            self.orientation = [0., 0., 0., 1.]
            self.size = [0., 0., 0.]
            self.is_valid = False


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
