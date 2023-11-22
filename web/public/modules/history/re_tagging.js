import { fetchPeople } from '../api/people.js';
import { redirect, reload } from '../routing.js';
import { Page } from '../page.js';
import {post} from "../api/utils.js";
import {API_URL} from "../api/url.js";

const PERSON_ID_UNKNOWN = -1;
const PERSON_ID_DELETE = -2;

function getSelectedFaces() {
    const faces = [];

    document.getElementById('face-grid')
        .querySelectorAll('input[type=checkbox]:checked')
        .forEach(e => faces.push(e.value));

    return faces;
}

function getFacesCount() {
    return document.getElementById('face-grid').querySelectorAll('input[type=checkbox]').length;
}

async function reTag(person_id) {
    const selectedFaces = getSelectedFaces();
    await reTagFaces(person_id, selectedFaces);
    return selectedFaces.length;
}

export function reTagFaces(person, faces) {
	return post(`${API_URL}/known_faces/re_tag`, {person, faces})
			.catch((error) => console.error('Failed to re tag faces!', error));
}

function createDropdownOption(element, option_text, option_value) {
    const li = document.createElement('li');
    li.classList.add('dropdown-item');
    li.innerText = option_text;
    li.onclick = async () => {
        const facesUpdated = await reTag(option_value);
        reload();
        //$('#faces-modal').modal('hide');
    };
    element.appendChild(li);
}

function getFaceGridCheckboxes() {
    return document.getElementById('face-grid').querySelectorAll('input[type=checkbox]');
}

export async function loadReTaggingOptions() {
    document.getElementById('select-all-faces').onclick = () => getFaceGridCheckboxes()
         .forEach(e => e.checked = true);

    document.getElementById('clear-faces').onclick = () => getFaceGridCheckboxes()
         .forEach(e => e.checked = false);

    const optionList = document.getElementById('tagging-options');
    while (optionList.firstChild) {
        optionList.removeChild(optionList.firstChild);
    }
    (await fetchPeople()).forEach(person => createDropdownOption(optionList, person.name, person.id));
    createDropdownOption(optionList, "--unknown--", PERSON_ID_UNKNOWN);
    createDropdownOption(optionList, "--delete--", PERSON_ID_DELETE);
}
