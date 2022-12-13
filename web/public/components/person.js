import { createPersonRow } from './person/row.js';
import { createAlbumIcon, createAddIcon } from './icons.js';
import { API_URL } from '../modules/api/url.js'

function mapTextToRow(row, nameCol, createdAtCol, lastSeenCol, photosCol, addPhotoCol) {
   row.querySelector('.person-name').appendChild(nameCol);
   row.querySelector('.person-created_at').appendChild(createdAtCol);
   row.querySelector('.person-last_seen').appendChild(lastSeenCol);
   row.querySelector('.person-photos').appendChild(photosCol);
   row.querySelector('.person-add_photo').appendChild(addPhotoCol);
}

export async function createPersonHeader() {
    const row = await createPersonRow();

    row.classList.add('text-bg-secondary');

    mapTextToRow(row,
        document.createTextNode('Name'),
        document.createTextNode('Created At'),
        document.createTextNode('Last Seen'),
        document.createTextNode('Photos'),
        document.createTextNode('Add Photos'));

    return row;
}

function createSlideshowItem(person, photo) {
    const item = document.createElement('div');
    item.setAttribute('class', 'carousel-item');

    const img = document.createElement('img');
    img.setAttribute('src', `${API_URL}/people/${person.id}/photos/${photo}`);
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

export async function createPersonItem(person) {
    const albumIcon = await createAlbumIcon();
    const addIcon = await createAddIcon();

    const row = await createPersonRow();

    mapTextToRow(row,
        document.createTextNode(person['text']),
        document.createTextNode(person['created_at']),
        document.createTextNode(person['last_seen'] || '-'),
        createAlbumButton(person, albumIcon),
        createUploadPhotoButton(person.id, addIcon));

    return row;
}

export async function createNewPersonItem() {
    const addIcon = await createAddIcon();
    const row = await createPersonRow();

    let person_name_input = document.createElement("input");
    person_name_input.setAttribute('type', 'text');
    person_name_input.setAttribute('id', 'person_name_input');
    person_name_input.setAttribute('placeholder', '*new person name*');

    mapTextToRow(row,
        person_name_input,
        document.createTextNode('-'),
        document.createTextNode('-'),
        document.createTextNode('-'),
        createUploadPhotoButton(-1, addIcon));

    return row;
}