

class Node:

    def __init__(self,value):
        self.value = value
        self.next = None


class LinkedList:

    def __init__(self,*values):
        if not values:
              self.head = self.tail  = None
              self.size = 0
        else:
              self.head = Node(values[0])
              current = self.head
              for k in values[1:]:
                  current.next = Node(k)
                  current = current.next
              self.tail = current
              self.size = len(values)

    def __len__(self):
        return self.size


    def __iter__(self):
        current_node = self.head
        while current_node:
            yield current_node
            current_node = current_node.next


    def __getitem__(self, index):
        assert 0 <= index < self.size, 'Invalid index'
        for k,current_node in enumerate(self):
            if k == index:
                return current_node.value


    def __setitem__(self, index, value):
        assert 0 <= index < self.size , 'Invalid index'
        previous = self.head
        for k,current_node in enumerate(self):
            if k == index:
                new = Node(value)
                new.next = current_node.next
                if index == 0:
                    self.head = new
                else:
                     previous.next = new
                break

            previous = current_node

    def __delitem__(self,index):
        assert 0 <= index < self.size, 'Invalid index'
        previous = self.head
        for k, current_node in enumerate(self):
            if k == index:
                if index == 0:
                    self.head = self.head.next
                elif k == index:
                    previous.next = current_node.next
                self.size -= 1
                break
            previous = current_node


    def append(self,value):
        if self.head:
           self.tail.next = Node(value)
           self.tail = self.tail.next
        else:
            self.head = self.tail =  Node(value)
        self.size += 1

    def reverse(self):

        start , stop = 0, self.size - 1
        while start < stop:
            self[start] , self[stop] = self[stop] , self[start]
            start ,stop  = start + 1 ,stop - 1



    def __str__(self):
        return f" [ {' -> '.join(str(node.value) for node in self)} ]"



x = LinkedList(1,2,3,4)
print(x)
x.reverse()
print(x)








