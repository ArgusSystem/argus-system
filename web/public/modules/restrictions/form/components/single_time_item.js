import { createInput, createLabel, createListItem, FROM, TO } from './utils.js';


const DATETIME_LOCAL = 'datetime-local';
const LABEL_CLASS = 'h6 px-3'

export function createSingleTimeItem(id_salt) {
  const li = createListItem();

  const startDateId = `start-date-${id_salt}`;
  li.appendChild(createLabel(startDateId, FROM, LABEL_CLASS));
  li.appendChild(createInput(startDateId, DATETIME_LOCAL));

  const endDateId = `end-date-${id_salt}`;
  li.appendChild(createLabel(endDateId, TO, LABEL_CLASS));
  li.appendChild(createInput(endDateId, DATETIME_LOCAL));

  return li;
}