import argparse

from confluent_kafka.admin import AdminClient

from cli_utils import read_json_input
from input import load_input


UID_TOPIC_NAME = "uids"
READ_TIMEOUT = 2.0

"""
example input JSON
{
    'uid': 17,
    'environment': 'RND',
    'topics_to_recreate': [
        'aaa',
        'bbb'
    ]
}
"""

JSON_INPUT_UID = "uid"
JSON_INPUT_ENV = "environment"
JSON_INPUT_RECREATE_TOPICS = "topics_to_recreate"


def handle_arguments():
    parser = argparse.ArgumentParser(
        description="Reads a JSON file with topics to delete. Returns 0 for success, otherwise 1. "
    )

    parser.add_argument("-i", "--input", help="JSON input file")
    parser.add_argument("-o", "--output", help="Output file")

    return parser.parse_args()


def main():
    # get the command line arguments
    args = handle_arguments()

    ####################################################################################################
    # TODO update options
    ####################################################################################################
    bootstrap_servers = '192.168.0.129:9092'
    admin_options = {'bootstrap.servers': bootstrap_servers}
    consumer_options = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'test_safe_delete'
    }
    producer_options = {'bootstrap.servers': bootstrap_servers}
    ####################################################################################################

    # read JSON input data
    input_data = read_json_input(args.input)
    input_objects = load_input(input_data)

    success = True

    if success:
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
