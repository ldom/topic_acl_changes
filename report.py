from constants import Consts, ResultSet

titles_map = {
    ResultSet.TOPICS_ADDED: "Topics Added",
    ResultSet.TOPICS_REMOVED: "Topics Removed",
    ResultSet.TOPICS_UPDATED: "Topics Updated",
    ResultSet.TOPICS_PARTITION_CHANGED: "Topics with Partitions Changed",
    ResultSet.TOPICS_MAX_BYTES_CHANGED: "Topics with Max Bytes Changed",
    ResultSet.TOPICS_RETENTION_CHANGED: "Topics with Retention Changed",
    ResultSet.TOPICS_FINITE_RETENTION: "Topics with Finite Retention",

    ResultSet.ACLS_ADDED: "ACLs Added",
    ResultSet.ACLS_REMOVED: "ACLs Removed",
    ResultSet.ACLS_ADDED_TO_EXISTING_TOPICS: "ACLs Added to Existing Topics",
    ResultSet.ACLS_REMOVED_FROM_EXISTING_TOPICS: "ACLs Removed from Existing Topics",
    ResultSet.ACLS_ADDED_TO_ADDED_TOPICS: "ACLs Added to Added Topics",
    ResultSet.ACLS_BEFORE_MISSING_TOPIC: "ACLs with No Topics - Before",
    ResultSet.ACLS_AFTER_MISSING_TOPIC: "ACLs with No Topics - After",

    ResultSet.TOPICS_NO_ACCESS_BEFORE: "ACLs with No Access - Before",
    ResultSet.TOPICS_NO_ACCESS_AFTER: "ACLs with No Access - After",
    ResultSet.TOPICS_RO_BEFORE: "ACLs with Read-only Access - Before",
    ResultSet.TOPICS_RO_AFTER: "ACLs with Read-only Access - After",
    ResultSet.TOPICS_WO_BEFORE: "ACLs with Write-only Access - Before",
    ResultSet.TOPICS_WO_AFTER: "ACLs with Write-only Access - After",

    ResultSet.PRINCIPALS_ADDED: "Principals Added",
    ResultSet.PRINCIPALS_REMOVED: "Principals Removed",
    ResultSet.PRINCIPALS_USING_OLD_CN: "Principals using Old-style CN",
    ResultSet.PRINCIPALS_USING_OLD_UPN: "Principals using Old-style UPN",
    ResultSet.PRINCIPALS_AFTER: "Principals After",
}


def output_report(result_sets):
    for result_set_number, result_set in result_sets.items():
        print(f"{titles_map[result_set_number]}")
        for result in result_set:
            print(result)
        print("------------------------------------------------------------------")


def output_changes(result_sets, before_topics, before_acls, after_topics, after_acls):
    # prepare the work to do: take result sets and build lists with all the details (topic config, etc)
    topics_to_add = [after_topics[topic_name] for topic_name in result_sets[ResultSet.TOPICS_ADDED]]
    topics_to_remove = [before_topics[topic_name] for topic_name in result_sets[ResultSet.TOPICS_REMOVED]]
    topics_to_update = [after_topics[topic_name] for topic_name in result_sets[ResultSet.TOPICS_UPDATED]]

    acls_to_add = [after_acls[acl_sig] for acl_sig in result_sets[ResultSet.ACLS_ADDED]]
    acls_to_remove = [before_acls[acl_sig] for acl_sig in result_sets[ResultSet.ACLS_REMOVED]]

    return {
        Consts.TOPICS: {Consts.ADDED: topics_to_add,
                        Consts.UPDATED: topics_to_update,
                        Consts.REMOVED: topics_to_remove},

        Consts.ACLS: {Consts.ADDED: acls_to_add,
                      Consts.REMOVED: acls_to_remove}
    }
