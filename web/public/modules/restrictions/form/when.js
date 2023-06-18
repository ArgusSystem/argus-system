import { createSingleTimeItem } from './components/single_time_item.js';
import { createRepeatedTimeItem } from './components/repeated_time_item.js';

const RANDOM_CEIL = 1_000_000;
function getRandomInt() {
    return Math.floor(Math.random() * RANDOM_CEIL);
}

function getList() {
    return document.getElementById('when-list');
}

function newSingleItem() {
    getList().appendChild(createSingleTimeItem(getRandomInt()));
}

function newRepeatedItem() {
    getList().appendChild(createRepeatedTimeItem(getRandomInt()));
}


export async function loadWhen() {
    document.getElementById('new-single-time-item').onclick = newSingleItem;
    document.getElementById('new-repeated-time-item').onclick = newRepeatedItem;
}