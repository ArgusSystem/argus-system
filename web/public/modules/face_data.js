export class FaceData {
    constructor () {
        this.initialized = false
        this.video_chunk_id = null;
        this.offset = null;
        this.face_num = null;
        this.name = null;
        this.bounding_box = null;
        this.probability = null;
    }

    update(face) {
        this.initialized = true
        this.video_chunk_id = face.video_chunk_id;
        this.offset = face.offset;
        this.face_num = face.face_num;
        this.name = face.name;
        this.bounding_box = face.bounding_box;
        this.probability = face.probability;
    }
}