import { PriorityQueue } from './priority_queue.js'

// Time to pre-buffer
const PRE_BUFFER_SIZE = 1.0

export class VideoBuffer {
  constructor (sourceBuffer, videoIndex) {
    this.sourceBuffer = sourceBuffer
    this.sourceBuffer.mode = 'sequence'

    this.videoIndex = videoIndex

    this.timeAppended = 0
    this.preBuffering = 0
    this.lastTimestamp = 0
    this.lastChunk = null

    this.queue = new PriorityQueue(function (a, b) {
      return a.timestamp > b.timestamp
    })

    // Rename this to use inside callbacks
    const self = this

    this.sourceBuffer.addEventListener('updateend', function (e) {
      if (!self.needsToPreBuffer()) {
        self.appendToBuffer()
      }
    })

    this.sourceBuffer.addEventListener('error', function (e) {
      console.log(e)
    })
  }

  needsToPreBuffer () {
    return this.preBuffering < PRE_BUFFER_SIZE
  }

  getTimeAppended () {
    return this.timeAppended
  }

  getLastChunk () {
    return this.lastChunk
  }

  appendToBuffer () {
    let chunk

    do {
      chunk = this.queue.pop()
      this.preBuffering -= chunk.duration / 1000
      // Remove chunks that have a timestamp before the last appended until queue is emptied
    } while (chunk.timestamp < this.lastTimestamp && !this.queue.isEmpty())

    if (chunk.timestamp > this.lastTimestamp) {
      this.lastTimestamp = chunk.timestamp
      this.timeAppended += chunk.duration / 1000
      this.lastChunk = chunk
      this.videoIndex.addVideoChunk(chunk)
      this.sourceBuffer.appendBuffer(chunk.payload)
    }
  }

  preBufferChunk (chunk) {
    let appended = false

    this.preBuffering += chunk.duration / 1000
    this.queue.push(chunk)

    if (!this.sourceBuffer.updating && !this.needsToPreBuffer()) {
      this.appendToBuffer()
      appended = true
    }

    return appended
  }
}
