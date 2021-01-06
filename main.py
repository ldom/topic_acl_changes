import argparse

from confluent_kafka.admin import AdminClient

from acl_loader import load_acls_from_cluster
from cli_utils import read_json_input
from input import load_input
from topic_loader import load_topics_from_cluster


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
    admin_options = {'bootstrap.servers': '192.168.0.129:9092'}
    ####################################################################################################

    # read JSON input data
    input_data = read_json_input(args.input)
    new_topics, new_acls = load_input(input_data)

    admin_client = AdminClient(admin_options)

    existing_topics = load_topics_from_cluster(admin_client)
    existing_acls = load_acls_from_cluster(admin_client)

    success = True

    if success:
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
