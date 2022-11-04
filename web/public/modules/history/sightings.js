function createSightingItem(cameras, sighting) {
    const item = document.createElement('li');
    item.setAttribute('class', 'list-group-item');

    const start_time = new Date(sighting.start_time).toLocaleString();
    const end_time = new Date(sighting.end_time).toLocaleString();
    const sightingText = `${cameras[sighting.camera_id].name} (${start_time} - ${end_time})`;
    item.appendChild(document.createTextNode(sightingText));

    return item;
}

export function onSightings(cameras, sightings) {
    document.getElementById('sightings').removeAttribute('hidden');
    const list = document.getElementById('sightings-list');

    sightings.forEach(sighting => {
        list.appendChild(createSightingItem(cameras, sighting));
    });
}