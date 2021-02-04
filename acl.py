from acl_external import ExternalACL
from typing import Dict

from constants import Consts


class ACL:
    def __init__(self, name, principal, operation, type, allow):
        self.name = name
        self.principal = principal
        self.operation = operation
        self.type = type
        self.allow = allow
        self.signature = f"{self.name}/{self.principal}/{self.operation}/{self.type}/{self.allow}"

    @classmethod
    def create_from_cluster(cls, admin_client):
        # query using a script call and later the Admin API
        #acls_raw_output = ExternalACL.list_acls()

        # parse or load
        pass

    @classmethod
    def create_from_json(cls, json_object):
        return cls(
            name=json_object.get(Consts.A_NAME),
            principal=json_object.get(Consts.A_PRINCIPAL),
            type=json_object.get(Consts.A_TYPE),
            operation=json_object.get(Consts.A_OPERATION),
            allow=json_object.get(Consts.A_ALLOW),
        )
