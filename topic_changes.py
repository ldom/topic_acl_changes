from confluent_kafka.admin import ConfigResource, NewTopic, RESOURCE_TOPIC
from confluent_kafka import KafkaException, KafkaError

from cluster_info import get_zookeeper_url
from constants import Consts
from safe_delete import topic_safe_delete


class TopicChanges():
    def __init__(self, topics_to_create, topics_to_update, topics_to_delete,
                 admin_client, bootstrap_server_url, command_config, placements):
        self.topics_to_create = topics_to_create
        self.topics_to_update = topics_to_update
        self.topics_to_delete = topics_to_delete
        self.admin_client = admin_client
        self.bootstrap_server_url = bootstrap_server_url
        self.command_config = command_config
        self.placements = placements

        self.zookeeper_url = get_zookeeper_url(admin_client)

    def create_topics(self):
        for topic in self.topics_to_create:
            placement = self.placements[topic[Consts.T_PLACEMENT]]
            topic_config = {Consts.T_PLACEMENT_PROP: placement}
            topic_config.update(topic[Consts.T_CONFIG_PROPS])

            new_topic = [NewTopic(topic[Consts.T_NAME],
                                  num_partitions=topic[Consts.T_NB_PARTITIONS],
                                  config=topic_config)]

            fs = self.admin_client.create_topics([new_topic])
            for t, f in fs.items():
                try:
                    f.result()  # The result itself is None
                except KafkaException as e:
                    print(f"Error creating topic {t}: {e}.")

    def update_topics(self):
        for topic in self.topics_to_update:
            self.admin_client.alter_configs()
            resource = ConfigResource(RESOURCE_TOPIC, topic[Consts.T_NAME])
            resources = [resource]

            placement = self.placements[topic[Consts.T_PLACEMENT]]
            topic_config = {Consts.T_PLACEMENT_PROP: placement}
            topic_config.update(topic[Consts.T_CONFIG_PROPS])

            for k, v in topic_config.items():
                resource.set_config(k, v)

            fs = self.admin_client.alter_configs(resources)

            # Wait for operation to finish.
            for res, f in fs.items():
                try:
                    f.result()  # empty, but raises exception on failure
                    print("{} configuration successfully altered".format(res))
                except Exception:
                    raise

    def delete_topics(self):
        for topic in self.topics_to_delete:
            success, msg, _ = topic_safe_delete(self.admin_client, topic[Consts.T_NAME])
            if not success:
                print(msg)

    def apply_to_cluster(self):
        self.create_topics()
        self.update_topics()
        self.delete_topics()

    @staticmethod
    def topic_properties(topic_config_dict, is_for_kafka_configs=False):
        props = []
        if is_for_kafka_configs:
            for option_name, option_value in topic_config_dict.items():
                props.append(f"{option_name}={option_value}")

            return "--add-config " + ",".join(props)
        else:
            for option_name, option_value in topic_config_dict.items():
                props.append(f"--config {option_name}={option_value}")

            return " ".join(props)

    def apply_to_scripts(self):
        output = []

        for topic in self.topics_to_create:
            placement_option = f"--replica-placement {self.placements[topic.placement]}" if topic.placement else ""

            topic_props = self.topic_properties(topic.config_properties)
            command_config_option = f"--command-config {self.command_config}" if self.command_config else ""

            create_topic_cmd = f"kafka-topics --bootstrap-server {self.bootstrap_server_url} {command_config_option} " \
                               f"--alter --topic {topic.name} --partitions {topic.nb_partitions} " \
                               f"{placement_option} {topic_props}"

            output.append(create_topic_cmd)

        for topic in self.topics_to_update:
            placement_option = f"--replica-placement {self.placements[topic.placement]}" if topic.placement else ""

            topic_props = self.topic_properties(topic.config_properties, is_for_kafka_configs=True)
            command_config_option = f"--command-config {self.command_config}" if self.command_config else ""

            update_topic_cmd = f"kafka-configs --zookeeper {self.zookeeper_url} {command_config_option} " \
                               f"--alter --entity-type topics --entity-name {topic.name} " \
                               f"{placement_option} {topic_props}"

            # todo: deal with nb_partitions changes f"--partitions {topic.nb_partitions} " \

            output.append(update_topic_cmd)

        for topic in self.topics_to_delete:
            command_config_option = f"--command-config {self.command_config}" if self.command_config else ""

            delete_topic_cmd = f"kafka-topics --bootstrap-server {self.bootstrap_server_url} {command_config_option} " \
                               f"--delete --topic {topic.name}"

            output.append(delete_topic_cmd)

        return "\n\n".join(output)
