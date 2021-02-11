from enum import Enum, auto


class Consts:
    TOPICS = "topics"
    ACLS = "acls"

    T_TOPIC = "topic"
    T_NAME = "name"
    T_PARTITIONS = "partitions"
    T_PLACEMENT = "placement"
    T_CONFIG = "config"
    T_CONFIG_PROPS = "config_properties"

    T_PLACEMENT_PROP = 'confluent.placement.constraints'
    T_NB_PARTITIONS = 'nb_partitions'
    T_OBSERVERS = "observers"

    A_NAME = 'name'
    A_PRINCIPAL = 'principal'
    A_TYPE = 'type'
    A_OPERATION = 'operation'
    A_ALLOW = 'allow'
    A_SIGNATURE = 'signature'

    A_TYPE_TOPIC = 'TOPIC'

    CFG_MAX_BYTES = 'max.message.bytes'
    CFG_RETENTION = 'retention.ms'
    CFG_BOOTSTRAP = 'bootstrap.servers'

    READ_OPERATION = "read"
    WRITE_OPERATION = "write"

    ADDED = 'added'
    UPDATED = 'updated'
    REMOVED = 'removed'


class ResultSet(Enum):
    TEST = auto()

    TOPICS_ADDED = auto()
    TOPICS_REMOVED = auto()
    TOPICS_PARTITION_CHANGED = auto()
    TOPICS_MAX_BYTES_CHANGED = auto()
    TOPICS_RETENTION_CHANGED = auto()
    TOPICS_FINITE_RETENTION = auto()
    TOPICS_UPDATED = auto()

    ACLS_ADDED = auto()
    ACLS_REMOVED = auto()
    ACLS_ADDED_TO_EXISTING_TOPICS = auto()
    ACLS_REMOVED_FROM_EXISTING_TOPICS = auto()
    ACLS_ADDED_TO_ADDED_TOPICS = auto()
    ACLS_BEFORE_MISSING_TOPIC = auto()
    ACLS_AFTER_MISSING_TOPIC = auto()

    TOPICS_NO_ACCESS_BEFORE = auto()
    TOPICS_NO_ACCESS_AFTER = auto()
    TOPICS_RO_BEFORE = auto()
    TOPICS_RO_AFTER = auto()
    TOPICS_WO_BEFORE = auto()
    TOPICS_WO_AFTER = auto()

    PRINCIPALS_ADDED = auto()
    PRINCIPALS_REMOVED = auto()
    PRINCIPALS_USING_OLD_CN = auto()
    PRINCIPALS_USING_OLD_UPN = auto()
    PRINCIPALS_AFTER = auto()
