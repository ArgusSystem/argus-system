const DEFAULT_ZOOM = 18;

// hardcodeo para coords de cuartos de demo casa gabo, en mapa de FIUBA
const FIUBA_COORDS = {
    kitchen: [
        // kitchen camera
        [-34.61759710915304, -58.3682885202042],
        // point between
        [-34.61795673382567, -58.36824226952407],
        // hallway camera
        [-34.61793573388762, -58.36794722208188]
    ],
    hallway: [
        // hallway camera
        [-34.61793573388762, -58.36794722208188],
        // bedroom end point
        [-34.61732279585517, -58.36799506761304]
    ],
    bedroom: [
        // bedroom camera
        [-34.61730835828806, -58.36774148629787],
        // bedroom end point
        [-34.61732279585517, -58.36799506761304]
    ],
    study: [
        // study camera
        [-34.61756692160962, -58.36772394293642],
        // study end point
        [-34.61757742162597, -58.36797433454955]
    ]
};

// hardcodeo para mapear camera ids a nombres
const FIUBA_AREAS = ['NONE', 'kitchen', 'hallway', 'study', 'bedroom'];

const COLOR_GREEN = '#00d500';
const COLOR_GRAY = '#7a7571';
const COLOR_LIGHT_GRAY = '#aaa29d';

export class Map {
    constructor () {
        const tileLayer =  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: false
        });

        this.map = L.map('map', {
            zoomControl: true,
            layers: [tileLayer],
            maxZoom: 18,
            minZoom: 6
        });

        this.map.setView(FIUBA_COORDS['kitchen'][0], DEFAULT_ZOOM);

        this.mapCorridors = null;
        this.drawMapCorridors(Object.values(FIUBA_COORDS));
        this.mapRooms = null;
        this.drawMapRooms(Object.values(FIUBA_COORDS));
        this.mapRoomLabels = [];
        this.drawMapRoomLabels(Object.keys(FIUBA_COORDS), Object.values(FIUBA_COORDS).map((coords) => coords[0]));

        this.markers = {};
        this.markersCenter = null;
        this.activeMarker = null;
        this.activeLine = null;
        this.activeRoom = null
    }

    init() {
        const map = this.map;

        for (const marker of Object.values(this.markers)) {
            this.map.removeLayer(marker);
        }

        this.markers = {};
        this.activeMarker = null;
        setTimeout(() => { map.invalidateSize() }, 100);
    }

    addMarker(camera, labels=[], opacity=0.5) {
        //console.log(camera);
        if (!(camera.id in this.markers)) {

            const marker = L.marker([camera.latitude, camera.longitude], {opacity: opacity});
            // First marker
            if (this.activeMarker === null) {
                //marker.setOpacity(1.0);
                this.activeMarker = marker;
            }
            this.map.addLayer(marker);

            // add popup with labels
            if (labels.length > 0) {
                const labelContainer = L.DomUtil.create('div', 'custom-label-container');
                labels.forEach((label, index) => {
                    const labelElement = L.DomUtil.create('div', 'custom-label', labelContainer);
                    labelElement.innerHTML = label;
                });
                const popup = marker.bindPopup(labelContainer, {className: 'custom-label-popup', closeButton: false});
            }

            this.markers[camera.id] = marker;

            this.markersCenter = calculateCenterPoint(Object.values(this.markers));
            this.map.setView(this.markersCenter, DEFAULT_ZOOM);
        }
    }

    // draws lines through each points list in point list
    drawMapCorridors(pointsLists, opacity=1, weight=8, color=COLOR_LIGHT_GRAY) {
        if (this.mapCorridors) {
            this.map.removeLayer(this.mapCorridors);
        }

        this.mapCorridors = L.layerGroup(pointsLists.map(coordinates => {
            return L.polyline(coordinates, { color: color, weight: weight, opacity: opacity });
        })).addTo(this.map);
    }

    // draws a room for each points list, cenetered on its first point
    // and align to its first two points
    drawMapRooms(pointsLists, fillOpacity=1, color=COLOR_GRAY) {
        if (this.mapRooms) {
            this.map.removeLayer(this.mapRooms);
        }

        this.mapRooms = L.layerGroup(pointsLists.map(coordinates => {
            return L.polygon(this.room_coordinates(coordinates), { color: color, fillColor: COLOR_LIGHT_GRAY, fillOpacity: fillOpacity });
        })).addTo(this.map);
    }

    drawMapRoomLabels(labels, points){
        for (let i = 0; i < labels.length; ++i) {
            const label = labels[i];
            const point = points[i];

            // Convert geographical coordinates to pixel coordinates
            const pixelCoordinates = this.map.latLngToContainerPoint([point[0], point[1]]);

            // Create a custom div for the text
            const customTextDiv = L.DomUtil.create('div', 'custom-text');
            customTextDiv.innerHTML = label;

            // Set the position using absolute positioning
            customTextDiv.style.position = 'absolute';
            customTextDiv.style.left = pixelCoordinates.x + 'px';
            customTextDiv.style.top = pixelCoordinates.y + 'px';

            customTextDiv.style.zIndex = 500; // Adjust the z-index as needed

            const self = this;

            function updateTextPosition() {
                const pixelCoordinates = self.map.latLngToContainerPoint([point[0], point[1]]);
                customTextDiv.style.left = pixelCoordinates.x + 'px';
                customTextDiv.style.top = pixelCoordinates.y + 'px';
            }

            this.map.on('move', updateTextPosition);

            // Add the custom div to the map container
            this.map.getContainer().appendChild(customTextDiv);
            this.mapRoomLabels.push(customTextDiv);
        }
    }

    focus(camera_id) {
        this.activeMarker.setOpacity(0.5);

        const marker = this.markers[camera_id];

        this.map.panTo(this.markersCenter, DEFAULT_ZOOM);
        marker.setOpacity(1.0);

        this.activeMarker = marker;

        // draws a green line from the camera position to the next point
        // marking its 'view line'
        if (this.activeLine){
            this.map.removeLayer(this.activeLine);
        }
        this.activeLine = L.polyline(this.camera_line_coordinates(camera_id), { color: COLOR_GREEN }).addTo(this.map);

        if (this.activeRoom){
            this.map.removeLayer(this.activeRoom);
        }
        this.activeRoom = L.polygon(this.room_coordinates(FIUBA_COORDS[FIUBA_AREAS[camera_id]]), { color: COLOR_GREEN, fillOpacity: 0.2, weight: 1 }).addTo(this.map);
    }

    camera_line_coordinates(camera_id) {
        const activeLine = FIUBA_COORDS[FIUBA_AREAS[camera_id]];
        return [activeLine[0], activeLine[1]];
    }

    // Returns vertices of a square centered on the first point
    // and aligned with the line from the first to the second point
    room_coordinates(pointsList, halfSideLength=0.0001) {
        const start_point = pointsList[0];
        const end_point = pointsList[1];

        // Calculate vector along the line from start_point to end_point
        const lineVector = [end_point[0] - start_point[0], end_point[1] - start_point[1]];

        // Calculate the length of the vector
        const vectorLength = Math.sqrt(lineVector[0] ** 2 + lineVector[1] ** 2);

        // Normalize the vector
        const normalizedVector = [lineVector[0] / vectorLength, lineVector[1] / vectorLength];

        // Calculate the normalized normal vector
        const normalizedNormalVector = [-normalizedVector[1], normalizedVector[0]];

        // Calculate the center of the square
        const squareCenter = start_point;

        // Calculate the displacement vectors along the normalized vector and normalized normal vector
        const displacementVector = [
            normalizedVector[0] * halfSideLength,
            normalizedVector[1] * halfSideLength
        ];
        const displacementNormalVector = [
            normalizedNormalVector[0] * halfSideLength,
            normalizedNormalVector[1] * halfSideLength
        ];

        // Define the vertices of the square
        return [
            [squareCenter[0] - displacementVector[0] - displacementNormalVector[0], squareCenter[1] - displacementVector[1] - displacementNormalVector[1]],
            [squareCenter[0] + displacementVector[0] - displacementNormalVector[0], squareCenter[1] + displacementVector[1] - displacementNormalVector[1]],
            [squareCenter[0] + displacementVector[0] + displacementNormalVector[0], squareCenter[1] + displacementVector[1] + displacementNormalVector[1]],
            [squareCenter[0] - displacementVector[0] + displacementNormalVector[0], squareCenter[1] - displacementVector[1] + displacementNormalVector[1]]
        ];
    }
}

function calculateCenterPoint(markers) {
    if (markers.length === 0) {
        return null;
    }

    let sumLat = 0;
    let sumLng = 0;

    markers.forEach(marker => {
        const position = marker.getLatLng();
        sumLat += position.lat;
        sumLng += position.lng;
    });

    const avgLat = sumLat / markers.length;
    const avgLng = sumLng / markers.length;

    return [avgLat, avgLng];
}