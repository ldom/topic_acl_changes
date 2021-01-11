from typing import Dict, Tuple

from acl import ACL
from constants import Consts
from topic import Topic


def load_input(json_objects_dict) -> Tuple[Dict[str, Topic], Dict[str, ACL]]:
    topics = {}
    for t in json_objects_dict.get(Consts.TOPICS, []):
        topic = Topic.create_from_json(t)
        topics[topic.name] = topic

    acls = {}
    for a in json_objects_dict.get(Consts.ACLS, []):
        acl = ACL.create_from_json(a)
        acls[acl.signature] = acl

    return topics, acls
