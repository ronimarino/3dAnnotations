import json
import requests
import urllib
from helpers import *
from enums import *
from bicycle import Bicycle
from human import Human

#TODO: tests
#TODO: error handlin & log - dict keywords checks
#TODO: improve readme (cli help kopiraj, setup kako se radi)


import logging
import argparse

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def main(args=None):

    parser = argparse.ArgumentParser(prog='annotations', description='Command line interface for Export 3d Annotations')
    parser.add_argument(
        'input_json', default='annotations.json', help='Input file or web url'
    )
    parser.add_argument(
        'output_json', default='output.json', help='Output file'
    )
    parser.add_argument(
        '--loglevel', default='info', help='Log level',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
    )
    


    # Parse all command line arguments
    args = parser.parse_args(args)
    if args.loglevel == 'debug':
        log.setLevel(logging.DEBUG)
    elif args.loglevel == 'warning':
        log.setLevel(logging.WARNING)
    elif args.loglevel == 'error':
        log.setLevel(logging.ERROR)
    elif args.loglevel == 'critical':
        log.setLevel(logging.CRITICAL)
    
    if hasattr(args, 'input_json') and hasattr(args, 'output_json'):
        convert_json(args.input_json, args.output_json)
        return
    else:
        parser.print_help()
        return

    # log.debug('some debug')
    # log.info('some info')
    # log.warning('some warning')


def parse_annotations_from_file(input_json):
    annotations_list = None
    try:
        if urllib.parse.urlparse(input_json).scheme != "":
            response = requests.get(input_json)
            annotations_list = json.loads(response.text)
            #https://jsonplaceholder.typicode.com/todos
        else:
            with open(input_json) as input_json_file:
                annotations_list = json.load(input_json_file)
    except (FileNotFoundError, IOError):
        log.error('Can\'t open the file' + input_json)
        return []
    except (json.JSONDecodeError):
        log.error('Could not decode json file!')
        return []

    
    parsed_list = []
    if annotations_list:
        rider_bike_dict = {} # used for assigning rider to bike
        temporal_id_object_id_dict = {} # used for reusing of object id if object already appeared
        
        object_id = 0

        # instead of object_id, human_id and bicycle_id can be used 
        # human_id = 0
        # bicycle_id = 0
        for annotation_input in annotations_list:
            if annotation_input['label'] == 'HUMAN':
                human = Human(annotation_input)
                if human.temporal_id in temporal_id_object_id_dict.keys():
                    human.human_id = temporal_id_object_id_dict[human.temporal_id]
                else:
                    human.human_id = object_id
                    temporal_id_object_id_dict[human.temporal_id] = object_id
                    object_id+=1
                if human.bicycle_id != '':
                    rider_bike_dict[human.bicycle_id] = (human.temporal_id, human.human_id)
                parsed_list.append(human)

            elif annotation_input['label'] == 'BICYCLE':
                bicycle = Bicycle(annotation_input)
                if bicycle.temporal_id in temporal_id_object_id_dict.keys():
                    bicycle.bicycle_id = temporal_id_object_id_dict[bicycle.temporal_id]
                else:
                    bicycle.bicycle_id = object_id
                    temporal_id_object_id_dict[bicycle.temporal_id] = object_id
                    object_id+=1
                parsed_list.append(bicycle)

        for item in parsed_list:
            if isinstance(item, Bicycle):
                if item.temporal_id in rider_bike_dict.keys():
                    item.rider_id = rider_bike_dict[item.temporal_id][1]
                else:
                    item.rider_id = 'null'

    if len(annotations_list) != len(parsed_list):
        log.warning('Unrecognized annotations found in input json!')
    return parsed_list


def convert_json(input_json, output_json):
    parsed_list = parse_annotations_from_file(input_json)
    if len(parsed_list) > 0:
        output_dict = {}
        output_dict['FRAMES'] = []
        current_frame_id = -1

        for item in parsed_list:
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

        with open(output_json, 'w') as outfile:
            json.dump(output_dict, outfile, indent=2)

main()




