import { API_URL } from './url.js';

export function getFaceImageUrl(imgKey) {
    return `${API_URL}/faces/${imgKey}`;
}
