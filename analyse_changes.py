import argparse
import json

from confluent_kafka.admin import AdminClient

from acl import ACL
from classify import classify_acls, classify_topics
from cli_utils import read_json_input
from input import load_input
from report import output_changes, output_report
from topic import Topic


def handle_arguments():
    parser = argparse.ArgumentParser(
        description="Compare the desired state (from a JSON file) against an existing cluster. Produces a readable "
                    "output as well as a JSON file to be used by the apply_changes tool. Returns 0 for success, "
                    "otherwise 1. "
    )

    parser.add_argument("input", help="JSON input file")
    parser.add_argument("output", help="JSON output file (can be used by apply_changes tool")

    parser.add_argument("--connect-config",
                        help="Config properties for connecting to the cluster, in JSON format. "
                             "Minimum = '{ \"bootstrap.servers\": \"<ip-or-dns-name>:9092\" }'")

    parser.add_argument("--command-config",
                        help="Config properties for connecting to the cluster, in JSON format. "
                             "Minimum = '{ \"bootstrap.servers\": \"<ip-or-dns-name>:9092\" }'",
                        default=None)

    return parser.parse_args()


def main():
    # get the command line arguments
    args = handle_arguments()

    ####################################################################################################
    # default options
    ####################################################################################################
    admin_options = {'bootstrap.servers': '192.168.0.129:9092'}

    if args.connect_config:
        admin_options = read_json_input(args.connect_config)

    ####################################################################################################

    # read JSON input data
    input_data = read_json_input(args.input)
    after_topics, after_acls = load_input(input_data)

    admin_client = AdminClient(admin_options)

    before_topics = Topic.create_from_cluster(admin_client)
    before_acls = ACL.create_from_cluster(admin_client, admin_options['bootstrap.servers'], args.comand_config)

    topics_sets = classify_topics(before_topics, after_topics)
    acls_sets = classify_acls(before_topics, after_topics, before_acls, after_acls)
    topics_sets.update(acls_sets)

    output_report(topics_sets)
    changes = output_changes(topics_sets, before_topics, before_acls, after_topics, after_acls)
    json_text = json.dumps(changes)
    with open(args.output, 'w') as data_file:
        data_file.write(json_text)

    exit(0)


if __name__ == "__main__":
    main()
