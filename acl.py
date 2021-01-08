class ACL:
    def __init__(self, name, principal, operation, type, allow):
        self.name = name
        self.principal = principal
        self.operation = operation
        self.type = type
        self.allow = allow
        self.signature = f"{self.name}/{self.principal}/{self.operation}/{self.type}/{self.allow}"
