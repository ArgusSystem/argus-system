import { fetchPeople } from '../api/people.js';
import { reTagFaces } from '../api/unknown_clusters.js';

function getSelectedFaces() {
    const faces = [];

    document.getElementById('face-grid')
        .querySelectorAll('input[type=checkbox]:checked')
        .forEach(e => faces.push(e.value));

    return faces;
}

async function reTag(clusterId, person) {
    await reTagFaces(clusterId, person.id, getSelectedFaces());
}
function createDropdownOption(element, clusterId, person) {
    const li = document.createElement('li');
    li.classList.add('dropdown-item')
    li.innerText = person.name;
    li.onclick = async () => await reTag(clusterId, person);
    element.appendChild(li);
}

function getFaceGridCheckboxes() {
    return document.getElementById('face-grid').querySelectorAll('input[type=checkbox]');
}

export async function loadReTaggingOptions(clusterId) {
    document.getElementById('select-all-faces').onclick = () => getFaceGridCheckboxes()
         .forEach(e => e.checked = true);

    document.getElementById('clear-faces').onclick = () => getFaceGridCheckboxes()
         .forEach(e => e.checked = false);

    const optionList = document.getElementById('tagging-options');
    (await fetchPeople()).forEach(person => createDropdownOption(optionList, clusterId, person));
}
