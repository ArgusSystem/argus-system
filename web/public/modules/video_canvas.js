export class VideoCanvas {
  constructor (videoIndex) {
    this.videoIndex = videoIndex
    this.frameOffset = 0

    const video = document.getElementById('auxiliary-video')

    this.canvas = document.getElementById('video-canvas')
    const ctx = this.canvas.getContext('2d')

    const self = this

    const updateCanvas = (now, metadata) => {
      console.log(self.frameOffset)
      ctx.drawImage(video, 0, 0)

      const boxes = self.videoIndex.getBoxes(this.frameOffset)

      if (boxes != null) {
        boxes.forEach((box) => {
          // Create rectangle box
          ctx.beginPath()
          ctx.lineWidth = 4
          ctx.strokeStyle = box.isMatch ? 'green' : 'red'
          ctx.rect(box.x, box.y, box.width, box.height)
          ctx.stroke()

          // Add person description if needed
          if (box.isMatch) {
            ctx.font = '14px verdana'
            ctx.textAlign = 'center'
            ctx.fillText(`${box.name} (${box.probability.toFixed(2)}%)`,
              // x coordinate is the the middle of the box
              box.x + Math.floor(box.width / 2),
              // y coordinate is 10 pixels below the box
              box.y + box.height + 10,
              // max width is the box width
              box.width)
          }
        })
      }

      self.frameOffset += 1
      video.requestVideoFrameCallback(updateCanvas)
    }

    video.requestVideoFrameCallback(updateCanvas)
  }

  updateToChunk (chunkId) {
    console.log("Update to chunk triggered")
    this.frameOffset = this.videoIndex.getFrameOffset(chunkId)
  }
}
