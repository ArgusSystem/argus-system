const {protocol, hostname, port} = window.location;

export const API_URL = `${protocol}//${hostname}:5000`;
export const MAIN_URL = `${protocol}//${hostname}:${port}`;