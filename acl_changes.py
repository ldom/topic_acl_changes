class ACLChanges():
    def __init__(self, acls_to_create, acls_to_delete, admin_client, bootstrap_server_url, command_config):
        self.acls_to_create = acls_to_create
        self.acls_to_delete = acls_to_delete
        self.admin_client = admin_client
        self.bootstrap_server_url = bootstrap_server_url
        self.command_config = command_config

    def apply_to_cluster(self):
        pass

    def apply_to_scripts(self):
        pass
