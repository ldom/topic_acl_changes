from constants import Consts


class ACL:
    def __init__(self, name, principal, operation, resource_type, allow, pattern_type=Consts.A_PATTERN_TYPE_LITERAL):
        self.name = name
        self.principal = principal
        self.operation = operation
        self.resource_type = resource_type
        self.pattern_type = pattern_type
        self.allow = allow
        self.signature = f"{self.name}/{self.principal}/{self.operation}/{self.resource_type}/" \
                         f"{self.allow}/{self.pattern_type}"

    @staticmethod
    def get_principal(full_principal):
        items = full_principal.split(':')
        if len(items) == 2:
            return items[1]
        return full_principal

    @staticmethod
    # for this app, allow is true or false
    def get_allow(acl):
        from acl_external import ExternalACL
        if acl[ExternalACL.C_ACL_PERMISSION_TYPE] == ExternalACL.PERM_ALLOW:
            return True
        return False

    @classmethod
    def load_from_kafka_acl_output(cls, output):
        from acl_external import ExternalACL
        acls = {}
        for resource in ExternalACL.parse_acl_output(output):
            for acl_details in resource[ExternalACL.C_ACLS]:
                new_acl = ACL(
                    name=resource[ExternalACL.C_RES_NAME],
                    principal=cls.get_principal(acl_details[ExternalACL.C_ACL_PRINCIPAL]),
                    operation=acl_details[ExternalACL.C_ACL_OPERATION],
                    # for this app, type is the type of resource, either TOPIC or GROUP
                    resource_type=resource[ExternalACL.C_RES_TYPE],
                    pattern_type=resource[ExternalACL.C_PATTERN_TYPE],
                    allow=cls.get_allow(acl_details),
                )
                acls[new_acl.signature] = new_acl

        return acls

    @classmethod
    def create_from_cluster(cls, admin_client, bootstrap_servers, command_config):
        from acl_external import ExternalACL
        list_output = ExternalACL.list_acls(bootstrap_servers, command_config)
        return cls.load_from_kafka_acl_output(list_output)

    @classmethod
    def create_from_json(cls, json_object):
        return cls(
            name=json_object.get(Consts.A_NAME),
            principal=json_object.get(Consts.A_PRINCIPAL),
            resource_type=json_object.get(Consts.A_RESOURCE_TYPE),
            pattern_type=json_object.get(Consts.A_PATTERN_TYPE),
            operation=json_object.get(Consts.A_OPERATION),
            allow=json_object.get(Consts.A_ALLOW),
        )
