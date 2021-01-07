from collections import namedtuple
from distutils.util import strtobool
import time
from typing import Dict, Optional

from confluent_kafka.admin import ConfigResource, RESOURCE_TOPIC
from confluent_kafka import KafkaException

from constants import Consts
from topic import Topic


TopicInfo = namedtuple('TopicInfo', ["full_config",
                                     "non_default_config",
                                     "replication_factor",
                                     "partitions"])


def gather_topic_info(admin_client, topic_name) -> Optional[TopicInfo]:  # returns None if the topic does not exist
    fs = admin_client.describe_configs([ConfigResource(RESOURCE_TOPIC, topic_name)])

    topic_config = {}
    topic_non_default_config = {}

    for res, f in fs.items():
        try:
            configs = f.result()
            for config in iter(configs.values()):
                topic_config[config.name] = config.value
                if not config.is_default:
                    topic_non_default_config[config.name] = config.value
                # print_config(config, 1)

        except KafkaException as e:
            # print("Failed to describe {}: {}".format(res, e))
            return None
        except Exception:
            raise

    topic_data = admin_client.list_topics(topic_name)
    topic_partitions = topic_data.topics[topic_name].partitions

    replication_factor = len(topic_partitions.get(0).replicas)

    return TopicInfo(full_config=topic_config, non_default_config=topic_non_default_config,
                     partitions=topic_partitions,
                     replication_factor=replication_factor)



def load_topics_from_cluster(admin_client) -> Dict[str, Topic]:
    topics = {}
    all_topics = admin_client.list_topics()
    for topic_name, topic_data in all_topics.topics.items():
        nb_partitions = len(topic_data.partitions)

        topic_info = gather_topic_info(admin_client, topic_name)

        topics[topic_name] = Topic(
            name=topic_name,
            nb_partitions=nb_partitions,
            placement="",
            config_properties=topic_info.full_config,
        )
    return topics


def load_topic_from_json(json_object) -> Topic:
    return Topic(
        name=json_object.get(Consts.T_TOPIC),
        nb_partitions=json_object.get(Consts.T_PARTITIONS),
        placement=json_object.get(Consts.T_PLACEMENT),
        config_properties=json_object.get(Consts.T_CONFIG),
    )
