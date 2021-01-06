from acl import ACL
from constants import Consts


def load_acl_from_cluster(admin_client):
    pass


def load_acl_from_json(json_object):
    return ACL(
        name=json_object.get(Consts.A_NAME),
        principal=json_object.get(Consts.A_PRINCIPAL),
        type=json_object.get(Consts.A_TYPE),
        operation=json_object.get(Consts.A_OPERATION),
        allow=json_object.get(Consts.A_ALLOW),
    )
