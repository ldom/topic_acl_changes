import json
import unittest

from confluent_kafka.admin import AdminClient

from classify import classify_acls, classify_topics
from cli_utils import read_json_input
from constants import Consts, ResultSet
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

        admin_options = {'bootstrap.servers': 'localhost:9092'}
        admin_client = AdminClient(admin_options)

        topic_changes = TopicChanges(input_data[Consts.TOPICS][Consts.ADDED],
                                     input_data[Consts.TOPICS][Consts.UPDATED],
                                     input_data[Consts.TOPICS][Consts.REMOVED],
                                     admin_client,
                                     bootstrap_server_url=admin_options[Consts.CFG_BOOTSTRAP],
                                     command_config=None,
                                     placements=None)

        ret = topic_changes.apply_to_scripts()
        self.assertIsNotNone(ret)  # do better

    def test_topic_dynamic_config_changes(self):
        before_json = """
        {
            "topics": [
                {
                    "topic": "Topic1",
                    "partitions": 120,
                    "placement": "async",
                    "config": {
                        "cleanup.policy": "delete",
                        "compression.type": "producer",
                        "retention.ms": -1,
                        "min.insync.replicas": 2
                    }
                },
                {
                    "topic": "Topic2",
                    "partitions": 120,
                    "placement": "async",
                    "config": {
                        "cleanup.policy": "delete",
                        "compression.type": "producer",
                        "retention.ms": 2592000000
                    }
                },
                {
                    "topic": "Topic3",
                    "partitions": 120,
                    "placement": "async",
                    "config": {
                        "cleanup.policy": "delete",
                        "compression.type": "producer",
                        "retention.ms": 2592000000,
                        "segment.bytes": 1897687
                    }
                },
                {
                    "topic": "Topic4",
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
            ]
        }
        """

        after_json = """
        {
            "topics": [
                {
                    "topic": "Topic1",
                    "partitions": 120,
                    "placement": "async",
                    "config": {
                        "cleanup.policy": "compact",
                        "compression.type": "producer",
                        "retention.ms": -1,
                        "max.message.bytes": 123456
                    }
                },
                {
                    "topic": "Topic2",
                    "partitions": 120,
                    "placement": "async",
                    "config": {
                        "cleanup.policy": "delete",
                        "compression.type": "producer",
                        "file.delete.delay.ms": "123456"
                    }
                },
                {
                    "topic": "Topic3",
                    "partitions": 120,
                    "placement": "async",
                    "config": {
                        "cleanup.policy": "delete",
                        "compression.type": "producer",
                        "retention.ms": 25920000,
                        "index.interval.bytes": 9000
                    }
                },
                {
                    "topic": "Topic4",
                    "partitions": 120,
                    "placement": "async",
                    "config": {
                        "cleanup.policy": "delete",
                        "retention.ms": 2592000000,
                        "index.interval.bytes": 9000,
                        "max.compaction.lag.ms": 45768
                    }
                }
            ],
            "acls": []
        }
        """

        before_data = json.loads(before_json)
        after_data = json.loads(after_json)

        before_topics, before_acls = load_analysis_input(before_data)
        after_topics, after_acls = load_analysis_input(after_data)

        topics_sets = classify_topics(before_topics, after_topics)

        self.assertIn('Topic1', topics_sets[ResultSet.TOPICS_MAX_BYTES_CHANGED])
        self.assertIn('Topic3', topics_sets[ResultSet.TOPICS_RETENTION_CHANGED])
        self.assertIn('Topic2', topics_sets[ResultSet.TOPICS_RETENTION_CHANGED])

        self.assertIn('Topic4', topics_sets[ResultSet.TOPICS_FINITE_RETENTION])
        self.assertIn('Topic3', topics_sets[ResultSet.TOPICS_FINITE_RETENTION])
        self.assertIn('Topic2', topics_sets[ResultSet.TOPICS_FINITE_RETENTION])

        self.assertIn('Topic1', topics_sets[ResultSet.TOPICS_UPDATED])
        self.assertIn('Topic3', topics_sets[ResultSet.TOPICS_UPDATED])
        self.assertIn('Topic4', topics_sets[ResultSet.TOPICS_UPDATED])
        self.assertIn('Topic2', topics_sets[ResultSet.TOPICS_UPDATED])

        self.assertIn('Topic1', topics_sets['Topic(s) with added max.message.bytes'])
        self.assertIn('Topic1', topics_sets['Topic(s) with changed cleanup.policy'])
        self.assertIn('Topic1', topics_sets['Topic(s) with removed min.insync.replicas'])
        self.assertIn('Topic3', topics_sets['Topic(s) with added index.interval.bytes'])
        self.assertIn('Topic4', topics_sets['Topic(s) with added index.interval.bytes'])
        self.assertIn('Topic3', topics_sets['Topic(s) with changed retention.ms'])
        self.assertIn('Topic3', topics_sets['Topic(s) with removed segment.bytes'])
        self.assertIn('Topic4', topics_sets['Topic(s) with added max.compaction.lag.ms'])
        self.assertIn('Topic4', topics_sets['Topic(s) with removed compression.type'])
        self.assertIn('Topic2', topics_sets['Topic(s) with added file.delete.delay.ms'])
        self.assertIn('Topic2', topics_sets['Topic(s) with removed retention.ms'])
