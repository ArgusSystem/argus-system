import {
    createTextNode,
    createDeleteButton,
    createSaveButton,
    mapChildrenToRow,
    createTableHeader,
    fetchHTMLElement,
    createInputTextNode
} from "./utils.js";

async function createCameraRow(){
    return await fetchHTMLElement('components/table_rows/camera.html');
}

export async function createCamerasHeader() {
    return createTableHeader(await createCameraRow(), "Id", "Alias", "Area", "Lat.", "Long.", "Save", "Delete");
}

function _delete(id){
    return null;
}

function _save(id){
    return null;
}

export async function createCamerasItem(camera) {
    return mapChildrenToRow(await createCameraRow(),
        createTextNode(camera['id']),
        createTextNode(camera['alias']),
        createTextNode(camera['area']),
        createTextNode(camera['latitude']),
        createTextNode(camera['longitude']),
        createSaveButton(camera['id'], _save),
        createDeleteButton(camera['id'], _delete));
}

export async function createNewCameraItem() {
    return mapChildrenToRow(await createCameraRow(),
        createInputTextNode('camera_id_input', '-1'),
        createInputTextNode('camera_alias_input', '*new camera alias*'),
        createInputTextNode('camera_area_input', '*area*'),
        createInputTextNode('camera_latitude_input', '*latitude*'),
        createInputTextNode('camera_longitude_input', '*longitude*'),
        await createSaveButton(-1, _save),
        await createDeleteButton(-1, _delete));
}