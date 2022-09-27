import { VideoAnalysis } from './video_analysis.js'

export class VideoIndex {
  constructor () {
    this.chunkIndex = {}
    this.analysisIndex = {}

    this.frameOffset = 0
    this.chunkBST = []

    this.pointer = 0
  }

  addVideoChunk (chunk) {
    this.chunkIndex[chunk.id] = { frameOffset: this.frameOffset, frameCount: chunk.frameCount }
    this.chunkBST.push([this.frameOffset, chunk.id])
    this.frameOffset += chunk.frameCount
  }

  addAnalysis (analysis) {
    this.analysisIndex[analysis.chunkId] = new VideoAnalysis(analysis)
  }

  getFrameOffset (chunkId) {
    return this.chunkIndex[chunkId].frameOffset
  }

  getBoxes (frameOffset) {
    // Use estimated pointer to avoid BST if possible
    const result = this.getBoxesFromChunkBST(frameOffset, this.pointer)

    if (result != null) {
      return result
    }

    const closestIndex = this.binarySearch(frameOffset)

    // Use max because we want the closest smallest possible
    return this.getBoxesFromChunkBST(frameOffset, closestIndex)
  }

  getBoxesFromChunkBST (frameOffset, index) {
    // Check for out of index
    if (index >= this.chunkBST.length) {
      return null
    }

    const [chunkOffset, chunkId] = this.chunkBST[index]

    const frameCount = this.chunkIndex[chunkId].frameCount
    // Subtract chunkOffset to normalize offset for chunk
    const offset = frameOffset - chunkOffset

    // Check that the offset is inside the possible frames
    if (offset >= 0 && offset < frameCount) {
      this.pointer = index
      // is currently at the last frame of the chunk, pointer should increase
      if (offset === frameCount - 1) {
        this.pointer += 1
      }

      // Check is an analysis exist
      if (chunkId in this.analysisIndex) {
        return this.analysisIndex[chunkId].getFaces(offset)
      } else {
        return null
      }
    } else {
      return null
    }
  }

  // Binary search in BST for frameOffset. Should only be used when reloading or a forced transition
  binarySearch (frameOffset) {
    let min = 0
    let max = this.chunkBST.length - 1

    while (min <= max) {
      const mid = Math.floor((max + min) / 2)

      const midFrameOffset= this.chunkBST[mid][0]

      if (midFrameOffset < frameOffset) {
        min = midFrameOffset + 1
      } else if (midFrameOffset > frameOffset) {
        max = midFrameOffset - 1
      } else {
        return midFrameOffset
      }
    }

    return max
  }
}
