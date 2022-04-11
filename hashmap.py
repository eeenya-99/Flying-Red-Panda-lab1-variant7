class Node(object):
    def __init__(self, key=None, value=None, next=None):
        self.key = key
        self.value = value
        self.next = next


class HashMap(object):
    empty = object()

    def __init__(self, size=10, dict=None):
        self.bucket_size = size  # hashmap bucket size
        self.bucket = [self.empty] * self.bucket_size
        self.key_existed = []  # store existed key in the dictionary
        if dict is not None:  # if dictionary is provided
            self.dict_to_hash(dict)
        self.iter_n = 0  # for iteration

    def hashFuction(self, key):
        if type(key) == str:
            key = ord(key[0])
        if type(key) == float:
            key = int(key)
        hf = 8 * key + 3
        hf %= self.bucket_size
        return hf

    # 1. Add a new element
    def add(self, key, value):
        hKey = self.hashFuction(key)
        node = Node(key, value)

        if self.bucket[hKey] == self.empty:
            self.bucket[hKey] = node
            self.key_existed.append(key)
        else:
            p = self.bucket[hKey]
            while p:
                if p.key == key:
                    p.value = value
                    return
                if p.next is None:
                    break
                else:
                    p = p.next
            p.next = node
            self.key_existed.append(key)

    # 2. Remove an element
    def remove(self, key):
        if key not in self.key_existed:
            return
        hKey = self.hashFuction(key)
        self.key_existed.remove(key)

        p = self.bucket[hKey]
        q = p.next
        if p.key == key:
            if q:
                self.bucket[hKey] = q
            else:
                self.bucket[hKey] = self.empty
            return
        while q:
            if q.key == key:
                p.next = q.next
                return
            p = q
            q = p.next

    # 3.1 Access: size
    def access_size(self):
        return len(self.key_existed)

    # 3.2 Access: member
    def access_member(self, key):
        if key not in self.key_existed:
            return None
        hKey = self.hashFuction(key)
        p = self.bucket[hKey]
        while p:
            if p.key == key:
                return p.value
            p = p.next

    # 4.1 Conversion from/to built-in dictionary: from_dict
    def dict_to_hash(self, dict):
        for key, value in dict.items():
            self.add(key, value)

    # 4.2 Conversion from/to built-in dictionary: to_dict
    def hash_to_dic(self):
        res = {}
        if len(self.key_existed) == 0:
            return res
        for item in self.bucket:
            if item == self.empty:
                continue
            p = item
            while p:
                res[p.key] = p.value
                if p.next is None:
                    break
                else:
                    p = p.next
        return res

    # 5. Filter data structure by specific predicate: even
    def filter_even(self):
        if len(self.key_existed) == 0:
            return
        keyOfEven = []
        for key in self.key_existed:
            value = self.access_member(key)
            if (not type(value) is str) and (value % 2 == 0):
                keyOfEven.append(key)
        for key in keyOfEven:
            self.remove(key)

    # 6. Map structure by specific function
    def map(self, func):
        res = {}
        for key in self.key_existed:
            value = self.access_member(key)
            res[key] = func(value)
        return res

    # 7. Reduce
    def reduce(self, func, initValue):
        res = initValue
        for key in self.key_existed:
            value = self.access_member(key)
            res = func(res, value)
        return res

    # 8. iterator
    def __iter__(self):
        return self

    def __next__(self):
        if self.iter_n < len(self.key_existed):
            key = self.key_existed[self.iter_n]
            value = self.access_member(self.key_existed[self.iter_n])
            node = Node(key, value)
            self.iter_n += 1
            return node
        raise StopIteration()  # signals "the end"

    # 9. empty
    def emptyHM(self):
        return None

    # 10. concat
    def concatHM(self, hashMap1=None, hashMap2=None):
        if hashMap1 is None:
            return hashMap2
        if hashMap2 is None:
            return hashMap1
        for key in hashMap2.key_existed:
            hashMap1.add(key, hashMap2.access_member(key))
        return hashMap1
