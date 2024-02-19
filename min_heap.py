class Min_heap():
    def __init__(self, items=list()):
        self.heap = [None]

        for i in items:
            self.heap.append(i)
            self.float_up(len(self.heap) - 1)

    def print(self):
        print(self.heap[1:])

    def push(self, data):
        self.heap.append(data)
        self.float_up(len(self.heap) - 1)

    def peek(self):
        if len(self.heap) > 1:
            return self.heap[1]
        else:
            return False

    def pop(self):
        if len(self.heap) > 1:
            self.heap[1], self.heap[len(
                self.heap) - 1] = self.heap[len(self.heap) - 1], self.heap[1]
            minVal = self.heap.pop()
            self.heapify(1)
        else:
            minVal = False

        return minVal

    # questa funzione come vedi non è necessaria -> basta bubble_down (heapify)
    def float_up(self, index):
        # sarebbe meglio usarla per pushare dentro i valori perchè arr.append è più veloce di arr.insert
        parent = index // 2
        # questo perchè 'self.heap[0] == None' => sempre e comunque
        if index <= 1:
            return None
        elif self.heap[index] < self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self.float_up(parent)

    def heapify(self, index):  # questa è la famosa heapify
        left = index * 2
        right = left + 1
        smallest = index
        if len(self.heap) > left and self.heap[smallest] > self.heap[left]:
            smallest = left
        if len(self.heap) > right and self.heap[smallest] > self.heap[right]:
            smallest = right
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self.heapify(smallest)
