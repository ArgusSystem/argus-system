class Node {
    constructor (element) {
        this.element = element;
        this.next = null;
    }
}

export class Queue {
    constructor () {
        this.head = null;
        this.tail = null;
        this.len = 0;
    }

    length() {
        return this.len;
    }

    append(element) {
        const node = new Node(element);

        if (this.tail === null) {
            this.head = node;
            this.tail = this.head;
        } else {
            this.tail.next = node;
            this.tail = node;
        }

        this.len++;
    }

    poll() {
        if (this.head === null)
            return null;

        const node = this.head;

        this.head = node.next;

        if (this.head === null)
            this.tail = null;

        this.len--;
        return node.element;
    }

    peek() {
        return (this.head === null) ? null : this.head.element;
    }
}