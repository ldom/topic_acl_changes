import argparse
import json

from confluent_kafka.admin import AdminClient

from acl import ACL
from classify import classify_acls, classify_topics
from cli_utils import read_json_input
from constants import Consts
from input import load_analysis_input
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
                        help="Command Config file passed to the CLI tools. ",
                        default=None)

    parser.add_argument("--placements",
                        help="File with placement constraints, in JSON format. "
                             "For example: '{ \"sync\": { \"version\": 1, "
                             "\"replicas\": [{\"count\": 2, \"constraints\": {\"rack\": \"gf2\"}}, "
                             "{\"count\": 2, \"constraints\": {\"rack\": \"gf1\"}}] } }'")

    return parser.parse_args()

def main():
    # get the command line arguments
    args = handle_arguments()

    ####################################################################################################
    # default options
    ####################################################################################################
    admin_options = {'bootstrap.servers': '192.168.0.129:9092'}
    placements = None

    if args.connect_config:
        admin_options = read_json_input(args.connect_config)
    if args.placements:
        placements = read_json_input(args.placements)
        Topic.normalize_placements(placements)

    ####################################################################################################

    # read JSON input data
    input_data = read_json_input(args.input)
    after_topics, after_acls = load_analysis_input(input_data)

    admin_client = AdminClient(admin_options)

    before_topics = Topic.create_from_cluster(admin_client, placements)
    before_acls = ACL.create_from_cluster(admin_client, admin_options['bootstrap.servers'], args.comand_config)

    topics_sets = classify_topics(before_topics, after_topics)
    acls_sets = classify_acls(before_topics, after_topics, before_acls, after_acls)
    topics_sets.update(acls_sets)

    output_report(topics_sets)
    changes = output_changes(topics_sets, before_topics, before_acls, after_topics, after_acls)

    def dumper(obj):
        try:
            return obj.toJSON()
        except:
            return obj.__dict__

    with open(args.output, 'w') as f:
        f.write(json.dumps(changes, default=dumper, indent=2))

    exit(0)


if __name__ == "__main__":
    main()
