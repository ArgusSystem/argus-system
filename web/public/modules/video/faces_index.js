export class FacesIndex {
    constructor () {
        this.faces = {};
    }

    add(face) {
        const chunkId = face.videoChunkId;
        const frameOffset = face.offset;

        const chunkFaces = (this.faces[chunkId] ||= {});
        const frameFaces = (chunkFaces[frameOffset] ||= []);
        frameFaces.push(face);
    }

    get(chunkId, frameOffset) {
        if (chunkId in this.faces) {
            const chunkFaces = this.faces[chunkId];

            if (frameOffset in chunkFaces) {
                return chunkFaces[frameOffset];
            }
        }

        return [];
    }

    remove(chunkId) {
        delete this.faces[chunkId];
    }
}