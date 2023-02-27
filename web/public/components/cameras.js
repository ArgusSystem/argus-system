import {
    createTextNode,
    createDeleteButton,
    createSaveButton,
    mapChildrenToRow,
    createTableHeader,
    fetchHTMLElement,
    createInputTextNode
} from "./utils.js";
import { API_URL } from '../modules/api/url.js'
import {createInputDropdownNode} from "./utils.js";

async function createCameraRow(){
    return await fetchHTMLElement('components/table_rows/camera.html');
}

export async function createCamerasHeader() {
    return createTableHeader(await createCameraRow(), "Id", "Alias", "Mac", "Area", "Lat.", "Long.", "Save", "Delete");
}

function _delete(row){
    let id = row.querySelector('.camera-id').innerHTML;
    fetch(`${API_URL}/cameras/${id}`, { method: 'DELETE' }).then(async (response) => {
        if (!response.ok) {
            alert("Camera is still in use, DELETE failed");
        }
        else{
            // row.parentNode.removeChild(row);
            window.location.reload()
        }
    });
}

function _save(row){
    //console.log("save: ", row);
    let id = row.querySelector('.camera-id').innerHTML;
    let alias = row.querySelector('.camera-alias').querySelector('input#camera_alias_input').value;
    let mac = row.querySelector('.camera-mac').querySelector('input#camera_mac_input').value;
    let area = row.querySelector('.camera-area').querySelector('select#camera_area_input').value;
    let latitude = row.querySelector('.camera-latitude').querySelector('input#camera_latitude_input').value;
    let longitude = row.querySelector('.camera-longitude').querySelector('input#camera_longitude_input').value;
    // console.log("save: ", id, name, type);
    fetch(`${API_URL}/cameras/${id}/${alias}/${mac}/${area}/${latitude}/${longitude}`, { method: 'POST' }).then((response) => {
        response.json().then(async (body) => {
            if (response.ok && id === '-1') {
                window.location.reload()
            }
        });
    });
}

export async function createCamerasItem(camera, areas) {
    let row = await createCameraRow();
    return mapChildrenToRow(row,
        createTextNode(camera['id']),
        createInputTextNode('camera_alias_input', '', camera['name']),
        createInputTextNode('camera_mac_input', '', camera['mac']),
        createInputDropdownNode("camera_area_input", areas, camera['area']),
        createInputTextNode('camera_latitude_input', '', camera['latitude']),
        createInputTextNode('camera_longitude_input', '', camera['longitude']),
        await createSaveButton(row, _save),
        await createDeleteButton(row, _delete));
}

export async function createNewCameraItem(areas) {
    let row = await createCameraRow();
    return mapChildrenToRow(row,
        createTextNode('-1'),
        createInputTextNode('camera_alias_input', '*new camera alias*'),
        createInputTextNode('camera_mac_input', '*mac*'),
        createInputDropdownNode("camera_area_input", areas),
        createInputTextNode('camera_latitude_input', '*latitude*'),
        createInputTextNode('camera_longitude_input', '*longitude*'),
        await createSaveButton(row, _save),
        await createDeleteButton(row, _delete));
}