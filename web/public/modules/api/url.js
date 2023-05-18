const {protocol, hostname} = window.location;

export const API_URL = `${protocol}//${hostname}:5000`;

export function with_params(url, params) {
    const endpoint = new URL(url);
	endpoint.search = new URLSearchParams(params).toString();
    return endpoint;
}
