const {protocol, hostname} = window.location;

export function fetchCameras() {
	return fetch(`${protocol}//${hostname}:5000/camera`)
		.then((response) => response.json())
		.catch((error) => console.error('Failed to fetch people!', error));
}
