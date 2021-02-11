import subprocess
from typing import Dict, List


class ExternalACL():
    TIMESTAMP_START = "["
    MAIN_START = "Current ACLs for resource"
    RESOURCE_PATTERN_START = "ResourcePattern("

    C_RES_TYPE = 'resource_type'
    C_RES_NAME = 'resource_name'
    C_PATTERN_TYPE = 'pattern_type'
    C_ACLS = 'acls'
    C_ACL_PRINCIPAL = 'acl_principal'
    C_ACL_HOST = 'acl_host'
    C_ACL_OPERATION = 'acl_operation'
    C_ACL_PERMISSION_TYPE = 'acl_permission_type'

    PERM_ALLOW = "ALLOW"

    @staticmethod
    def list_acls(bootstrap_server, command_config):


        kafka_acl_list_command = ["kafka-acls",
                                  "--bootstrap-server", bootstrap_server,
                                  "--list"]
        if command_config:
            kafka_acl_list_command.extend(["--command-config", command_config])

        result = subprocess.run(kafka_acl_list_command, stdout=subprocess.PIPE) # , capture_output=True)
        return result.stdout.decode('utf-8')

    @classmethod
    def __is_ignored(cls, line):
        return line.startswith(cls.TIMESTAMP_START) or len(line.strip()) == 0

    @classmethod
    def __is_main_line(cls, line):
        return line.startswith(cls.MAIN_START)

    @classmethod
    def __parse_main_line(cls, line):
        # Current ACLs for resource `ResourcePattern(resourceType=TOPIC, name=_confluent-monitoring, patternType=LITERAL)`:
        # extract the ResourcePattern using the ()
        start = line.find(cls.RESOURCE_PATTERN_START)
        if start == -1:
            raise RuntimeError("Missing 'ResourcePattern()' in resource header")

        resource_ptn_str = line[start + len(cls.RESOURCE_PATTERN_START):len(line) - 3]

        items = resource_ptn_str.split(", ")
        if len(items) != 3:
            raise RuntimeError(f"Invalid ResourcePattern(), not the right amount of items (needs 3)")

        resource_type = items[0].split("=")
        if len(resource_type) != 2:
            raise RuntimeError(f"Invalid resource type description: {resource_type}")

        resource_name = items[1].split("=")
        if len(resource_name) != 2:
            raise RuntimeError(f"Invalid resource name description: {resource_name}")

        pattern_type = items[2].split("=")
        if len(pattern_type) != 2:
            raise RuntimeError(f"Invalid pattern type description: {pattern_type}")

        return resource_type[1], resource_name[1], pattern_type[1]

    @classmethod
    def __parse_acl_line(cls, line):
        # (principal=User:control_center, host=*, operation=CREATE, permissionType=ALLOW)

        items = line[1:len(line) - 1].split(", ")
        if len(items) != 4:
            raise RuntimeError(f"Invalid ACL detail, not the right amount of items (needs 4)")

        acl_principal = items[0].split("=")
        if len(acl_principal) != 2:
            raise RuntimeError(f"Invalid ACL principal description: {acl_principal}")

        acl_host = items[1].split("=")
        if len(acl_host) != 2:
            raise RuntimeError(f"Invalid ACL host description: {acl_host}")

        acl_operation = items[2].split("=")
        if len(acl_operation) != 2:
            raise RuntimeError(f"Invalid ACL operation description: {acl_operation}")

        acl_permission_type = items[3].split("=")
        if len(acl_permission_type) != 2:
            raise RuntimeError(f"Invalid ACL permission type description: {acl_permission_type}")

        return {
            cls.C_ACL_PRINCIPAL: acl_principal[1],
            cls.C_ACL_HOST: acl_host[1],
            cls.C_ACL_OPERATION: acl_operation[1],
            cls.C_ACL_PERMISSION_TYPE: acl_permission_type[1]
        }

    @classmethod
    def parse_acl_output(cls, acl_output) -> List[Dict]:
        lines = acl_output.split("\n")

        results = []
        resource_type = resource_name = pattern_type = None
        acls = []

        for line in lines:
            line = line.strip()

            if cls.__is_ignored(line):
                continue

            if cls.__is_main_line(line):
                # not the first resource, we save the previous one
                if resource_type:
                    results.append({
                        cls.C_RES_TYPE: resource_type,
                        cls.C_RES_NAME: resource_name,
                        cls.C_PATTERN_TYPE: pattern_type,
                        cls.C_ACLS: acls
                    })

                resource_type, resource_name, pattern_type = cls.__parse_main_line(line)
                acls = []
            else:
                acl = cls.__parse_acl_line(line)
                acls.append(acl)

        # save last set
        if resource_type:
            results.append({
                cls.C_RES_TYPE: resource_type,
                cls.C_RES_NAME: resource_name,
                cls.C_PATTERN_TYPE: pattern_type,
                cls.C_ACLS: acls
            })

        return results
