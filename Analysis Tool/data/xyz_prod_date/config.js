'use strict'

module.exports = {

    request: 'CHG0740501 / CTASK0647527',

    recreates: [
    ],

    show_report: true,
    write_script: true,

    automatic_repartition_deletes: true,

    // ------------------------------------------------------------------------

    remote_server: 'ldsp301a.prod.pncint.net',
    bootstrap_server_switch: '--bootstrap-server ldsp301a.prod.pncint.net:9092',
    command_config_switch: '--command-config /var/local/scripts/command.properties',
    zookeeper_server_switch: '--zookeeper ldsp345a.prod.pncint.net:2181',

    local_script: '/Users/pl76700/Desktop/Kafka/Laurent/dsp-kafka-topic-avro-schemas/topic/dsp_prod_topics_acls_create_bash.sh',

    // local_script: '/Users/PL76700/Desktop/Kafka/Laurent/kafka_iac/out.sh',
    // local_json: '/Users/PL76700/Desktop/Kafka/Laurent/kafka_iac/out.json',

    ignore_topics: [
        /^[ \t]*$/,
        /^connect-cluster-/,
        /^gf\d-connect-cluster-configs$/,
        /^GF2-GF2-/,
        /^heartbeats$/,
        /^mm2/,
        /^MPC/,
        /^myFoo$/,
        /^srm-/,
    ],

    provided_placement_file: 'dsp_prod_topics_acls_placement_async.json',
    active_placement_file: '/var/local/scripts/gf2togf1.json',

}
