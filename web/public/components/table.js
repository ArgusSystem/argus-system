const COL = 'col';
const ROW = 'row';

const ACTIVE = 'table-active';

function tr() {
    return document.createElement('tr');
}

function th(text, scope) {
    const th = document.createElement('th');
    th.setAttribute('scope', scope);
    th.innerText = text;
    return th;
}

function td(text) {
    const td = document.createElement('td');
    td.innerText = text;
    return td;
}

export function createHeader(table, headers) {
    const thead = table.querySelector('thead');

    const row = tr();
    thead.appendChild(row);

    headers.forEach(header => row.appendChild(th(header, COL)));

    return row;
}

export function createRow(table, header, columns) {
    const tbody = table.querySelector('tbody');

    const row = tr();
    tbody.appendChild(row);

    row.appendChild(th(header, ROW));
    columns.forEach(column => row.appendChild(td(column)));

    return row;
}

export function clearBody(table) {
    table.querySelector('tbody').replaceChildren();
}

export function setActiveRow(table, row) {
    table.querySelectorAll(`.${ACTIVE}`).forEach(element => element.classList.remove(ACTIVE));
    row.classList.add(ACTIVE);
}