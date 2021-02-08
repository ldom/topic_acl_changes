import argparse

from confluent_kafka.admin import AdminClient

from cli_utils import read_json_input
from input import load_input


def handle_arguments():
    parser = argparse.ArgumentParser(
        description="Reads a JSON file with changes to apply (on topics and ACLs). Returns 0 for success, otherwise 1."
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

    if args.config:
        admin_options = read_json_input(args.connect_config)

    ####################################################################################################

    # read JSON input data
    input_data = read_json_input(args.input)
    after_topics, after_acls = load_input(input_data)

    admin_client = AdminClient(admin_options)

    # TODO

    exit(0)


if __name__ == "__main__":
    main()
