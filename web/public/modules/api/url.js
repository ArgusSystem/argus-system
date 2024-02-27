// NOTE: this forces that both the page and REST API use the same protocol (http or https)
const {protocol} = window.location;

const HOST = 'argus-web';

export const API_URL = `${protocol}//${HOST}:5000`;


export function with_params(url, params) {
    const endpoint = new URL(url);
	endpoint.search = new URLSearchParams(params).toString();
    return endpoint;
}
