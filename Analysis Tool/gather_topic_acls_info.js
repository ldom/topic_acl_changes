'use strict'

// ----------------------------------------------------------------------------

const fs = require('fs')

// ----------------------------------------------------------------------------

const {

    remote_server,
    bscc,
    ignore_topics,
    provided_placement_file,
    active_placement_file,

} = global.config

// ----------------------------------------------------------------------------

const local_script =
    fs
        .readFileSync(global.config.local_script, 'utf8')
        .replace(/\r/g, '')
        .split('\n')

global.local_topic_creates =
    local_script
        .filter(l => l.match(/^kafka-topics/))
        .map(l => l.replace(provided_placement_file, active_placement_file))

global.local_acl_creates =
    local_script
        .filter(l => l.match(/^kafka-acls/) && !l.match(/--group/))

// ----------------------------------------------------------------------------

const shell = cmd => require('child_process').execSync(cmd, { encoding: 'utf8' })

// ----------------------------------------------------------------------------

const extract = (raw, fields, replacements=[]) => {
    return raw
        .map(line => Object.entries(fields).reduce((outer, field) => {
            const [ k, v ] = field
            const matches = (line + ' ').match(v)
            outer[k] = replacements.reduce((inner, replacement) => inner.replace(...replacement), (matches || [])[1] || '')
            return outer
        }, {}))
        .filter(it => ! ignore_topics.some(pat => it.topic.match(pat)))
}

// ----------------------------------------------------------------------------

const get_remote_topics = () => {
    const raw = shell(`ssh ${remote_server} "sudo kafka-topics --describe ${bscc} 2> /dev/null | egrep -e'^Topic' | grep -v -e'Topic: _'`)
        .split('\n')
        .map(line => line.trim())

    const fields = {
        'topic': /Topic: ([^ ,\t]*)/,
        'partitions': /PartitionCount: ([^ ,\t]*)/,
        'maxbytes': /max.message.bytes=([^ ,\t]*)/,
        'retention': /retention.ms=([^ ,\t]*)/,
    }

    return extract(raw, fields)
}

// ----------------------------------------------------------------------------

const get_local_topics = () => {
    const fields = {
        'topic': /--topic '?([^ ,\t']*)'? /,
        'partitions': /--partitions ([^ ,\t]*) /,
        'maxbytes': /max.message.bytes=([^ ,\t]*) /,
        'retention': /retention.ms=([^ ,\t]*) /,
    }

    return extract(global.local_topic_creates, fields)
}

// ----------------------------------------------------------------------------

const parse_remote_acls = (raw) => {
    let topic = '', type = ''

    return raw.reduce((rv, line, i) => {
        const aclm = line.match(/\(principal=User:([^,]*),.*operation=([^,]*),.*\)$/)

        if (aclm) {
            rv.push({ topic, principal: aclm[1], type, operation: aclm[2] })
        } else {
            const resm = line.match(/Current ACLs for.*, name=([^,]*), patternType=([^,)]*)/)

            if (resm) {
                topic = resm[1]
                type = resm[2]
            } else {
                throw new Error(`Bad line (${i + 1}) in ACL information`)
            }
        }

        return rv
    }, [])
}

const get_remote_acls = () => {
    try {
        return (parse_remote_acls(
            shell(`ssh ${remote_server} "sudo kafka-acls ${bscc} --list 2> /dev/null"`)
                .split('\n')
                .map(l => l.trim())
                .filter(l => l)
        )
        .filter(acl => ! ignore_topics.some(pat => acl.topic.match(pat))))
    }
    catch (e) {
        return []
    }
}

// ----------------------------------------------------------------------------

const get_local_acls = () => {
    const fields = {
        topic: /--topic ([^ ,\t]*) /,
        principal: /--allow-principal ([^ ,\t]*) /,
        type: /--resource-pattern-type ([^ ,\t]*) /,
        operation: /--operation ([^ ,\t]*) /
    }

    const replacements = [
        [ /'/g, '' ],
        [ 'User:', '' ],
        [ 'Read', 'READ' ],
        [ 'Write', 'WRITE' ],
    ]

    return extract(global.local_acl_creates, fields, replacements)
}

// ----------------------------------------------------------------------------

module.exports =
{
    topics_now: get_remote_topics(),
    topics_new: get_local_topics(),
    acls_now: get_remote_acls(),
    acls_new: get_local_acls(),
}

// ----------------------------------------------------------------------------

// const tn = 'MPCFIS.retail_deposits'

// console.error('now: %s', JSON.stringify(module.exports.topics_now.filter(t => t.topic === tn)))
// console.error('new: %s', JSON.stringify(module.exports.topics_new.filter(t => t.topic === tn)))
