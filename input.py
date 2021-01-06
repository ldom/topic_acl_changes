from typing import List, Tuple

from acl import ACL
from acl_loader import load_acl_from_json
from constants import Consts
from topic import Topic
from topic_loader import load_topic_from_json


def load_input(json_objects_dict) -> Tuple[List[Topic], List[ACL]]:
    topics = []
    for t in json_objects_dict.get(Consts.TOPICS, []):
        topics.append(load_topic_from_json(t))

    acls = []
    for a in json_objects_dict.get(Consts.ACLS, []):
        acls.append(load_acl_from_json(a))

    return topics, acls
