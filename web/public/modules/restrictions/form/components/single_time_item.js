import { createInput, createLabel, createListItem, FROM, TO, toTimestamp } from './utils.js';


const START_DATE = 'start-date';
const END_DATE = 'end-date';

const DATETIME_LOCAL = 'datetime-local';
const LABEL_CLASS = 'h6 px-3';
const ID_CLASS = 'single-time-item';

export function createSingleTimeItem(id_salt) {
    const li = createListItem(ID_CLASS);

    const startDateId = `${START_DATE}-${id_salt}`;
    li.appendChild(createLabel(startDateId, FROM, LABEL_CLASS));
    li.appendChild(createInput(startDateId, DATETIME_LOCAL));

    const endDateId = `${END_DATE}-${id_salt}`;
    li.appendChild(createLabel(endDateId, TO, LABEL_CLASS));
    li.appendChild(createInput(endDateId, DATETIME_LOCAL));

    return li;
}

function validateTimestamp(timestamp) {
    if (isNaN(timestamp))
        throw new Error('Invalid date(s)!');

    return timestamp;
}

export function fetchSingleTimeItem() {
    const items = [];

    document.querySelectorAll(`.${ID_CLASS}`).forEach(element => {
        const dates = element.querySelectorAll('input');

        items.push({
            type: 'single',
            value: {
                start_time: validateTimestamp(toTimestamp(dates.item(0).value)),
                end_time: validateTimestamp(toTimestamp(dates.item(1).value))
            }
        });
    });

    return items;
}