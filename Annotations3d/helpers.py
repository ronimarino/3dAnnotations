import numpy as np


def assertDictAlmostEqual(test, d1, d2, msg=None, places=7):

    # check if both inputs are dicts
    if isinstance(d1, dict) and isinstance(d2, dict):
        # check if both inputs have the same keys
        test.assertEqual(d1.keys(), d2.keys())

        # check each key
        for key, value in d1.items():
            if isinstance(value, dict):
                test.assertDictAlmostEqual(d1[key], d2[key], msg=msg)
    elif isinstance(d1, list) and isinstance(d2, list):
        for val in value:
            test.assertDictAlmostEqual(val, val, places=places, msg=msg)
    else:
        test.assertAlmostEqual(d1, d2, places=places, msg=msg)

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


keyword_list_general = [
    'annotationId',
    'frameId',
    'temporalId',
    'label',
    'attributes',
    'x',
    'y',
    'z',
    'roll',
    'pitch',
    'yaw',
    'length',
    'height',
    'width',
    ]

keyword_list_bike_attributes = [
    'status',
    'type',
    ]

keyword_list_human_attributes = [
    'wears_helmet',
    'age',
    'rides_on_bicycle',
    ]


