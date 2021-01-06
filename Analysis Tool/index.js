'use strict'

// ----------------------------------------------------------------------------

const root = process.argv[2]

global.config = require(`./data/${root}/config.js`)
global.config.bscc = `${global.config.bootstrap_server_switch} ${global.config.command_config_switch}`

if (global.config.automatic_repartition_deletes) console.error('AUTOMATIC REPARTITION TOPIC DELETE ACL MODE ENABLED')

// ----------------------------------------------------------------------------

const indent = '    '

// ----------------------------------------------------------------------------

const fs = require('fs')

const { topics_now, topics_new, acls_now, acls_new } = require('./gather_topic_acl_info')

// ----------------------------------------------------------------------------

const fmts = {
    acls: ['topic', 'principal', 'type', 'operation'],
    topics: ['topic', 'partitions', 'maxbytes']
}

// ----------------------------------------------------------------------------

const comp = (l, fmt, delim = '|') =>
    fmts[fmt].map(kn => l[kn]).join(delim)

// ----------------------------------------------------------------------------

const decomp = (l, fmt) => {
    const vals = l.split('|')
    return fmts[fmt].reduce((rv, kn, i) => {
        if (kn[0] === '#') {
            rv[kn.slice(1)] = +vals[i]
        } else {
            rv[kn] = vals[i]
        }
        return rv
    }, {})
}

// ----------------------------------------------------------------------------

Array.prototype.uniq = function () { return this.filter((e, i) => this.indexOf(e) === i) }

// ----------------------------------------------------------------------------

const topic_names_now = topics_now.map(t => t.topic).sort()
const topic_names_new = topics_new.map(t => t.topic).sort()

// ----------------------------------------------------------------------------

const topics_added = topic_names_new.filter(tn => !topic_names_now.includes(tn))
const topics_removed = topic_names_now.filter(tn => !topic_names_new.includes(tn))
const topics_added_needing_delete_acl = topics_added.filter(tn => tn.endsWith('-repartition'))

// ----------------------------------------------------------------------------

const topics_common = topic_names_now.filter(tn => topic_names_new.includes(tn))
const topic_in_recreates = tn => global.config.recreates.includes(tn)
const topic_in_recreates_msg1 = tn => topic_in_recreates(tn) ? 'Topic Recreate Scheduled' : '*** TOPIC NEEDS TO BE RECREATED ***'
const topic_in_recreates_msg2 = tn => topic_in_recreates(tn) ? 'Topic Recreate Scheduled' : '*** TOPIC ALTER WILL BE GENERATED ***'

const topics_parts = topics_common.reduce((rv, tn) => {
    const parts_now = topics_now.find(t => t.topic === tn).partitions
    const parts_new = topics_new.find(t => t.topic === tn).partitions

    if (parts_now != parts_new) {
        rv.push(`${tn} (${parts_now} => ${parts_new}) -- ${topic_in_recreates_msg1(tn)}`)
    }

    return rv
}, [])

const topics_maxbytes = topics_common.reduce((rv, tn) => {
    const mbs_now = topics_now.find(t => t.topic === tn).maxbytes
    const mbs_new = topics_new.find(t => t.topic === tn).maxbytes

    if (mbs_now != mbs_new) {
        rv.push(`${tn} (${mbs_now || '<none>'} => ${mbs_new || '<none>'}) -- ${topic_in_recreates_msg1(tn)}`)
    }

    return rv
}, [])

// ----------------------------------------------------------------------------

const human_readable_time = t => {
    const pieces = {
        days: 86400000,
        hrs: 3600000,
        mins: 60000,
        secs: 1000,
        ms: 1
    }

    t = +t

    if (t === -1) return 'forever'

    return Object.entries(pieces).reduce((rv, ent) => {
        const [unit, factor] = ent
        const inunit = Math.floor(t / factor)
        if (inunit > 0){
            t -= inunit * factor
            rv.push(`${inunit} ${unit}`)
        }
        return rv
    }, []).join(' ')
}

const topics_retention = topics_common.reduce((rv, tn) => {
    const ret_now = human_readable_time(topics_now.find(t => t.topic === tn).retention)
    const ret_new = human_readable_time(topics_new.find(t => t.topic === tn).retention)

    if (ret_now != ret_new) {
        rv.push({ topic: tn, ret_now, ret_new, recreated: topic_in_recreates(tn) })
    }

    return rv
}, []).filter(tr => !tr.recreated)

const topics_retentions = topics_retention.map(tr => `${tr.topic} (${tr.ret_now} => ${tr.ret_new}) -- ${topic_in_recreates_msg2(tr.topic)}`)

const topics_finite_retention = topics_new.filter(t => t.retention != -1).map(t => `${t.topic} (${human_readable_time(t.retention)})`)

// ----------------------------------------------------------------------------

const acls_compressed_now = acls_now.map(acl => comp(acl, 'acls'))
const acls_compressed_new = acls_new.map(acl => comp(acl, 'acls'))

// ----------------------------------------------------------------------------

const acls_addedA = acls_compressed_new.filter(acl => !acls_compressed_now.includes(acl)).map(acl => decomp(acl, 'acls'))

const acls_added = (! global.config.automatic_repartition_deletes ? acls_addedA :
    acls_addedA.concat(
        acls_addedA
            .filter(acl => topics_added.includes(acl.topic) && acl.topic.endsWith('-repartition') && acl.operation === 'READ')
            .map(acl => ({ topic: acl.topic, principal: acl.principal, type: acl.type, operation: 'DELETE'}))
    )
)

const acls_removedA = acls_compressed_now.filter(acl => !acls_compressed_new.includes(acl)).map(acl => decomp(acl, 'acls'))

const acls_removed = (! global.config.automatic_repartition_deletes ? acls_removedA :
    acls_removedA.filter(acl => ! (acl.operation.toUpperCase() === 'DELETE' && acl.topic.endsWith('-repartition'))))

// ----------------------------------------------------------------------------

const acls_now_no_topic = acls_now.filter(acl => !topic_names_now.includes(acl.topic)).map(l => comp(l, 'acls', ' -- '))
const acls_new_no_topic = acls_new.filter(acl => !topic_names_new.includes(acl.topic)).map(l => comp(l, 'acls', ' -- '))

// ----------------------------------------------------------------------------

const acls_added_existing = acls_added.filter(acl => topic_names_now.includes(acl.topic))
const acls_added_added = acls_added.filter(acl => topics_added.includes(acl.topic))
const acls_removed_existing = acls_removed.filter(acl => topic_names_now.includes(acl.topic))

// ----------------------------------------------------------------------------

const elim_prefixes = (tnl, pl) => tnl.filter(tn => !pl.some(p => tn.startsWith(p) || p === '*'))

const read_prefixes_now = acls_now.filter(acl => acl.type === 'PREFIXED' && acl.operation === 'READ').map(acl => acl.topic)
const write_prefixes_now = acls_now.filter(acl => acl.type === 'PREFIXED' && acl.operation === 'WRITE').map(acl => acl.topic)

const elim_read_prefixes_now = tnl => elim_prefixes(tnl, read_prefixes_now)
const elim_write_prefixes_now = tnl => elim_prefixes(tnl, write_prefixes_now)
const elim_read_write_prefixes_now = tnl => elim_read_prefixes_now(elim_write_prefixes_now(tnl))

const read_prefixes_new = acls_new.filter(acl => acl.type === 'PREFIXED' && acl.operation === 'READ').map(acl => acl.topic)
const write_prefixes_new = acls_new.filter(acl => acl.type === 'PREFIXED' && acl.operation === 'WRITE').map(acl => acl.topic)

const elim_read_prefixes_new = tnl => elim_prefixes(tnl, read_prefixes_new)
const elim_write_prefixes_new = tnl => elim_prefixes(tnl, write_prefixes_new)
const elim_read_write_prefixes_new = tnl => elim_read_prefixes_new(elim_write_prefixes_new(tnl))

// ----------------------------------------------------------------------------

const topics_access_now = acls_now.reduce((rv, acl) => {
    rv[acl.topic] = rv[acl.topic] || []
    if (!rv[acl.topic].includes(acl.operation)) {
        rv[acl.topic].push(acl.operation)
    }
    return rv
}, {})

const topics_na_now = elim_read_write_prefixes_now(topic_names_now.filter(tn => !topics_access_now[tn]))
const topics_ro_now = elim_write_prefixes_now(topic_names_now.filter(tn => topics_access_now[tn] && topics_access_now[tn].includes('READ') && !topics_access_now[tn].includes('WRITE')))
const topics_wo_now = elim_read_prefixes_now(topic_names_now.filter(tn => topics_access_now[tn] && topics_access_now[tn].includes('WRITE') && !topics_access_now[tn].includes('READ')))

// ----------------------------------------------------------------------------

const topics_access_new = acls_new.reduce((rv, acl) => {
    rv[acl.topic] = rv[acl.topic] || []
    if (!rv[acl.topic].includes(acl.operation)) {
        rv[acl.topic].push(acl.operation)
    }
    return rv
}, {})

const topics_na_new = elim_read_write_prefixes_new(topic_names_new.filter(tn => !topics_access_new[tn]))
const topics_ro_new = elim_write_prefixes_new(topic_names_new.filter(tn => topics_access_new[tn] && topics_access_new[tn].includes('READ') && !topics_access_new[tn].includes('WRITE')))
const topics_wo_new = elim_read_prefixes_new(topic_names_new.filter(tn => topics_access_new[tn] && topics_access_new[tn].includes('WRITE') && !topics_access_new[tn].includes('READ')))

// ----------------------------------------------------------------------------

const principals_now = acls_now.map(acl => acl.principal).sort().uniq()
const principals_new = acls_new.map(acl => acl.principal).sort().uniq()

// ----------------------------------------------------------------------------

const principals_new_cn = principals_new.filter(p => p.match(/^...-.*-kfkusr\d{3,3}$/))
const principals_new_old = principals_new.filter(p => p.match(/^xq...kfkusr\d{1,2}$/))

// ----------------------------------------------------------------------------

const principals_added = principals_new.filter(p => !principals_now.includes(p))
const principals_removed = principals_now.filter(p => !principals_new.includes(p))

// ============================================================================

const show = (heading, content, options = {}) => {
    if (options.fmt) content = content.map(l => comp(l, options.fmt, ' -- '))
    content = content.sort().uniq()
    heading += ` (${content.length}):`
    console.log('\n%s\n%s\n\n%s%s\n', heading, '='.repeat(heading.length), indent, content.length ? content.join('\n' + indent) : '--- none ---')
}

// ----------------------------------------------------------------------------

const missing = (a1, a2, marker) => a1.map(i1 => (a2.includes(i1)) ? i1 : `${i1} (${marker})`)

// ----------------------------------------------------------------------------

const mne_prins = principals =>
    principals.map(p => {
        const m1 = p.match(/^xq(...)kfkusr\d{3,3}$/)
        if (m1) p += ` -- ${m1[1].toUpperCase()}`

        const m2 = p.match(/^xq(...)kfkusr\d$/)
        if (m2) p += ` -- ${m2[1].toUpperCase()}`

        const m3 = p.match(/^(...)-[^-]*-kfkusr\d{3,3}$/)
        if (m3) p += ` -- ${m3[1].toUpperCase()}`

        if (!m1 && !m2 && !m3) p += ` -- NO MNEMONIC`

        return p
    })

// ----------------------------------------------------------------------------

const title = (s, m) => `${m.substr(0,1).repeat(Math.floor((98 - s.length) / 2))} ${s} ${m.substr(-1,1).repeat(Math.ceil((98 - s.length) /2))}`

// ----------------------------------------------------------------------------

const description = `${root} -- ${global.config.request || 'MISSING REQUEST'}`

if (global.config.show_report) {
    console.log('Run Timestamp: %s', (new Date()).toLocaleString())
    console.log()
    console.log()
    console.log(title(description, '><'))
    console.log()

    show('Topics to be Recreated', global.config.recreates)

    show('Topics Added', topics_added)
    show('Topics Removed', topics_removed)

    show('New Repartition Topics Needing a DELETE ACL', topics_added_needing_delete_acl)

    show('Topics with Partition Change', topics_parts)
    show('Topics with Max Bytes Change', topics_maxbytes)

    show('Topics with Retention Change', topics_retentions)
    show('Topics with Finite Retention After', topics_finite_retention)

    show('ACLs Added', acls_added, { fmt: 'acls' })
    show('ACLs Removed', acls_removed, { fmt: 'acls' })

    show('ACLs Added to Existing Topics', acls_added_existing, { fmt: 'acls' })
    show('ACLs Removed from Existing Topics', acls_removed_existing, { fmt: 'acls' })

    show('ACLs Added to Added Topics', acls_added_added, { fmt: 'acls' })

    show('ACLs Before Missing a Specific Topic', missing(acls_now_no_topic, acls_new_no_topic, '-'))
    show('ACLs After Missing a Specific Topic', missing(acls_new_no_topic, acls_now_no_topic, '+'))

    show('Topics No Access Before', missing(topics_na_now, topics_na_new, '-'))
    show('Topics No Access After', missing(topics_na_new, topics_na_now, '+'))

    show('Topics Read-Only Before', missing(topics_ro_now, topics_ro_new, '-'))
    show('Topics Read-Only After', missing(topics_ro_new, topics_ro_now, '+'))

    show('Topics Write-Only Before', missing(topics_wo_now, topics_wo_new, '-'))
    show('Topics Write-Only After', missing(topics_wo_new, topics_wo_now, '+'))

    show('Principals Added', mne_prins(principals_added))
    show('Principals Removed', mne_prins(principals_removed))

    show('Principals After Using Old Style CN', mne_prins(principals_new_cn))
    show('Principals After Using Old Style UPN', mne_prins(principals_new_old))
    show('Principals After', mne_prins(principals_new))
}

// ----------------------------------------------------------------------------

if (global.config.write_script) {

    // ----------------------------------------------------

    const header = ['#! /bin/bash', '', 'set +e    # continue on error', '', 'echo', `echo '${title(description, '><')}'`, 'echo' ]

    const topic_recreates =
        global.config.recreates.map(topic =>
            [
                global.local_topic_creates.filter(tc => tc.match(` ${topic.trim()} `)).map(tc => tc.replace('--create', '--delete').replace(/ --partitions.*/, '')),
                global.local_topic_creates.filter(tc => tc.match(` ${topic.trim()} `))
            ]
        ).flat(2).filter(l => l)
    if (topic_recreates.length != global.config.recreates.length * 2) throw new Error('Generated topic recreates out of balance.')

    const topic_creates =
        topics_added.sort().map(tn => global.local_topic_creates.filter(tc => tc.match(` ${tn} `))).flat().filter(l => l)

    const td_template = `kafka-topics --delete ${global.config.bscc} --topic '%1'`
    const topic_deletes =
        topics_removed.sort().map(tn => td_template.replace('%1', tn))

    const tar_template = `kafka-configs --alter ${global.config.zookeeper_server_switch} --entity-type topics --entity-name %1 --add-config retention.ms=%2`
    const topic_alters =
            topics_retention.map(tr => tar_template.replace('%1', tr.topic).replace('%2', tr.ret_new))

    Array.prototype.sortACLs = function () {
        return this.sort((a, b) => {
            if (a.topic > b.topic) return 1
            if (a.topic < b.topic) return -1
            if (a.operation > b.operation) return 1
            if (a.operation < b.operation) return -1
            if (a.principal > b.principal) return 1
            if (a.principal < b.principal) return -1
            return 0
        })
    }

    const aa_template = `kafka-acls --add ${global.config.bscc} --topic %1 --allow-principal User:%2 --resource-pattern-type %3 --operation %4`
    const acl_adds =
        acls_added.sortACLs().map(acl => aa_template.replace('%1', acl.topic).replace('%2', acl.principal).replace('%3', acl.type).replace('%4', acl.operation))

    const ar_template = `kafka-acls --remove --force ${global.config.bscc} --topic %1 --allow-principal User:%2 --resource-pattern-type %3 --operation %4`
    const acl_removes =
        acls_removed.sortACLs().map(acl => ar_template.replace('%1', acl.topic).replace('%2', acl.principal).replace('%3', acl.type).replace('%4', acl.operation))

    // ----------------------------------------------------

    const echo = s => ['', 'echo', `echo '==== ${s} ${'='.repeat(94 - s.length)}'`, 'echo', '']

    let file = []

    file = file.concat(header)

    if (topic_recreates.length) {
        file = file.concat(
            echo(`${topic_recreates.length / 2} TOPIC RECREATE(S)`),
            topic_recreates,
        )
    }

    if (topic_creates.length) {
        file = file.concat(
            echo(`${topic_creates.length} TOPIC CREATE(S)`),
            topic_creates,
        )
    }

    if (topic_deletes.length) {
        file = file.concat(
            echo(`${topic_deletes.length} TOPIC DELETE(S)`),
            topic_deletes,
        )
    }

    if (topic_alters.length) {
        file = file.concat(
            echo(`${topic_alters.length} TOPIC ALTER(S)`),
            topic_alters,
        )
    }

    if (acl_adds.length) {
        file = file.concat(
            echo(`${acl_adds.length} ACL ADD(S)`),
            acl_adds,
        )
    }

    if (acl_removes.length) {
        file = file.concat(
            echo(`${acl_removes.length} ACL REMOVE(S)`),
            acl_removes,
        )
    }

    file = file.concat(echo('JOB COMPLETED'))

    fs.writeFileSync(`data/${root}/script1.sh`, file.flat().join('\n'))
}

// ----------------------------------------------------------------------------