const DEFAULT_ZOOM = 17;

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

        this.map.setView([-34.60331220075804, -58.3805567750609], DEFAULT_ZOOM);

        this.markers = {};
        this.activeMarker = null;
    }

    init() {
        const map = this.map;

        for (const marker of Object.values(this.markers)) {
            this.map.removeLayer(marker);
        }

        this.markers = {}
        this.activeMarker = null;
        setTimeout(() => { map.invalidateSize() }, 100);
    }

    addMarker(camera) {
        if (!(camera.id in this.markers)) {
            const coordinates = [camera.latitude, camera.longitude];

            const marker = L.marker([camera.latitude, camera.longitude], {opacity: 0.5});

            // First marker
            if (this.activeMarker === null) {
                marker.setOpacity( 1.0);
                this.map.setView(coordinates, DEFAULT_ZOOM);
                this.activeMarker = marker;
            }

            this.map.addLayer(marker);

            this.markers[camera.id] = marker;
        }
    }

    focus(camera_id) {
        this.activeMarker.setOpacity(0.5);

        const marker = this.markers[camera_id];

        this.map.panTo(marker.getLatLng(), DEFAULT_ZOOM);
        marker.setOpacity( 1.0);

        this.activeMarker = marker;
    }
}
