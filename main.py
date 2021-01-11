import argparse

from confluent_kafka.admin import AdminClient

from acl import ACL
from classify import classify_acls, classify_topics
from cli_utils import read_json_input
from input import load_input
from topic import Topic


def handle_arguments():
    parser = argparse.ArgumentParser(
        description="Reads a JSON file with topics to delete. Returns 0 for success, otherwise 1. "
    )

    parser.add_argument("-i", "--input", help="JSON input file")
    parser.add_argument("-o", "--output", help="Output file")

    parser.add_argument("-c", "--config", help="Config properties for connecting to the cluster, in JSON format. "
                                               "Minimum = '{ \"bootstrap.servers\": \"<ip-or-dns-name>:9092\" }'")

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
    after_topics, after_acls = load_input(input_data)

    admin_client = AdminClient(admin_options)

    before_topics = Topic.create_from_cluster(admin_client)
    before_acls = ACL.create_from_cluster(admin_client)

    topics_sets = classify_topics(before_topics, after_topics)
    acls_sets = classify_acls(before_topics, after_topics, before_acls, after_acls)

    success = True

    if success:
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
