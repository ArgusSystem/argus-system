import { daytimeToString, timestampToString } from './format.js';
import { fetchPeople } from './api/people.js';
import { fetchRoles } from './api/roles.js';
import { fetchCameras } from './api/cameras.js';
import { fetchAreas } from './api/areas.js';
import { fetchAreaTypes } from './api/area_types.js';

function to_dict(array) {
    return array.reduce((result, value) => {
        result[value.id] = value.name;
        return result;
    }, {});
}

function format_text(node, mapping) {
    return node.map(n => {
        if (!(n.type in mapping))
            return n.type.toUpperCase();

        return `(${n.value.map(v => mapping[n.type][v]).join(', ')})`;
    }).join(' OR ');
}

function format_time(node) {
    return node.map(n => {
        if (n.type === 'repeated') {
            const day = n.value.days.length === 7 ?
                'Everyday' :
                n.value.days.map(d => d.substring(0, 2)).join(', ');

            return `${day} FROM ${daytimeToString(n.value['start_time'])} TO ${daytimeToString(n.value['end_time'])}`;
        } else {
            return `FROM ${timestampToString(n.value['start_time'])} TO ${timestampToString(n.value['end_time'])}`;
        }
    }).join(', ');
}

export async function createRuleContext() {
    return new RuleContext(
        await fetchPeople(), await fetchRoles(),
        await fetchCameras(), await fetchAreas(), await fetchAreaTypes());
}

export class RuleContext {
    constructor (people, roles, cameras, areas, area_types) {
        this.who = {
            'person': to_dict(people),
            'role': to_dict(roles)
        };

        this.where = {
            'camera': to_dict(cameras),
            'area': to_dict(areas),
            'area_type': to_dict(area_types)
        };
    }

    formatToString(rule) {
        const ruleStruct = this.formatToStruct(rule);
        return `${ruleStruct.who} NOT ALLOWED AT ${ruleStruct.where} ON ${ruleStruct.when}`;
    }

    formatToStruct(rule) {
        return {
            who: this.#who(rule.who),
            where: this.#where(rule.where),
            when: this.#when(rule.when)
        };
    }

    #who(who) {
        return format_text(who, this.who);
    }

    #where(where) {
        return format_text(where, this.where);
    }

    #when(when) {
        return format_time(when);
    }
}