function getHeaderId(person) {
    return `header-${person.id}`;
}

function getCollapseId(person) {
    return `collapse-${person.id}`;
}

function getAccordionId() {
    return 'peopleList';
}

function createButton(person) {
    const button = document.createElement('button');
    const collapseId = getCollapseId(person);

    button.setAttribute('class', 'accordion-button collapsed');
    button.setAttribute('type', 'button');
    button.setAttribute('data-bs-toggle', 'collapse');
    button.setAttribute('data-bs-target', `#${collapseId}`);
    button.setAttribute('aria-expanded', 'false');
    button.setAttribute('aria-controls', collapseId);

    button.innerHTML = person.text;

    return button;
}

function createHeader(person) {
    const header = document.createElement('h2');
    header.setAttribute('id', getHeaderId(person));
    header.setAttribute('class', 'accordion-header');

    header.appendChild(createButton(person));

    return header;
}

function createCollapse(person) {
    const collapse = document.createElement('div');

    collapse.setAttribute('id', getCollapseId(person));
    collapse.setAttribute('class', 'accordion-collapse collapse');
    collapse.setAttribute('aria-labelledby', getHeaderId(person));
    collapse.setAttribute('data-bs-parent', getAccordionId());

    const body = document.createElement('div');
    body.setAttribute('class', 'accordion-body');
    body.innerHTML = person.id;

    collapse.appendChild(body);

    return collapse;
}

function createItem(person) {
    const item = document.createElement('div');
    item.setAttribute('class', 'accordion-item');

    item.appendChild(createHeader(person));
    item.appendChild(createCollapse(person));

    return item;
}

export function createAccordion(people) {
    const accordion = document.getElementById(getAccordionId());
    people.forEach(person => accordion.appendChild(createItem(person)));
}