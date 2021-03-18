import argparse

from confluent_kafka.admin import AdminClient

from cli_utils import read_json_input
from safe_delete import topics_safe_delete, topics_recreate
from topic_storage import get_latest_applied, set_latest_applied


UID_TOPIC_NAME = "uids"
READ_TIMEOUT = 2.0

"""
example input JSON
{
    'version': 17,
    'environment': 'RND',
    'recreates': [
        'aaa',
        'bbb'
    ]
}
"""

JSON_INPUT_UID = "version"
JSON_INPUT_ENV = "environment"
JSON_INPUT_RECREATE_TOPICS = "recreates"


def handle_arguments():
    parser = argparse.ArgumentParser(
        description="Reads a JSON file with topics to re-create. Returns 0 for success, otherwise 1. "
    )

    parser.add_argument("actions",
                        help="JSON input file to specify what to do.")

    parser.add_argument("cluster-config",
                        help="JSON input file with cluster bootstrap-servers, etc.")

    # parser.add_argument("-c", "--config", help="Config properties for connecting to the cluster, in JSON format. "
    #                                            "Minimum = '{ \"bootstrap.servers\": \"<ip-or-dns-name>:9092\" }'", 
    #                                            required=True)

    return parser.parse_args()


def main():
    # get the command line arguments
    args = handle_arguments()

    ####################################################################################################
    # client options
    ####################################################################################################
    # admin_options = read_json_input(args.config)
    admin_options = read_json_input("config.json")

    consumer_options = admin_options.copy()
    consumer_options.update({'group.id': 'safe_delete'})

    producer_options = admin_options
    ####################################################################################################

    # read JSON input data
    actions = read_json_input(args.actions)
    print(actions)

    cluster_config = read_json_input(args.cluster_config)
    print(cluster_config)
    
    raise RuntimeError('delete this stuff')

    # read uid from topic
    latest_applied_uid = get_latest_applied(consumer_options, UID_TOPIC_NAME, READ_TIMEOUT)

    # if not the first time, we check that we haven't applied this one yet
    if latest_applied_uid:
        if int(actions[JSON_INPUT_UID]) <= int(latest_applied_uid):
            print("Already done!")
            return False  # we do nothing if it's been applied already

    # TODO test the env (how to get the current env?)
    # required env received in --> actions[JSON_INPUT_ENV]

    # apply the actions
    a = AdminClient(admin_options)
    success, results = topics_recreate(a, actions[JSON_INPUT_RECREATE_TOPICS])

    print(results)

    # write uid in topic
    set_latest_applied(producer_options, UID_TOPIC_NAME, str(actions['uid']))

    if success:
        return True
    else:
        return False


if __name__ == "__main__":
    main()
