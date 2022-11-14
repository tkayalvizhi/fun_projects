class FIFOQueue(object):
    def __init__(self):
        self.arr = []
    
    def push_item(self, item):
        self.arr.insert(0, item)
    
    def pop_item(self):
        item = self.arr[-1]
        self.arr = self.arr[:-1]
    
    def get_last(self):
        return self.arr[-1]
    
    def is_null(self):
        return len(self.arr) == 0
    
    def __len__(self):
        return len(self.arr)
