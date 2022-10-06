export function setUpDisplay(faceData) {
  const video = document.getElementById('auxiliary-video');
  const canvas = document.getElementById('video-canvas');
  // TODO: Shouldn't be hardcoded
  canvas.width = 1920;
  canvas.height = 1080;
  const ctx = canvas.getContext('2d');

  const updateCanvas = (now, metadata) => {
    // clear canvas
    //context.clearRect(0, 0, canvas.width, canvas.height);

    // draw video feed
    ctx.drawImage(video, 0, 0);

    if (faceData.initialized) {
      let x1 = faceData.bounding_box[0];
      let y1 = faceData.bounding_box[1];
      let x2 = faceData.bounding_box[2];
      let y2 = faceData.bounding_box[3];
      let w = x2 - x1;
      let h = y2 - y1;

      ctx.font = "20px Arial";
      ctx.fillStyle = 'red';
      ctx.fillText(`${faceData.name}, ${faceData.probability.toFixed(2)}`, x1, y1 - 10);

      // console.log("drawing face rect")
      ctx.beginPath();
      // console.log(`x1: ${x1}, y1: ${y1}, x2: ${x2}, y2: ${y2}`)
      ctx.rect(x1, y1, w, h);
      ctx.fillStyle = "rgba(0,0,0,0)";
      ctx.fill();
      ctx.lineWidth = 5;
      ctx.strokeStyle = 'red';
      ctx.stroke();
    }

    video.requestVideoFrameCallback(updateCanvas);
  }

  video.requestVideoFrameCallback(updateCanvas);
}

