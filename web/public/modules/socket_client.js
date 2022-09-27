export class SocketClient {
  constructor () {
    this.client = io.connect('http://localhost:8080/video', { forceNew: true })

    this.client.on('metadata', (data) => {
      const canvas = document.getElementById('video-canvas')
      canvas.width = data.video.width
      canvas.height = data.video.height
    })

    console.log("Connected to web server!")
  }

  onChunk (callback) {
    this.client.on('chunk', callback)
  }

  onAnalysis (callback) {
    this.client.on('analysis', callback)
  }
}
