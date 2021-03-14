import json
import requests
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

class Human:
    annotation_id = 0
    human_id = None
    temporal_id = 0
    frame_id = 0
    label = ''
    position = [0, 0, 0]
    orientation = [0,0,0,1]
    size = [1,1,1]
    wears_helmet = 0
    age = 0
    bicycle_id = 0

    # not used for this purpose
    def quaternion_to_euler(q):
        (x, y, z, w) = (q[0], q[1], q[2], q[3])
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll = math.atan2(t0, t1)
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch = math.asin(t2)
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw = math.atan2(t3, t4)
        return [yaw, pitch, roll]

    def __init__(self, data):
        self.annotation_id = data.annotation_id
        self.temporal_id = data.temporal_id
        self.frame_id = data.frame_id
        self.label = data.label
        self.position = [-data.position[2], -data.position[0], data.position[1]] # converting to customer CS
        # UAI y = yaw, x = roll, z = pitch UAI
        orientation = [data.orientation[0], data.orientation[1], data.orientation[2]] # yaw, pitch, roll
        self.orientation = euler_to_quaternion(orientation[0], orientation[1], orientation[2])
        self.size = [data.size[2], data.size[0], data.size[1]]
        self.age = age_dict[data.attributes['age']]
        self.bicycle_id = data.attributes['rides_on_bicycle']
        if self.bicycle_id != '':
            self.wears_helmet = wears_helmet_dict[data.attributes['wears_helmet']]
        else:
            self.wears_helmet = 'null'


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


def euler_to_quaternion(yaw, pitch, roll):

    yaw, pitch, roll = -roll, yaw, -pitch #converting to customer CS
    
    qx = np.sin(roll/2) * np.cos(yaw/2) * np.cos(pitch/2) - np.cos(roll/2) * np.sin(yaw/2) * np.sin(pitch/2)
    qy = np.cos(roll/2) * np.sin(yaw/2) * np.cos(pitch/2) + np.sin(roll/2) * np.cos(yaw/2) * np.sin(pitch/2)
    qz = np.cos(roll/2) * np.cos(yaw/2) * np.sin(pitch/2) - np.sin(roll/2) * np.sin(yaw/2) * np.cos(pitch/2)
    qw = np.cos(roll/2) * np.cos(yaw/2) * np.cos(pitch/2) + np.sin(roll/2) * np.sin(yaw/2) * np.sin(pitch/2)

    return [qx, qy, qz, qw]

def generate_human_dict(human):
    return {
        'HUMAN_ID' : human.human_id,
        'POSITION' : human.position,
        'ORIENTATION' : human.orientation,
        'SIZE' : human.size,
        'WEARS_HELMET' : human.wears_helmet,
        'AGE' : human.age 
    }

def generate_bicycle_dict(bicycle):
    return {
        'BICYCLE_ID' : bicycle.bicycle_id,
        'POSITION' : bicycle.position,
        'ORIENTATION' : bicycle.orientation,
        'SIZE' : bicycle.size,
        'STATUS' : bicycle.status,
        'RIDER' : bicycle.rider_id,
        'TYPE' : bicycle.b_type
    }

status_dict = {
    'driving' : 0, # 'moving' in the specification
    'stopped' : 1,
    'parked' : 2,
}

type_dict = {
    'normal' : 0,
    'motorized' : 1
}

wears_helmet_dict = {
    False : '0',
    True : '1'
}

age_dict = {
    'adult' : 0,
    'child' : 1
}

annotations_list = None
with open('annotations.json') as input_json_file:  #add command line args
    annotations_list = json.load(input_json_file)
        
if annotations_list:
    output_dict = {}
    output_dict['FRAMES'] = []
    current_frame_id = -1
    parsed_list = []
    for annotation_input in annotations_list:
        annotation = AnnotationInput(annotation_input)

        if annotation.label == 'HUMAN':
            human = Human(annotation)
            parsed_list.append(human)

        elif annotation.label == 'BICYCLE':
            bicycle = Bicycle(annotation)
            parsed_list.append(bicycle)
    
    if len(annotations_list) == len(parsed_list):
        rider_bike_dict = {}
        for i, item in enumerate(parsed_list):
            if isinstance(item, Human):
                item.human_id = i
                if item.bicycle_id != '':
                    rider_bike_dict[item.bicycle_id] = (item.temporal_id, item.human_id)
            elif isinstance(item, Bicycle):
                item.bicycle_id = i

        for item in parsed_list:
            if isinstance(item, Bicycle):
                if item.temporal_id in rider_bike_dict.keys():
                    item.rider_id = rider_bike_dict[item.temporal_id][1]
                else:
                    item.rider_id = 'null'
            if current_frame_id != item.frame_id:
                frame_dict = {'FRAME_ID':item.frame_id}
                if item.label == 'HUMAN':
                    frame_dict['BICYCLES'] = []
                    humans_dict = generate_human_dict(item)
                    frame_dict['HUMANS'] = [humans_dict,]

                elif item.label == 'BICYCLE':
                    bicycles_dict = generate_bicycle_dict(item)
                    frame_dict['BICYCLES'] = [bicycles_dict,]
                    frame_dict['HUMANS'] = []
                    output_dict['FRAMES'].append(frame_dict)
            else:
                frame_dict = output_dict['FRAMES'][-1]
                if item.label == 'HUMAN':
                    humans_dict = generate_human_dict(item)
                    if 'HUMANS' in frame_dict.keys():
                        frame_dict['HUMANS'].append(humans_dict)
                    else:
                        frame_dict['HUMANS'] = [humans_dict,]

                elif item.label == 'BICYCLE':
                    bicycles_dict = generate_bicycle_dict(item)
                    if 'BICYCLES' in frame_dict.keys():
                        frame_dict['BICYCLES'].append(bicycles_dict)
                    else:
                        frame_dict['BICYCLES'] = [bicycles_dict,]
            
            current_frame_id = item.frame_id

    with open('output.json', 'w') as outfile:
        json.dump(output_dict, outfile, indent=2)

        
        


response = requests.get("https://jsonplaceholder.typicode.com/todos")
todos = json.loads(response.text)
