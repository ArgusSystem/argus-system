export class VideoAnalysis {
  constructor (analysis) {
    this.chunkId = analysis.chunkId
    this.frameCount = analysis.frameCount
    this.offsetIndex = []
    this.framesByOffset = {}

    for (const frame in analysis.frames) {
      this.framesByOffset[frame.offset] = frame
    }

    const offsets = analysis.frames.map((frame) => frame.offset)
    offsets.push(this.frameCount)
    offsets.sort()

    for (let i = 0; i < offsets.length - 1; i++) {
      for (let j = offsets[i]; j < offsets[i + 1]; j++) {
        this.offsetIndex.push(offsets[i])
      }
    }
  }

  getFaces (frameOffset) {
    return this.framesByOffset[this.offsetIndex[frameOffset]].faces
  }
}
