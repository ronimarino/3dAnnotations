import numpy as np


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

