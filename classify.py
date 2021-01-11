from typing import Dict, Set, Tuple

from constants import Consts, ResultSet


def classify_topics(before, after) -> Dict[ResultSet, Set]:
    sets = {}

    before_topics = set(before.keys())
    after_topics = set(after.keys())

    sets[ResultSet.TOPICS_ADDED] = after_topics - before_topics
    sets[ResultSet.TOPICS_REMOVED] = before_topics - after_topics

    remaining_topics = after_topics - sets[ResultSet.TOPICS_ADDED]

    sets[ResultSet.TOPICS_PARTITION_CHANGED] = set()
    sets[ResultSet.TOPICS_MAX_BYTES_CHANGED] = set()
    sets[ResultSet.TOPICS_RETENTION_CHANGED] = set()
    sets[ResultSet.TOPICS_FINITE_RETENTION] = set()

    for t in remaining_topics:
        topic_before = before[t]
        topic_after = after[t]

        if topic_before.nb_partitions != topic_after.nb_partitions:
            sets[ResultSet.TOPICS_PARTITION_CHANGED].add(t)  # TODO add value

        if topic_before.config_properties.get(Consts.CFG_MAX_BYTES) \
                != topic_after.config_properties.get(Consts.CFG_MAX_BYTES):
            sets[ResultSet.TOPICS_MAX_BYTES_CHANGED].add(t)  # TODO add value

        if topic_before.config_properties.get(Consts.CFG_RETENTION) \
                != topic_after.config_properties.get(Consts.CFG_RETENTION):
            sets[ResultSet.TOPICS_RETENTION_CHANGED].add(t)  # TODO add value

    for t in after_topics:
        topic_after = after[t]

        if topic_after.config_properties.get(Consts.CFG_RETENTION) != -1:
            sets[ResultSet.TOPICS_FINITE_RETENTION].add(t)  # TODO add value

    return sets


def access_map(acls) -> Dict[str, Dict[str, bool]]:
    result = {}
    for acl in acls.values():
        access_read = access_write = False
        if acl.allow:
            if acl.operation.lower() == Consts.READ_OPERATION:
                access_read = True
            elif acl.operation.lower() == Consts.WRITE_OPERATION:
                access_write = True

            try:
                topic_entry = result[acl.name]
                if access_read:
                    topic_entry[Consts.READ_OPERATION] = True
                if access_write:
                    topic_entry[Consts.WRITE_OPERATION] = True
            except KeyError:
                result[acl.name] = {
                    Consts.READ_OPERATION: access_read,
                    Consts.WRITE_OPERATION: access_write,
                }
    return result


def classify_acls(before_topics, after_topics, before_acls, after_acls) -> Dict[ResultSet, Set]:
    sets = {}

    before_acls_set = set(before_acls.keys())
    after_acls_set = set(after_acls.keys())

    before_topics_set = set(before_topics.keys())
    after_topics_set = set(after_topics.keys())

    added_topics = after_topics_set - before_topics_set

    sets[ResultSet.ACLS_ADDED] = after_acls_set - before_acls_set
    sets[ResultSet.ACLS_REMOVED] = before_acls_set - after_acls_set

    acls_before_on_before_topics = set([k for k,v in before_acls.items() if v.name in before_topics_set])
    acls_after_on_before_topics = set([k for k,v in after_acls.items() if v.name in before_topics_set])

    sets[ResultSet.ACLS_ADDED_TO_EXISTING_TOPICS] = acls_after_on_before_topics - acls_before_on_before_topics
    sets[ResultSet.ACLS_REMOVED_FROM_EXISTING_TOPICS] = acls_before_on_before_topics - acls_after_on_before_topics

    sets[ResultSet.ACLS_ADDED_TO_ADDED_TOPICS] = sets[ResultSet.ACLS_ADDED] \
                                                 - sets[ResultSet.ACLS_ADDED_TO_EXISTING_TOPICS]

    sets[ResultSet.ACLS_BEFORE_MISSING_TOPIC] = set([k for k, v in before_acls.items()
                                                     if v.name not in before_topics_set])
    sets[ResultSet.ACLS_AFTER_MISSING_TOPIC] = set([k for k, v in after_acls.items()
                                                    if v.name not in after_topics_set])

    topics_in_before_acls = set(v.name for v in before_acls.values())
    topics_in_after_acls = set(v.name for v in after_acls.values())

    sets[ResultSet.TOPICS_NO_ACCESS_BEFORE] = before_topics_set - topics_in_before_acls
    sets[ResultSet.TOPICS_NO_ACCESS_AFTER] = after_topics_set - topics_in_after_acls

    access_to_before_topics = access_map(before_acls)
    access_to_after_topics = access_map(after_acls)

    read_access_to_before = set([k for k,v in access_to_before_topics.items() if v[Consts.READ_OPERATION]])
    read_access_to_after = set([k for k,v in access_to_after_topics.items() if v[Consts.READ_OPERATION]])
    write_access_to_before = set([k for k,v in access_to_before_topics.items() if v[Consts.WRITE_OPERATION]])
    write_access_to_after = set([k for k,v in access_to_after_topics.items() if v[Consts.WRITE_OPERATION]])

    sets[ResultSet.TOPICS_RO_BEFORE] = read_access_to_before - write_access_to_before
    sets[ResultSet.TOPICS_RO_AFTER] = read_access_to_after - write_access_to_after
    sets[ResultSet.TOPICS_WO_BEFORE] = write_access_to_before - read_access_to_before
    sets[ResultSet.TOPICS_WO_AFTER] = write_access_to_after - read_access_to_after

    return sets
