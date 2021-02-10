from confluent_kafka.admin import ConfigResource, ConfigSource, NewTopic, RESOURCE_TOPIC, RESOURCE_BROKER
from confluent_kafka import KafkaException, KafkaError


def get_zookeeper_url(admin_client):
    fs = admin_client.describe_configs([ConfigResource(RESOURCE_BROKER, '0')])

    for res, f in fs.items():
        configs = f.result()
        zk_connect = configs['zookeeper.connect']
        return zk_connect.value

    return None
