import json
import requests
import urllib
from bicycle import Bicycle
from human import Human

#TODO: sort out human_id - object_id - bicycle_id

import logging
import argparse

logging.basicConfig(filename='annotations.log', level=logging.INFO)
log = logging.getLogger(__name__)


def main(args=None):
    args = init_logging(args)
    if hasattr(args, 'input_json') and hasattr(args, 'output_json'):
        convert_json(args.input_json, args.output_json)
        log.info('######################################################')
        return
    else:
        parser.print_help()
        return


def init_logging(args):
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
    return args


def load_json_from_file_url(input_json):
    annotations_list = []
    try:
        if urllib.parse.urlparse(input_json).scheme != "":
            response = requests.get(input_json)
            annotations_list = json.loads(response.text)
        else:
            with open(input_json) as input_json_file:
                annotations_list = json.load(input_json_file)
        return annotations_list
    except (FileNotFoundError, IOError):
        log.error('Can\'t open the file' + input_json)
        return None
    except (json.JSONDecodeError):
        log.error('Could not decode json file!')
        return None


def parse_annotations(input_json):
    annotations_list = load_json_from_file_url(input_json)
    parsed_list = []
    if annotations_list:
        rider_bike_dict = {} # used for assigning rider to bike
        temporal_id_object_id_dict = {} # used for reusing of object id if object already appeared
        
        object_id = 0

        # instead of object_id, human_id and bicycle_id can be used 
        # human_id = 0
        # bicycle_id = 0
        for annotation_input in annotations_list:
            label_exists = 'label' in annotation_input.keys()
            if label_exists and annotation_input['label'] == 'HUMAN':
                human = Human(annotation_input)
                if not human.is_valid:
                    message = ''
                    if human.annotation_id is not None:
                        message = ' AnnotationId = ' + human.annotation_id
                    elif human.temporal_id is not None:
                        message = ' TemporalId = ' + human.temporal_id
                    log.warning('Corrupted annotation detected!' + message)
                    if human.age is None:
                        log.warning('Corrupted annotation attributes detected!' + message)
                else:
                    if human.temporal_id in temporal_id_object_id_dict.keys():
                        human.human_id = temporal_id_object_id_dict[human.temporal_id]
                    else:
                        human.human_id = object_id
                        temporal_id_object_id_dict[human.temporal_id] = object_id
                        object_id+=1
                    if human.bicycle_id != '':
                        rider_bike_dict[human.bicycle_id] = (human.temporal_id, human.human_id)
                    parsed_list.append(human)

            elif label_exists and annotation_input['label'] == 'BICYCLE':
                bicycle = Bicycle(annotation_input)
                if not bicycle.is_valid:
                    message = '' 
                    if bicycle.annotation_id is not None:
                        message = ' AnnotationId = ' + bicycle.annotation_id
                    elif bicycle.temporal_id is not None:
                        message = ' TemporalId = ' + bicycle.temporal_id
                    log.warning('Corrupted annotation detected!' + message)
                    if bicycle.status is None:
                        log.warning('Corrupted annotation attributes detected!' + message)
                else:
                    if bicycle.temporal_id in temporal_id_object_id_dict.keys():
                        bicycle.bicycle_id = temporal_id_object_id_dict[bicycle.temporal_id]
                    else:
                        bicycle.bicycle_id = object_id
                        temporal_id_object_id_dict[bicycle.temporal_id] = object_id
                        object_id+=1
                    parsed_list.append(bicycle)

            elif not label_exists:
                message = ''
                if 'annotationId' in annotation_input.keys():
                    message = ' AnnotationId = ' + annotation_input['annotationId']
                log.error('Input json file is missing label keyword!' + message)

            else:
                message = ''
                if 'annotationId' in annotation_input.keys():
                    message = ' AnnotationId = ' + annotation_input['annotationId']
                log.error('Input json file has unsupported label value!' + message)

        for item in parsed_list:
            if isinstance(item, Bicycle):
                if item.temporal_id in rider_bike_dict.keys():
                    item.rider_id = rider_bike_dict[item.temporal_id][1]
                else:
                    item.rider_id = None

        if len(annotations_list) != len(parsed_list):
            log.warning('Unrecognized annotations found in input json!')
    return parsed_list


def convert_json(input_json, output_json):
    parsed_list = parse_annotations(input_json)
    if len(parsed_list) > 0:
        output_dict = {}
        output_dict['FRAMES'] = []
        current_frame_id = -1
        
        for item in parsed_list:
            new_frame = False
            if current_frame_id != item.frame_id:
                frame_dict = {'FRAME_ID':item.frame_id}
                new_frame = True
                output_dict['FRAMES'].append(frame_dict)
            else:
                frame_dict = output_dict['FRAMES'][-1]
            item.flush_data(frame_dict, new_frame=new_frame)
            current_frame_id = item.frame_id

        with open(output_json, 'w') as outfile:
            json.dump(output_dict, outfile, indent=2)


if __name__ == "__main__":
   main()




