import subprocess

from constants import Consts


class ACLChanges():
    def __init__(self, acls_to_create, acls_to_delete, admin_client, bootstrap_server_url, command_config):
        self.acls_to_create = acls_to_create
        self.acls_to_delete = acls_to_delete
        self.admin_client = admin_client
        self.bootstrap_server_url = bootstrap_server_url
        self.command_config = command_config

    @staticmethod
    def run_command(command):
        command_as_list = command.split(" ")
        result = subprocess.run(command_as_list, stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8')

    def apply_to_cluster(self):
        # builds script lists
        commands = self.add_commands()
        commands += self.delete_commands()

        output = ""
        for cmd in commands:
            output += self.run_command(cmd) + "\n"

        return output

    def add_commands(self):
        output = []

        for acl in self.acls_to_create:
            command_config_option = f"--command-config {self.command_config} " if self.command_config else ""

            allow_option = "--allow-principal" if acl[Consts.A_ALLOW] else "--deny-principal"
            type_option = "--topic" if acl[Consts.A_PATTERN_TYPE] == Consts.A_RESOURCE_TYPE_TOPIC else "--group"

            create_acl_cmd = f"kafka-acls --bootstrap-server {self.bootstrap_server_url} {command_config_option}" \
                             f"--add {type_option} {acl[Consts.A_NAME]} {allow_option} User:{acl[Consts.A_PRINCIPAL]} " \
                             f"--operation {acl[Consts.A_OPERATION]}"

            output.append(create_acl_cmd)

        return output

    def delete_commands(self):
        output = []

        for acl in self.acls_to_delete:
            command_config_option = f"--command-config {self.command_config} " if self.command_config else ""

            allow_option = "--allow-principal" if acl[Consts.A_ALLOW] else "--deny-principal"
            type_option = "--topic" if acl[Consts.A_PATTERN_TYPE] == Consts.A_RESOURCE_TYPE_TOPIC else "--group"

            delete_acl_cmd = f"kafka-acls --bootstrap-server {self.bootstrap_server_url} {command_config_option}" \
                             f"--force --remove {type_option} {acl[Consts.A_NAME]} " \
                             f"{allow_option} User:{acl[Consts.A_PRINCIPAL]} " \
                             f"--operation {acl[Consts.A_OPERATION]}"

            output.append(delete_acl_cmd)

        return output


    def apply_to_scripts(self):
        # builds script lists
        output = self.add_commands()
        output += self.delete_commands()

        return "\n".join(output)
