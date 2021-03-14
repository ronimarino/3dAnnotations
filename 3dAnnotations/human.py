from helpers import *
from enums import *

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


