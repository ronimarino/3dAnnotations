import numpy as np

class AnnotationInput:
    annotation_id = None
    frame_id = None
    temporal_id = None
    label = None
    attributes = {}
    position = [0, 0, 0]
    orientation = [0, 0, 0]
    size = [0, 0, 0]

    def __init__(self, data):
        self.annotation_id = data['annotationId']
        self.frame_id = data['frameId']
        self.temporal_id = data['temporalId']
        self.label = data['label']
        self.attributes = data['attributes']
        self.position = (data['x'], data['y'], data['z'])
        self.orientation = (data['yaw'] * np.pi / 180., data['pitch'] * np.pi / 180., data['roll'] * np.pi / 180.)
        self.size = (data['length'], data['height'], data['width'])

