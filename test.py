import json
import time
import unittest

from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException, KafkaError

from input import load_input
from topic_loader import load_topics_from_cluster
from acl_loader import load_acls_from_cluster
from classify import classify_acls, classify_mixed, classify_topics

class TestLib(unittest.TestCase):
    admin_options = {'bootstrap.servers': '127.0.0.1:9092'}

    def test_load_from_cluster(self):
        admin_client = AdminClient(self.admin_options)
        existing_topics = load_topics_from_cluster(admin_client)
        # existing_acls = load_acls_from_cluster(admin_client)

        self.assertTrue(True)

    def test_load(self):
        input_json = """
{
    "topics": [
        {
            "topic": "BIAN.Account",
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
        }
    ]
}
        """

        input_data = json.loads(input_json)

        topics, acls = load_input(input_data)

        self.assertEqual(len(topics), 2)
        self.assertEqual(len(acls), 2)

    def test_classify(self):
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

        before_topics, before_acls = load_input(before_data)
        after_topics, after_acls = load_input(after_data)

        topics_sets = classify_topics(before_topics, after_topics)
        acls_sets = classify_acls(before_acls, after_acls)
        mixed_sets = classify_mixed(before_topics, after_topics, before_acls, after_acls)

        self.assertEqual(len(topics_sets), 1)
