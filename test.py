import json
import time
import unittest

from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException, KafkaError

from input import load_input
from topic_loader import load_topics_from_cluster
from acl_loader import load_acls_from_cluster

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
