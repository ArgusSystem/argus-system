export const FROM = 'From:';
export const TO = 'To:';

export function createLabel(id, text, klass) {
    const label = document.createElement('label');
    label.setAttribute('class', klass);
    label.setAttribute('for', id);
    label.innerText = text;
    return label;
}

export function createInput(id, type) {
  const input = document.createElement('input');
  input.setAttribute('id', id);
  input.setAttribute('type', type);
  input.setAttribute('name', id);
  return input;
}

export function createListItem(klass) {
  const li = document.createElement('li');
  li.setAttribute('class', `list-group-item ${klass}`);
  return li;
}
