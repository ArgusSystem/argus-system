export class FaceData {
    constructor () {
        this.detected_faces = {};
    }

    update(face) {
        if (!(face.video_chunk_id in this.detected_faces)) {
            this.detected_faces[face.video_chunk_id] = {};
        }
        if (!(face.offset in this.detected_faces[face.video_chunk_id])) {
            this.detected_faces[face.video_chunk_id][face.offset] = []
        }
        this.detected_faces[face.video_chunk_id][face.offset].push(face);
    }

    currentFaceData(video_chunk_id, offset) {
        if (video_chunk_id in this.detected_faces){
            if (offset in this.detected_faces[video_chunk_id]){
                return this.detected_faces[video_chunk_id][offset];
            }
        }
        return null
    }
}