from typing import Dict, Tuple

from acl import ACL
from acl_loader import load_acl_from_json
from constants import Consts
from topic import Topic
from topic_loader import load_topic_from_json


def load_input(json_objects_dict) -> Tuple[Dict[str, Topic], Dict[str, ACL]]:
    topics = {}
    for t in json_objects_dict.get(Consts.TOPICS, []):
        topic = load_topic_from_json(t)
        topics[topic.name] = topic

    acls = {}
    for a in json_objects_dict.get(Consts.ACLS, []):
        acl = load_acl_from_json(a)
        acls[acl.signature] = acl

    return topics, acls
