import json
import requests
from helpers import *
from enums import *
from annotation_input import AnnotationInput
from bicycle import Bicycle
from human import Human

#TODO: cli arguments
#TODO: cli help
#TODO: split functions
#TODO: tests
#TODO: error handlin & log 
#TODO: log level option cli argument
#TODO: improve readme (cli help kopiraj, setup kako se radi)
#TODO: Entry klasa koju nasljedjuju Bicycle i Human
#TODO: Parsiranje da je u Bycicle i Human klasama
#TODO: BicycleWithRider klasu


import logging
import argparse

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def main(args=None):

    parser = argparse.ArgumentParser(prog='annotations', description='Command line interface for Export 3d Annotations')
    parser.add_argument(
        'input_json', default='annotations.json', help='Input file'
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

    if hasattr(args, 'input_json') and hasattr(args, 'output_json'):
        run(args.input_json, args.output_json)
        return 0
    else:
        parser.print_help()
        return 0

    # log.debug('some debug')
    # log.info('some info')
    # log.warning('some warning')

def run(input_json, output_json):
    annotations_list = None
    with open(input_json) as input_json_file:
        annotations_list = json.load(input_json_file)
            
    if annotations_list:
        output_dict = {}
        output_dict['FRAMES'] = []
        current_frame_id = -1
        parsed_list = []
        for annotation_input in annotations_list:
            if annotation_input['label'] == 'HUMAN':
                human = Human(annotation_input)
                parsed_list.append(human)

            elif annotation_input['label'] == 'BICYCLE':
                bicycle = Bicycle(annotation_input)
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

        with open(output_json, 'w') as outfile:
            json.dump(output_dict, outfile, indent=2)

            
            


        response = requests.get("https://jsonplaceholder.typicode.com/todos")
        todos = json.loads(response.text)

main()




