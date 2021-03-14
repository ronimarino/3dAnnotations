import numpy as np


def euler_to_quaternion(yaw, pitch, roll):

    yaw, pitch, roll = -roll, yaw, -pitch #converting to customer CS
    
    qx = np.sin(roll/2) * np.cos(yaw/2) * np.cos(pitch/2) - np.cos(roll/2) * np.sin(yaw/2) * np.sin(pitch/2)
    qy = np.cos(roll/2) * np.sin(yaw/2) * np.cos(pitch/2) + np.sin(roll/2) * np.cos(yaw/2) * np.sin(pitch/2)
    qz = np.cos(roll/2) * np.cos(yaw/2) * np.sin(pitch/2) - np.sin(roll/2) * np.sin(yaw/2) * np.cos(pitch/2)
    qw = np.cos(roll/2) * np.cos(yaw/2) * np.cos(pitch/2) + np.sin(roll/2) * np.sin(yaw/2) * np.sin(pitch/2)

    return [qx, qy, qz, qw]

# not used for this purpose, but could be useful for import of customer data
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

