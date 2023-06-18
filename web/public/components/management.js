export function createRemoveButton(callback) {
    const button = document.createElement('button');
    button.setAttribute('type', 'button');
    button.setAttribute('class', 'btn btn-sm btn-danger');
    button.onclick = callback;

    const i = document.createElement('i');
    i.setAttribute('class', 'fa fa-trash')

    button.appendChild(i);

    return button;
}