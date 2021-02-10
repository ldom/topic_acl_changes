import json
import unittest

from confluent_kafka.admin import AdminClient

from classify import classify_acls, classify_topics
from cli_utils import read_json_input
from constants import Consts
from input import load_analysis_input
from report import output_changes
from topic_changes import TopicChanges


class TestTopicChanges(unittest.TestCase):
    def test_topic_topic_properties(self):
        ret = TopicChanges.topic_properties({
            'compression.type': 'snappy',
            'max.message.bytes': '10000'
        }, is_for_kafka_configs=False)
        self.assertEqual(ret, "--config compression.type=snappy --config max.message.bytes=10000")

        ret = TopicChanges.topic_properties({
            'max.message.bytes': '10000',
            'retention.ms': '897698769'
        }, is_for_kafka_configs=True)
        self.assertEqual(ret, "--add-config max.message.bytes=10000,retention.ms=897698769")

    def test_topic_script(self):
        before_json = """
        {
            "topics": [
                {
                    "topic": "BIAN.Account",
                    "partitions": 120,
                    "placement": "async",
                    "config": {
                        "cleanup.policy": "delete",
                        "compression.type": "producer",
                        "retention.ms": -1
                    }
                },
                {
                    "topic": "BIAN.Account.1",
                    "partitions": 120,
                    "placement": "async",
                    "config": {
                        "cleanup.policy": "delete",
                        "compression.type": "producer",
                        "retention.ms": 2592000000
                    }
                },
                {
                    "topic": "BIAN.Account.2",
                    "partitions": 120,
                    "placement": "async",
                    "config": {
                        "cleanup.policy": "delete",
                        "compression.type": "producer",
                        "retention.ms": 2592000000
                    }
                },
                {
                    "topic": "BIAN.Account.AccountModality",
                    "partitions": 120,
                    "placement": "async",
                    "config": {
                        "cleanup.policy": "delete",
                        "compression.type": "producer",
                        "retention.ms": 2592000000
                    }
                }
            ],
            "acls": [
                {
                    "name": "BIAN.Account",
                    "principal": "xqdmgkfkusr001",
                    "type": "TOPIC",
                    "operation": "READ",
                    "allow": true
                },
                {
                    "name": "BIAN.Account",
                    "principal": "xqdspkfkusr002",
                    "type": "TOPIC",
                    "operation": "READ",
                    "allow": true
                },
                {
                    "name": "BIAN.Account",
                    "principal": "xqdmgkfkusr001AA",
                    "type": "TOPIC",
                    "operation": "WRITE",
                    "allow": true
                },
                {
                    "name": "BIAN.Account.1",
                    "principal": "xqdspkfkusr002BB",
                    "type": "TOPIC",
                    "operation": "READ",
                    "allow": true
                },
                {
                    "name": "BIAN.Account.2",
                    "principal": "xqdmgkfkusr001CC",
                    "type": "TOPIC",
                    "operation": "WRITE",
                    "allow": true
                },
                {
                    "name": "BIAN.Account",
                    "principal": "xqdspkfkusr002DD",
                    "type": "TOPIC",
                    "operation": "READ",
                    "allow": true
                }
            ]
        }
        """

        after_json = """
        {
            "topics": [
                {
                    "topic": "BIAN.Account",
                    "partitions": 120,
                    "placement": "async",
                    "config": {
                        "cleanup.policy": "delete",
                        "compression.type": "producer",
                        "retention.ms": -1
                    }
                },
                {
                    "topic": "BIAN.Account.1",
                    "partitions": 60,
                    "placement": "async",
                    "config": {
                        "cleanup.policy": "delete",
                        "compression.type": "producer",
                        "retention.ms": 2592000000,
                        "max.message.bytes": 123456
                    }
                },
                {
                    "topic": "BIAN.Account.2",
                    "partitions": 120,
                    "placement": "async",
                    "config": {
                        "cleanup.policy": "delete",
                        "compression.type": "producer",
                        "retention.ms": 122000
                    }
                },
                {
                    "topic": "BIAN.NEW",
                    "partitions": 120,
                    "placement": "async",
                    "config": {
                        "cleanup.policy": "delete",
                        "compression.type": "producer",
                        "retention.ms": 2592000000
                    }
                }
            ],
            "acls": [
                {
                    "name": "BIAN.Account",
                    "principal": "xqdmgkfkusr001",
                    "type": "TOPIC",
                    "operation": "READ",
                    "allow": true
                },
                {
                    "name": "BIAN.Account",
                    "principal": "xqdspkfkusr002",
                    "type": "TOPIC",
                    "operation": "READ",
                    "allow": false
                },
                {
                    "name": "BIAN.Account",
                    "principal": "xqdspkfkusr002BB",
                    "type": "TOPIC",
                    "operation": "READ",
                    "allow": true
                },
                {
                    "name": "BIAN.Account",
                    "principal": "xqdmgkfkusr001CC",
                    "type": "TOPIC",
                    "operation": "WRITE",
                    "allow": true
                },
                {
                    "name": "BIAN.Account.1",
                    "principal": "xqdspkfkusr002DD",
                    "type": "TOPIC",
                    "operation": "READ",
                    "allow": true
                },
                {
                    "name": "BIAN.Account.1",
                    "principal": "xqdspkfkusr002BBXX",
                    "type": "TOPIC",
                    "operation": "WRITE",
                    "allow": true
                },
                {
                    "name": "BIAN.Account.2",
                    "principal": "xqdmgkfkusr001CCYY",
                    "type": "TOPIC",
                    "operation": "WRITE",
                    "allow": true
                },
                {
                    "name": "BIAN.Account",
                    "principal": "xqdspkfkusr002DDZZ",
                    "type": "TOPIC",
                    "operation": "READ",
                    "allow": true
                }
            ]
        }
        """
        before_data = json.loads(before_json)
        after_data = json.loads(after_json)

        before_topics, before_acls = load_analysis_input(before_data)
        after_topics, after_acls = load_analysis_input(after_data)

        topics_sets = classify_topics(before_topics, after_topics)
        mixed_sets = classify_acls(before_topics, after_topics, before_acls, after_acls)
        topics_sets.update(mixed_sets)

        changes = output_changes(topics_sets, before_topics, before_acls, after_topics, after_acls)

        def dumper(obj):
            try:
                return obj.toJSON()
            except:
                return obj.__dict__

        temp_file = "temp.json"

        with open(temp_file, 'w') as f:
            f.write(json.dumps(changes, default=dumper, indent=2))

        input_data = read_json_input(temp_file)

        placements = read_json_input("placements.json")

        admin_options = {'bootstrap.servers': 'localhost:9092'}

        admin_client = AdminClient(admin_options)

        topic_changes = TopicChanges(input_data[Consts.TOPICS][Consts.ADDED],
                                     input_data[Consts.TOPICS][Consts.UPDATED],
                                     input_data[Consts.TOPICS][Consts.REMOVED],
                                     admin_client,
                                     bootstrap_server_url=admin_options[Consts.CFG_BOOTSTRAP],
                                     command_config=None,
                                     placements=placements)

        ret = topic_changes.apply_to_scripts()

        truc = 1