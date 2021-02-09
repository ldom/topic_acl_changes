from confluent_kafka.admin import ConfigResource, ConfigSource, NewTopic, RESOURCE_TOPIC, RESOURCE_BROKER
from confluent_kafka import KafkaException, KafkaError

from constants import Consts
from safe_delete import topic_create


class TopicChanges():
    def __init__(self, topics_to_create, topics_to_update, topics_to_delete):
        self.topics_to_create = topics_to_create
        self.topics_to_update = topics_to_update
        self.topics_to_delete = topics_to_delete

    def create_topics(self, admin_client, placements):
        for topic in self.topics_to_create:
            placement = placements[topic[Consts.T_PLACEMENT]]
            topic_config = {Consts.T_PLACEMENT_PROP: placement}
            topic_config.update(topic[Consts.T_CONFIG_PROPS])

            new_topic = [NewTopic(topic[Consts.T_NAME],
                                  num_partitions=topic[Consts.T_NB_PARTITIONS],
                                  config=topic_config)]

            fs = admin_client.create_topics([new_topic])
            for t, f in fs.items():
                try:
                    f.result()  # The result itself is None
                except KafkaException as e:
                    print(f"Error creating topic {t}: {e}.")

    def apply_to_cluster(self, admin_client, connect_config, command_config, placements):
        self.create_topics(admin_client, placements)

    def apply_to_scripts(self, connect_config, command_config, placements):
        pass
