import argparse

from confluent_kafka.admin import AdminClient

from acl_changes import ACLChanges
from constants import Consts
from cli_utils import read_json_input
from topic_changes import TopicChanges


def handle_arguments():
    parser = argparse.ArgumentParser(
        description="Reads a JSON file with changes to apply (on topics and ACLs). Returns 0 for success, otherwise 1."
    )

    parser.add_argument("input", help="JSON input file")

    grp = parser.add_mutually_exclusive_group()
    grp.add_argument("--to-scripts",
                     action='store_true',
                     help="Outputs Kafka CLI script commands ready to be executed.")
    grp.add_argument("--to-cluster",
                     action='store_true',
                     help="Executes changes on the cluster.",
                     default=True
                     )

    parser.add_argument("--connect-config",
                        help="Config properties for connecting to the cluster, in JSON format. "
                             "Minimum = '{ \"bootstrap.servers\": \"<ip-or-dns-name>:9092\" }'")

    parser.add_argument("--placements",
                        help="File with placement constraints, in JSON format. "
                             "For example: '{ \"async\": { \"sync\": { \"version\": 1, "
                             "\"replicas\": [{\"count\": 2, \"constraints\": {\"rack\": \"gf2\"}}, "
                             "{\"count\": 2, \"constraints\": {\"rack\": \"gf1\"}}] } } }'")

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
    admin_options = {Consts.CFG_BOOTSTRAP: '192.168.0.129:9092'}
    placements = None

    if args.connect_config:
        admin_options = read_json_input(args.connect_config)
    if args.placements:
        placements = read_json_input(args.placements)

    ####################################################################################################

    # read JSON input data
    input_data = read_json_input(args.input)

    admin_client = AdminClient(admin_options)

    topic_changes = TopicChanges(input_data[Consts.TOPICS][Consts.ADDED],
                                 input_data[Consts.TOPICS][Consts.UPDATED],
                                 input_data[Consts.TOPICS][Consts.REMOVED],
                                 admin_client,
                                 bootstrap_server_url=admin_options[Consts.CFG_BOOTSTRAP],
                                 command_config=args.command_config,
                                 placements=placements)

    acl_changes = ACLChanges(input_data[Consts.ACLS][Consts.ADDED],
                             input_data[Consts.ACLS][Consts.REMOVED],
                             admin_client,
                             bootstrap_server_url=admin_options[Consts.CFG_BOOTSTRAP],
                             command_config=args.command_config)

    if args.to_scripts:
        print(topic_changes.apply_to_scripts())
        print(acl_changes.apply_to_scripts())
    else:
        topic_changes.apply_to_cluster()
        acl_changes.apply_to_cluster()

    exit(0)


if __name__ == "__main__":
    main()
