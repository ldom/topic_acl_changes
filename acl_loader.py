from typing import Dict

from acl import ACL
from constants import Consts


def load_acls_from_cluster(admin_client) -> Dict[str, ACL]:
    pass


def load_acl_from_json(json_object) -> ACL:
    return ACL(
        name=json_object.get(Consts.A_NAME),
        principal=json_object.get(Consts.A_PRINCIPAL),
        type=json_object.get(Consts.A_TYPE),
        operation=json_object.get(Consts.A_OPERATION),
        allow=json_object.get(Consts.A_ALLOW),
    )
