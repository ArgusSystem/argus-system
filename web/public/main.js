import { SocketClient } from './modules/socket_client.js'
import { setUpDisplay } from './modules/video_display.js'
import { VideoBuffer } from './modules/video_buffer.js'


window.addEventListener('load', () => {
  const socketClient = new SocketClient();
  const mediaSource = new MediaSource;

  const video = document.getElementById('auxiliary-video');
  video.src = URL.createObjectURL(mediaSource);

  mediaSource.addEventListener('sourceopen', (e) => {
    setUpDisplay();

    const videoBuffer = new VideoBuffer(mediaSource);
    let preBuffer = 0;
    socketClient.onVideoChunk((chunk) => {
      videoBuffer.append(chunk);
      preBuffer += 1;
      if (preBuffer >= 3) {
        if (video.paused) {
          video.play();
        }
      }
    });
  })
})

