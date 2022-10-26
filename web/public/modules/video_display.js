export function setUpDisplay(videoInterpolator) {
    const video = document.getElementById('auxiliary-video');
    const canvas = document.getElementById('video-canvas');
    const ctx = canvas.getContext('2d');

    canvas.width = 1920;
    canvas.height = 1080;
    let frame_count = 0;

    const updateCanvas = (now, metadata) => {
        frame_count += 1;

        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw video feed
        ctx.drawImage(video, 0, 0);

        // Get faces for the time
        for (const face_data of videoInterpolator.getFaces(metadata.mediaTime)) {
            // Define rectangle points, width and height
            let x1 = face_data.boundingBox[0];
            let y1 = face_data.boundingBox[1];
            let x2 = face_data.boundingBox[2];
            let y2 = face_data.boundingBox[3];
            let w = x2 - x1;
            let h = y2 - y1;

            // Write face name over rectangle
            ctx.font = "20px Arial";
            ctx.fillStyle = 'green';
            ctx.fillText(`${face_data.name}, ${face_data.probability.toFixed(2)}`, x1, y1 - 10);

            // Draw face rectangle
            ctx.beginPath();
            ctx.rect(x1, y1, w, h);
            ctx.fillStyle = "rgba(0,0,0,0)";
            ctx.fill();
            ctx.lineWidth = 5;
            ctx.strokeStyle = 'green';
            ctx.stroke();
        }

        video.requestVideoFrameCallback(updateCanvas);
    };

    video.requestVideoFrameCallback(updateCanvas);

    let previous_frame_count = 0;

    setInterval(() => {
        const current_frame_count = frame_count;
        console.log('FPS: %d', current_frame_count - previous_frame_count);
        previous_frame_count = current_frame_count;
    },1000);
}

