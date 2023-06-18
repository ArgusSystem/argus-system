import { redirectToTab } from '../routing.js';
import { fetchRestrictionSeverities } from '../api/restriction_severities.js';
import { Tab } from '../tab.js';
import { fetchWho, loadWho } from './form/who.js';
import { fetchWhere, loadWhere } from './form/where.js';
import { fetchWhen, loadWhen } from './form/when.js';
import { insertRestriction, updateRestriction } from '../api/restrictions.js';

function getSeverityElement() {
    return document.getElementById('select-severity');
}

function fetchSeverity() {
    const selectValue = parseInt(getSeverityElement().value);

    if (isNaN(selectValue))
        throw new Error('Must select a SEVERITY!');

    return selectValue;
}

function fetchData() {
    const data = {
        rule: {
            who: fetchWho(),
            where: fetchWhere(),
            when: fetchWhen()
        },
        severity: fetchSeverity()
    };
    console.log(data);
    return data;
}

async function insert() {
    await with_error_closure(async () => await insertRestriction(fetchData()));
}

async function update(id) {
    await with_error_closure(async () => await updateRestriction(id, fetchData()));
}


async function with_error_closure(callback) {
    try {
        await callback();
        redirectToTab(Tab.RESTRICTIONS);
    } catch (e) {
        alert(e.message);
    }
}

async function onSave(restriction) {
    await (restriction ? update(restriction.id) : insert());
}

export async function loadForm(restriction) {
    await loadWho(restriction ? restriction.rule.who : null);
    await loadWhere(restriction ? restriction.rule.where : null);
    await loadWhen(restriction ? restriction.rule.when : null);

    await fetchRestrictionSeverities().then(data => {
        const selectSeverity = getSeverityElement();
        data.forEach(severity => {
            const selected = restriction && restriction.severity.name === severity.name;
            selectSeverity.appendChild(new Option(severity.name, severity.id, false, selected));
        });
    });

    document.getElementById('cancel-button').onclick = () => redirectToTab(Tab.RESTRICTIONS);
    document.getElementById('save-button').onclick = async () => await onSave(restriction);
}