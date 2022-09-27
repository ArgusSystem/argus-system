const top = 0
const parent = (c) => ((c + 1) >>> 1) - 1
const left = (c) => (c << 1) + 1
const right = (c) => (c + 1) << 1

export class PriorityQueue {
  constructor(c = (d, e) => d > e) {
    this._heap = []
    this._comparator = c
  }

  size() {
    return this._heap.length
  }

  isEmpty() {
    return 0 === this.size()
  }

  peek() {
    return this._heap[top]
  }

  push(...c) {
    c.forEach((d) => {
      this._heap.push(d)
      this._siftUp()
    })

    return this.size()
  }

  pop() {
    const c = this.peek()
    const d = this.size() - 1

    if (d > top) {
      this._swap(top, d)
      this._heap.pop()
      this._siftDown()
    }

    return c
  }

  replace(c) {
    const d = this.peek()
    this._heap[top] = c
    this._siftDown()
    return d
  }

  _greater(c, d) {
    return this._comparator(this._heap[c], this._heap[d])
  }

  _swap(c, d) {
    [this._heap[c], this._heap[d]] = [this._heap[d], this._heap[c]]
  }

  _siftUp() {
    for (let c = this.size() - 1; c > top && this._greater(c, parent(c)); ) {
      this._swap(c, parent(c))
      c = parent(c)
    }
  }

  _siftDown() {
    for (let d, c = top; (left(c) < this.size() && this._greater(left(c), c)) || (right(c) < this.size() && this._greater(right(c), c)); ) {
      d = right(c)

      if (d < this.size() && this._greater(right(c), left(c)))  {
        right(c)
      } else {
        left(c)
      }

      this._swap(c, d)

      c = d
    }
  }
}
