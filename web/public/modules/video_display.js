export function setUpDisplay(videoBuffer, facesData) {
    const video = document.getElementById('auxiliary-video');
    const canvas = document.getElementById('video-canvas');
    // TODO: Shouldn't be hardcoded
    canvas.width = 1920;
    canvas.height = 1080;
    const ctx = canvas.getContext('2d');
    let frame_counter = 0;

    const updateCanvas = (now, metadata) => {

        // draw video feed
        ctx.drawImage(video, 0, 0);

        // get current chunk id and face data
        let [chunk_id, offset] = videoBuffer.currentChunk(metadata.mediaTime);
        let frame_faces = facesData.currentFaceData(chunk_id, offset);

        if (frame_faces == null) {
            console.log("didn't find face data for chunk: " + chunk_id.toString() + ", offset: " + offset.toString());
        }
        else {
            for (const face_data of frame_faces) {
                // define rectangle points, width and height
                let x1 = face_data.bounding_box[0];
                let y1 = face_data.bounding_box[1];
                let x2 = face_data.bounding_box[2];
                let y2 = face_data.bounding_box[3];
                let w = x2 - x1;
                let h = y2 - y1;

                // write face name over rectangle
                ctx.font = "20px Arial";
                ctx.fillStyle = 'red';
                ctx.fillText(`${face_data.name}, ${face_data.probability.toFixed(2)}`, x1, y1 - 10);

                // draw face rectangle
                // console.log("drawing face rect")
                ctx.beginPath();
                // console.log(`x1: ${x1}, y1: ${y1}, x2: ${x2}, y2: ${y2}`)
                ctx.rect(x1, y1, w, h);
                ctx.fillStyle = "rgba(0,0,0,0)";
                ctx.fill();
                ctx.lineWidth = 5;
                ctx.strokeStyle = 'red';
                ctx.stroke();

                //console.log(metadata)
            }
        }


        video.requestVideoFrameCallback(updateCanvas);
    };

    video.requestVideoFrameCallback(updateCanvas);
}

