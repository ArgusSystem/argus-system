export function setUpDisplay() {
  const video = document.getElementById('auxiliary-video');
  const canvas = document.getElementById('video-canvas');
  // TODO: Shouldn't be hardcoded
  canvas.width = 1920;
  canvas.height = 1080;
  const ctx = canvas.getContext('2d');

  const updateCanvas = (now, metadata) => {
    ctx.drawImage(video, 0, 0);
    video.requestVideoFrameCallback(updateCanvas);
  }

  video.requestVideoFrameCallback(updateCanvas);
}

