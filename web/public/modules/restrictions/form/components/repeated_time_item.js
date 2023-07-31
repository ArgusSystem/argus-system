import { createInput, createLabel, createListItem, FROM, TO } from './utils.js';
import { createRemoveButton } from '../../../../components/management.js';
import { daytimeToString } from '../../../format.js';

const TIME = 'time';
const CHECKBOX = 'checkbox';
const LABEL_CLASS = 'h6 px-3'
const CHECKBOX_LABEL_CLASS = 'btn btn-outline-primary mx-1';
const ID_CLASS = 'repeated-time-item'

const SHORT_DAYS = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'];

// DO NOT COPY THIS
function createSpace() {
    const span = document.createElement('span');
    span.setAttribute('class', 'mx-3');
    return span;
}

function createCheckboxInput(id, type) {
    const input = createInput(id, type);
    input.setAttribute('class', 'btn-check');
    input.setAttribute('autocomplete', 'off');
    return input;
}

export function createRepeatedTimeItem(idSalt, parentNode, restriction) {
    const li = createListItem(ID_CLASS);

    li.appendChild(createRemoveButton(() => parentNode.removeChild(li)));

    const startTimeId = `start-time-${idSalt}`;
    li.appendChild(createLabel(startTimeId, FROM, LABEL_CLASS));
    const inputStartTime = createInput(startTimeId, TIME);
    li.appendChild(inputStartTime);

    const endTimeId = `end-time-${idSalt}`;
    li.appendChild(createLabel(endTimeId, TO, LABEL_CLASS));
    const inputEndTime = createInput(endTimeId, TIME);
    li.appendChild(inputEndTime);

    if (restriction) {
        inputStartTime.value = daytimeToString(restriction.start_time);
        inputEndTime.value = daytimeToString(restriction.end_time);
    }

    li.appendChild(createSpace());

    for (const [i, day] of SHORT_DAYS.entries()) {
        const dayId = `${day}-${idSalt}`;
        const inputDay = createCheckboxInput(dayId, CHECKBOX);
        li.appendChild(inputDay);
        li.appendChild(createLabel(dayId, day, CHECKBOX_LABEL_CLASS));

        if (restriction)
            inputDay.checked = restriction.days.some(d => d === LONG_DAYS[i]);
    }

    return li;
}

function toDaytime(time) {
    if (time === '')
        throw new Error('Invalid daytime(s)!');

    const [hours, minutes] = time.split(':');
    return hours * 3600 + minutes * 60;
}

const LONG_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

function toDayList(days) {
    const selectedDays = LONG_DAYS.filter((_, index) => days.item(index).checked);

    if (selectedDays.length === 0)
        throw new Error('No day selected!');

    return selectedDays;
}

export function fetchRepeatedTimeItem() {
    const items = [];

    document.querySelectorAll(`.${ID_CLASS}`).forEach(element => {
        const times = element.querySelectorAll(`input[type=${TIME}]`);
        const days = element.querySelectorAll(`input[type=${CHECKBOX}]`);

        items.push({
            type: 'repeated',
            value: {
                start_time: toDaytime(times.item(0).value),
                end_time: toDaytime(times.item(1).value),
                days: toDayList(days),
                time_zone: Intl.DateTimeFormat().resolvedOptions().timeZone
            }
        });
    });

    return items;
}