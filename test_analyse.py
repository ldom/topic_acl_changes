import json
import time
import unittest

from confluent_kafka.admin import AdminClient

from acl import ACL
from classify import classify_acls, classify_topics, has_old_style_upn_principal, has_old_style_cn_principal
from constants import ResultSet
from input import load_analysis_input
from report import output_changes
from topic import Topic


class TestLib(unittest.TestCase):
    admin_options = {'bootstrap.servers': 'localhost:9092'}

    def test_load_from_cluster(self):
        placements = {
            "simple": {
                "version": 1,
                "replicas": [{"count": 1, "constraints": {"rack": "gf1"}}]
            }
        }
        Topic.normalize_placements(placements)

        admin_client = AdminClient(self.admin_options)
        _ = Topic.create_from_cluster(admin_client, placements)
        _ = ACL.create_from_cluster(admin_client, self.admin_options['bootstrap.servers'], None)
        self.assertTrue(True)  # do better

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
            "resource_type": "TOPIC",
            "operation": "READ",
            "allow": true
        },
        {
            "name": "BIAN.Account",
            "principal": "xqdspkfkusr002",
            "resource_type": "TOPIC",
            "operation": "READ",
            "allow": true
        }
    ]
}
        """

        input_data = json.loads(input_json)

        topics, acls = load_analysis_input(input_data)

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
                    "resource_type": "TOPIC",
                    "operation": "READ",
                    "allow": true,
                    "pattern_type": "LITERAL"
                },
                {
                    "name": "BIAN.Account",
                    "principal": "xqdspkfkusr002",
                    "resource_type": "TOPIC",
                    "operation": "READ",
                    "allow": true,
                    "pattern_type": "LITERAL"
                },
                {
                    "name": "BIAN.Account",
                    "principal": "xqdmgkfkusr001AA",
                    "resource_type": "TOPIC",
                    "operation": "WRITE",
                    "allow": true,
                    "pattern_type": "LITERAL"
                },
                {
                    "name": "BIAN.Account.1",
                    "principal": "xqdspkfkusr002BB",
                    "resource_type": "TOPIC",
                    "operation": "READ",
                    "allow": true,
                    "pattern_type": "LITERAL"
                },
                {
                    "name": "BIAN.Account.2",
                    "principal": "xqdmgkfkusr001CC",
                    "resource_type": "TOPIC",
                    "operation": "WRITE",
                    "allow": true,
                    "pattern_type": "LITERAL"
                },
                {
                    "name": "BIAN.Account",
                    "principal": "xqdspkfkusr002DD",
                    "resource_type": "TOPIC",
                    "operation": "READ",
                    "allow": true,
                    "pattern_type": "LITERAL"
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
                    "resource_type": "TOPIC",
                    "operation": "READ",
                    "allow": true, 
                    "pattern_type": "LITERAL"
                },
                {
                    "name": "BIAN.Account",
                    "principal": "xqdspkfkusr002",
                    "resource_type": "TOPIC",
                    "operation": "READ",
                    "allow": false,
                    "pattern_type": "LITERAL"
                },
                {
                    "name": "BIAN.Account",
                    "principal": "xqdspkfkusr002BB",
                    "resource_type": "TOPIC",
                    "operation": "READ",
                    "allow": true,
                    "pattern_type": "LITERAL"
                },
                {
                    "name": "BIAN.Account",
                    "principal": "xqdmgkfkusr001CC",
                    "resource_type": "TOPIC",
                    "operation": "WRITE",
                    "allow": true,
                    "pattern_type": "LITERAL"
                },
                {
                    "name": "BIAN.Account.1",
                    "principal": "xqdspkfkusr002DD",
                    "resource_type": "TOPIC",
                    "operation": "READ",
                    "allow": true,
                    "pattern_type": "LITERAL"
                },
                {
                    "name": "BIAN.Account.1",
                    "principal": "xqdspkfkusr002BBXX",
                    "resource_type": "TOPIC",
                    "operation": "WRITE",
                    "allow": true,
                    "pattern_type": "LITERAL"
                },
                {
                    "name": "BIAN.Account.2",
                    "principal": "xqdmgkfkusr001CCYY",
                    "resource_type": "TOPIC",
                    "operation": "WRITE",
                    "allow": true,
                    "pattern_type": "LITERAL"
                },
                {
                    "name": "BIAN.Account",
                    "principal": "xqdspkfkusr002DDZZ",
                    "resource_type": "TOPIC",
                    "operation": "READ",
                    "allow": true,
                    "pattern_type": "LITERAL"
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

        self.assertEqual(len(topics_sets[ResultSet.TOPICS_ADDED]), 1)
        self.assertEqual(len(topics_sets[ResultSet.TOPICS_REMOVED]), 1)
        self.assertEqual(len(topics_sets[ResultSet.TOPICS_PARTITION_CHANGED]), 1)
        self.assertEqual(len(topics_sets[ResultSet.TOPICS_MAX_BYTES_CHANGED]), 1)
        self.assertEqual(len(topics_sets[ResultSet.TOPICS_RETENTION_CHANGED]), 1)
        self.assertEqual(len(topics_sets[ResultSet.TOPICS_FINITE_RETENTION]), 3)

        self.assertEqual(len(topics_sets[ResultSet.ACLS_ADDED]), 7)
        self.assertEqual(len(topics_sets[ResultSet.ACLS_REMOVED]), 5)
        self.assertEqual(len(topics_sets[ResultSet.ACLS_ADDED_TO_ADDED_TOPICS]), 0)
        self.assertEqual(len(topics_sets[ResultSet.ACLS_ADDED_TO_EXISTING_TOPICS]), 7)
        self.assertEqual(len(topics_sets[ResultSet.ACLS_REMOVED_FROM_EXISTING_TOPICS]), 5)

        self.assertEqual(len(topics_sets[ResultSet.TOPICS_NO_ACCESS_BEFORE]), 1)
        self.assertEqual(len(topics_sets[ResultSet.TOPICS_NO_ACCESS_AFTER]), 1)
        self.assertEqual(len(topics_sets[ResultSet.TOPICS_RO_BEFORE]), 1)
        self.assertEqual(len(topics_sets[ResultSet.TOPICS_RO_AFTER]), 0)
        self.assertEqual(len(topics_sets[ResultSet.TOPICS_WO_BEFORE]), 1)
        self.assertEqual(len(topics_sets[ResultSet.TOPICS_WO_AFTER]), 1)

        self.assertEqual(len(topics_sets[ResultSet.PRINCIPALS_ADDED]), 3)
        self.assertEqual(len(topics_sets[ResultSet.PRINCIPALS_AFTER]), 8)
        self.assertEqual(len(topics_sets[ResultSet.PRINCIPALS_REMOVED]), 1)
        self.assertEqual(len(topics_sets[ResultSet.PRINCIPALS_USING_OLD_CN]), 0)

        changes = output_changes(topics_sets, before_topics, before_acls, after_topics, after_acls)
        self.assertEqual(len(changes['topics']['added']), len(topics_sets[ResultSet.TOPICS_ADDED]))
        self.assertEqual(len(changes['topics']['removed']), len(topics_sets[ResultSet.TOPICS_REMOVED]))
        self.assertEqual(len(changes['topics']['updated']), len(topics_sets[ResultSet.TOPICS_UPDATED]))

        self.assertEqual(len(changes['acls']['added']), len(topics_sets[ResultSet.ACLS_ADDED]))
        self.assertEqual(len(changes['acls']['removed']), len(topics_sets[ResultSet.ACLS_REMOVED]))

        def dumper(obj):
            try:
                return obj.toJSON()
            except:
                return obj.__dict__

        with open("changes.json", 'w') as f:
            f.write(json.dumps(changes, default=dumper, indent=2))

    def test_principal_style(self):
        old_style_upn = "xqdmgkfkusr10"
        old_style_cn = "xqd-mg-kfkusr100"

        ok_style = "xqdmgkfkusr001"

        self.assertFalse(has_old_style_upn_principal(ok_style))
        self.assertTrue(has_old_style_upn_principal(old_style_upn))

        self.assertFalse(has_old_style_cn_principal(ok_style))

        ret = has_old_style_cn_principal(old_style_cn)
        self.assertTrue(ret)
