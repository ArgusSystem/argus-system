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

    socketClient.onVideoChunk((chunk) => {
      videoBuffer.append(chunk);

      if (video.paused) {
        video.play();
      }
    });
  })
})

