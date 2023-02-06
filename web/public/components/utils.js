import {createDeleteIcon, createSaveIcon} from "./icons.js";

const PARSER = new DOMParser();

export function fetchHTMLElement(url) {
    return fetch(url)
        .then(data => data.text())
        .then(html => PARSER.parseFromString(html, 'text/html').body.firstElementChild);
}

function createButton(icon, func, params) {
    let button = document.createElement('button');

    button.setAttribute('class', 'btn m-0 p-0');
    button.setAttribute('type', 'button');

    button.onclick = () => func(params);
    button.appendChild(icon);

    return button;
}

export async function createDeleteButton(id, delete_function) {
    return createButton(await createDeleteIcon(), delete_function, id);
}

export async function createSaveButton(id, save_function) {
    return createButton(await createSaveIcon(), save_function, id);
}

export function createTextNode(text){
    return document.createTextNode(text);
}

export function createInputTextNode(id, placeholder) {
    let text_input = document.createElement("input");
    text_input.setAttribute('type', 'text');
    text_input.setAttribute('id', id);
    text_input.setAttribute('placeholder', placeholder);
    return text_input;
}

export function mapChildrenToRow(row, ...children) {
    //console.log(row);
    let nodes = row.querySelectorAll('*');
    //console.log(nodes);
    //console.log(children);
    for (let i = 1; i < nodes.length; ++i) {
        //console.log(children[i-1]);
        nodes[i].appendChild(children[i-1]);
    }
    return row;
}

export function createTableHeader(row, ...fields) {
    row.classList.add('text-bg-secondary');
    let nodes = [];
    for (let field of fields){
        nodes.push(createTextNode(field));
    }
    return mapChildrenToRow(row, ...nodes);
}