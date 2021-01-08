from typing import Dict, Set

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

    access_to_before_topics = None
    access_to_after_topics = None

    sets[ResultSet.TOPICS_RO_BEFORE] = set()
    sets[ResultSet.TOPICS_RO_AFTER] = set()
    sets[ResultSet.TOPICS_WO_BEFORE] = set()
    sets[ResultSet.TOPICS_WO_AFTER] = set()

    return sets
