from typing import Dict, Tuple

from acl import ACL
from acl_external import ExternalACL
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


def get_principal(full_principal):
    items = full_principal.split(':')
    if len(items) == 2:
        return items[1]
    return full_principal


# for this app, allow is true or false
def get_allow(acl):
    if acl[ExternalACL.C_ACL_PERMISSION_TYPE] == ExternalACL.PERM_ALLOW:
        return True
    return False


def load_from_kafka_acl_output(output):
    acls = {}
    for resource in ExternalACL.parse_acl_output(output):
        for acl_details in resource[ExternalACL.C_ACLS]:
            new_acl = ACL(
                name=resource[ExternalACL.C_RES_NAME],
                principal=get_principal(acl_details[ExternalACL.C_ACL_PRINCIPAL]),
                operation=acl_details[ExternalACL.C_ACL_OPERATION],
                # for this app, type is the type of resource, either TOPIC or GROUP
                type=resource[ExternalACL.C_RES_TYPE],
                allow=get_allow(acl_details),
            )
            acls[new_acl.signature] = new_acl

    return acls
