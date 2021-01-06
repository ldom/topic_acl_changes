from constants import Consts
from topic import Topic


def load_topic_from_cluster(admin_client):
    pass


def load_topic_from_json(json_object):
    return Topic(
        name=json_object.get(Consts.T_TOPIC),
        nb_partitions=json_object.get(Consts.T_PARTITIONS),
        placement=json_object.get(Consts.T_PLACEMENT),
        config_properties=json_object.get(Consts.T_CONFIG),
    )
