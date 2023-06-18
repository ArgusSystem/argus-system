import { createInput, createLabel, createListItem, FROM, TO } from './utils.js';

const TIME = 'time';
const CHECKBOX = 'checkbox';
const LABEL_CLASS = 'h6 px-3'
const CHECKBOX_LABEL_CLASS = 'btn btn-outline-primary mx-1';

const DAYS = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'];

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

export function createRepeatedTimeItem(id_salt) {
  const li = createListItem();

  const startTimeId = `start-time-${id_salt}`;
  li.appendChild(createLabel(startTimeId, FROM, LABEL_CLASS));
  li.appendChild(createInput(startTimeId, TIME));

  const endTimeId = `end-time-${id_salt}`;
  li.appendChild(createLabel(endTimeId, TO, LABEL_CLASS));
  li.appendChild(createInput(endTimeId, TIME));

  li.appendChild(createSpace());

  for (const day of DAYS) {
      const dayId = `${day}-${id_salt}`;
      li.appendChild(createCheckboxInput(dayId, CHECKBOX));
      li.appendChild(createLabel(dayId, day, CHECKBOX_LABEL_CLASS));
  }

  return li;
}