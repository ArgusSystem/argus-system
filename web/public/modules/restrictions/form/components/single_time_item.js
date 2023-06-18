import { createInput, createLabel, createListItem, FROM, TO, toTimestamp } from './utils.js';
import { createRemoveButton } from '../../../../components/management.js';
import { timestampToISOString } from '../../../format.js';


const START_DATE = 'start-date';
const END_DATE = 'end-date';

const DATETIME_LOCAL = 'datetime-local';
const LABEL_CLASS = 'h6 px-3';
const ID_CLASS = 'single-time-item';

export function createSingleTimeItem(idSalt, parentNode, restriction) {
    const li = createListItem(ID_CLASS);

    li.appendChild(createRemoveButton(() => parentNode.removeChild(li)));

    const startDateId = `${START_DATE}-${idSalt}`;
    li.appendChild(createLabel(startDateId, FROM, LABEL_CLASS));
    const inputStartDate = createInput(startDateId, DATETIME_LOCAL);
    li.appendChild(inputStartDate);

    const endDateId = `${END_DATE}-${idSalt}`;
    li.appendChild(createLabel(endDateId, TO, LABEL_CLASS));
    const inputEndDate = createInput(endDateId, DATETIME_LOCAL);
    li.appendChild(inputEndDate);

    if (restriction) {
        inputStartDate.value = timestampToISOString(restriction.start_time);
        inputEndDate.value = timestampToISOString(restriction.end_time);
    }

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