import argparse

from cli_utils import read_json_input


def handle_arguments():
    parser = argparse.ArgumentParser(
        description="Checks that there are no one-sided topics on an MRC cluster"
    )

    parser.add_argument("-c", "--config", help="Config properties for connecting to the cluster, in JSON format. "
                                               "Minimum = '{ \"bootstrap.servers\": \"<ip-or-dns-name>:9092\" }'")

    return parser.parse_args()


def main():
    args = handle_arguments()

    ####################################################################################################
    # default options
    ####################################################################################################
    admin_options = {'bootstrap.servers': '192.168.0.129:9092'}

    if args.connect_config:
        admin_options = read_json_input(args.config)
    ####################################################################################################


if __name__ == "__main__":
    main()
