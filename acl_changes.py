class ACLChanges():
    def __init__(self, acls_to_create, acls_to_delete):
        self.acls_to_create = acls_to_create
        self.acls_to_delete = acls_to_delete

    def apply_to_cluster(self, admin_client, connect_config, command_config):
        pass

    def apply_to_scripts(self, connect_config, command_config):
        pass
