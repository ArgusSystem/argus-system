import { createSingleTimeItem, fetchSingleTimeItem } from './components/single_time_item.js';
import { createRepeatedTimeItem, fetchRepeatedTimeItem } from './components/repeated_time_item.js';

const RANDOM_CEIL = 1_000_000;
function getRandomInt() {
    return Math.floor(Math.random() * RANDOM_CEIL);
}

function getList() {
    return document.getElementById('when-list');
}

function newItem(createCallback) {
    const list = getList();
    list.appendChild(createCallback(getRandomInt(), list));
}


export function fetchWhen() {
    const when = [...fetchSingleTimeItem(), ...fetchRepeatedTimeItem()];

    if (when.length === 0)
        throw new Error('Must select WHEN to target!');

    return when;
}

export async function loadWhen(restrictions) {
    document.getElementById('new-single-time-item').onclick = () => newItem(createSingleTimeItem);
    document.getElementById('new-repeated-time-item').onclick = () => newItem(createRepeatedTimeItem);

    if (restrictions) {
        const list = getList();

        restrictions.filter(restriction => restriction.type === 'single')
            .forEach(restriction => list.appendChild(createSingleTimeItem(getRandomInt(), list, restriction.value)));

        restrictions.filter(restriction => restriction.type === 'repeated')
            .forEach(restriction => list.appendChild(createRepeatedTimeItem(getRandomInt(), list, restriction.value)));
    }
}