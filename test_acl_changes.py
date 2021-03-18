import json
import unittest

from confluent_kafka.admin import AdminClient

from acl_changes import ACLChanges
from classify import classify_acls, classify_topics
from cli_utils import read_json_input
from constants import Consts
from input import load_analysis_input
from report import output_changes


class TestACLChanges(unittest.TestCase):
    def test_acl_scripts(self):
        """
                        {
                            "topic": "test_acl",
                            "partitions": 2,
                            "placement": "",
                            "config": {
                                "cleanup.policy": "delete",
                                "compression.type": "producer",
                                "retention.ms": -1
                            }
                        }
        """

        before_json = """
        {
            "topics": [
            ],
            "acls": [
                {
                    "name": "test_acl",
                    "principal": "xqdmgkfkusr001",
                    "resource_type": "TOPIC",
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
                    "topic": "test_acl",
                    "partitions": 2,
                    "placement": "",
                    "config": {
                        "cleanup.policy": "delete",
                        "compression.type": "producer",
                        "retention.ms": -1
                    }
                }
            ],
            "acls": [
                {
                    "name": "test_acl",
                    "principal": "xqdmgkfkusr001",
                    "resource_type": "TOPIC",
                    "operation": "READ",
                    "allow": true
                },
                {
                    "name": "test_acl",
                    "principal": "xqdspkfkusr002",
                    "resource_type": "TOPIC",
                    "operation": "WRITE",
                    "allow": true
                },
                {
                    "name": "test_acl",
                    "principal": "xqdmgkfkusr001AA",
                    "resource_type": "TOPIC",
                    "operation": "WRITE",
                    "allow": false
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

        admin_options = {'bootstrap.servers': 'localhost:9092'}
        admin_client = AdminClient(admin_options)

        acl_changes = ACLChanges(input_data[Consts.ACLS][Consts.ADDED],
                                 input_data[Consts.ACLS][Consts.REMOVED],
                                 admin_client,
                                 bootstrap_server_url=admin_options[Consts.CFG_BOOTSTRAP],
                                 command_config=None)

        scripts_to_run = acl_changes.apply_to_scripts()
        lines = scripts_to_run.split("\n")
        self.assertEqual(len(lines), 2)

        ret = acl_changes.apply_to_cluster()
        self.assertIsNotNone(ret)  # do better
