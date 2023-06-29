import { createAlbumIcon, createAddIcon } from './icons.js';
import { API_URL } from '../modules/api/url.js'
import {
    createTableHeader,
    mapChildrenToRow,
    createTextNode,
    createInputTextNode,
    createInputDropdownNode,
    createDeleteButton,
    createSaveButton,
    fetchHTMLElement
} from "./utils.js";
import { getPersonPhotoURL } from '../modules/api/people.js';

async function createPersonRow(){
    return await fetchHTMLElement('components/table_rows/person.html');
}

export async function createPersonHeader() {
    return createTableHeader(await createPersonRow(), "Id", "Name", "Role", "Created At",
        "Photos", "Add Photos", "Save", "Delete");
}

function createSlideshowItem(person, photo) {
    const item = document.createElement('div');
    item.setAttribute('class', 'carousel-item');

    const img = document.createElement('img');
    img.setAttribute('src', getPersonPhotoURL(person.id, photo));
    img.setAttribute('alt', person.text);
    img.setAttribute('class', 'm-auto w-auto d-block');

    item.appendChild(img);

    return item;
}

function populateSlideshow(person) {
    const slideshow = document.querySelector('.carousel-inner');
    slideshow.replaceChildren();

    for (const photo of person.photos) {
        slideshow.appendChild(createSlideshowItem(person, photo));
    }

    slideshow.firstElementChild.classList.add('active');
}

function createAlbumButton(person, icon) {
    let button = document.createElement('button');

    button.setAttribute('class', 'btn m-0 p-0');
    button.setAttribute('type', 'button');
    button.setAttribute('data-bs-toggle', 'modal');
    button.setAttribute('data-bs-target', '#slideshowModal');
    button.onclick = () => populateSlideshow(person);
    button.appendChild(icon);

    return button;
}

export function train_model_button() {
    fetch(`${API_URL}/people/train`, { method: 'POST' })
}

function is_image_file(filename) {
    const idxDot = filename.lastIndexOf(".") + 1;
    const extFile = filename.substr(idxDot, filename.length).toLowerCase();
    return extFile === "jpg" || extFile === "jpeg" || extFile === "png";
}

function uploadPhoto(person_id) {
    let input = document.createElement('input');
    input.type = 'file';
    //input.accept = 'image/*';
    input.accept = '.jpg, .png, .jpeg';
    input.multiple = true;

    input.onchange = _ => {

        // create request
        const formdata = new FormData();
        if (person_id === -1) {
            formdata.append("name", document.getElementById("person_name_input").value);
        }

        // add all photos to request
        let files =   Array.from(input.files);
        console.log(files);
        for (let i = 0; i < files.length; ++i) {
            let file = files[i];
            // check that file extension is allowed
            if (!is_image_file(file.name)) {
                alert(`Only images allowed. Ignoring '${file.name}'`);
            }
            else {
                formdata.append("photo" + i, file);
            }
        }
        console.log(formdata);
        // send request
        fetch(`${API_URL}/people/${person_id}/photos`, {
            method: 'POST',
            body: formdata
        }).then((response) => {
            if (response.ok) {
                window.location.reload()
            }
            return response.blob();
        });
    };
    input.click();
}

function createUploadPhotoButton(person, icon) {
    let button = document.createElement('button');

    button.setAttribute('class', 'btn m-0 p-0');
    button.setAttribute('type', 'button');

    button.onclick = () => uploadPhoto(person);
    button.appendChild(icon);

    return button;
}

function _delete(row) {
    let id = row.querySelector('.person-id').innerHTML;
    fetch(`${API_URL}/people/${id}`, { method: 'DELETE' }).then(async (response) => {
        if (!response.ok) {
            alert("Person is still in use, DELETE failed");
        }
        else{
            // row.parentNode.removeChild(row);
            window.location.reload()
        }
    });
}

function _save(row) {
    let id = row.querySelector('.person-id').innerHTML;
    let name = row.querySelector('.person-name').querySelector('input#person_name_input').value;
    let role = (row.querySelector('.person-role').querySelector('select#person_role_input').value).split('-')[0];
    //console.log("save: ", id, name, role);
    fetch(`${API_URL}/people/${id}/${name}/${role}`, { method: 'POST' }).then((response) => {
        response.json().then(async (body) => {
            if (response.ok && id === '-1') {
                window.location.reload()
            }
        });
    });
}

export async function createPersonItem(person, roles) {
    const albumIcon = await createAlbumIcon();
    const addIcon = await createAddIcon();

    const row = await createPersonRow();

    mapChildrenToRow(row,
        createTextNode(person['id']),
        createInputTextNode("person_name_input", "", person['name']),
        createInputDropdownNode("person_role_input", roles, person['role']),
        createTextNode(person['created_at']),
        createAlbumButton(person, albumIcon),
        createUploadPhotoButton(person.id, addIcon),
        await createSaveButton(row, _save),
        await createDeleteButton(row, _delete));

    return row;
}

export async function createNewPersonItem(roles) {
    const addIcon = await createAddIcon();

    const row = await createPersonRow();

    mapChildrenToRow(row,
        createTextNode('-1'),
        createInputTextNode("person_name_input", '*new person name*'),
        createInputDropdownNode("person_role_input", roles),
        createTextNode('-'),
        createTextNode('-'),
        // createUploadPhotoButton(-1, addIcon),
        createTextNode('-'),
        await createSaveButton(row, _save),
        await createDeleteButton(row, _delete));

    return row;
}