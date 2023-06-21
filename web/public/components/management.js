function createButton(callback, btnClass, iconClass) {
    const button = document.createElement('button');
    button.setAttribute('type', 'button');
    button.setAttribute('class', `btn btn-sm ${btnClass} mx-1`);
    button.onclick = callback;

    const i = document.createElement('i');
    i.setAttribute('class', `fa ${iconClass}`);

    button.appendChild(i);

    return button;
}

export function createRemoveButton(callback) {
    return createButton(callback, 'btn-outline-danger', 'fa-trash');
}

export function createUpdateButton(callback) {
    return createButton(callback, 'btn-outline-success', 'fa-edit');
}