from typing import Union, Dict, Optional, Mapping, Any, List
from collections.abc import Callable

defineType = Union[str, int, float]

mapType = Mapping[defineType, defineType]
dictType = Dict[defineType, defineType]


class Node(object):
    def __init__(
                self,
                key: Optional[defineType] = None,
                value: Optional[defineType] = None,
                next: Optional["Node"] = None):
        self.key = key
        self.value = value
        self.next = next

# for hashmap's iteration


class Iter(object):
    def __init__(self, hashmap: "HashMap"):
        self.hashmap = hashmap
        self.iter_n = 0

    def __next__(self) -> "Node":
        if self.iter_n < len(self.hashmap.key_existed):
            key = self.hashmap.key_existed[self.iter_n]
            value = self.hashmap.access_member(key)
            node = Node(key, value)
            self.iter_n += 1
            return node
        else:
            raise StopIteration()  # signals "the end"


class HashMap(object):
    def __init__(self, dict: Optional[mapType] = None, size: int = 10):
        '''
        Initialize HashMap
        :param dict: initialize by the given dictionary (defaults is None)
        :param size: bucket size of HashMap (defaults is 10)
        '''
        self.bucket_size = size  # hashmap bucket size
        self.bucket = [Node()] * self.bucket_size
        # 'key_existed' store existed key in the dictionary
        self.key_existed: List[defineType] = []
        if dict is not None:  # if dictionary is provided
            self.dict_to_hash(dict)

    def hashFuction(self, key: defineType) -> int:
        '''
        Get HashMap address based on key value
        :param key: the key of the element
        :return: HashMap address
        '''
        hf = 0
        if type(key) == str:
            hf = ord(key[0])
        if type(key) == float:
            hf = int(key)
        if type(key) == int:
            hf = key
        hf = 8 * hf + 3
        hf %= self.bucket_size
        return hf

    def add(self, key: defineType, value: defineType) -> None:
        '''
        Add a new element to the HashMap
        :param key: the key of the element
        :param value: the value of the element
        '''
        hKey = self.hashFuction(key)
        node = Node(key, value)

        if self.bucket[hKey].key is None:
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

    def remove(self, key: defineType) -> None:
        '''
        Remove an element from HashMap by key
        :param key: the key of the element
        '''
        if key not in self.key_existed:
            return
        hKey = self.hashFuction(key)
        self.key_existed.remove(key)

        p = self.bucket[hKey]
        q = p.next
        if p.key == key:
            del p
            if q:
                self.bucket[hKey] = q
            else:
                self.bucket[hKey] = Node()
            return
        while q:
            if q.key == key:
                p.next = q.next
                del q
                return
            p = q
            q = p.next

    def access_size(self) -> int:
        '''
        Access the number of elements in the HashMap
        '''
        return len(self.key_existed)

    def access_member(self, key: defineType) -> Any:
        '''
        Access a element's value by its key
        :param key: the key of the element
        :return: the value corresponding to the key in the HashMap
        '''
        if key not in self.key_existed:
            return None
        hKey = self.hashFuction(key)
        p: Optional[Node] = self.bucket[hKey]
        while p:
            if p.key == key:
                return p.value
            p = p.next

    def dict_to_hash(self, dict: mapType) -> None:
        '''
        Conversion from built-in dictionary
        :param dict: the given built-in dictionary
        '''
        for key, value in dict.items():
            self.add(key, value)

    def hash_to_dict(self) -> dictType:
        '''
        Conversion to built-in dictionary
        :return: dictionary conversed from HashMap
        '''
        res: dictType = {}
        if len(self.key_existed) == 0:
            return res
        for key in self.key_existed:
            value = self.access_member(key)
            res[key] = value
        return res

    def filter(self, func: Optional[Callable[..., bool]] = None) -> None:
        '''
        Filter data structure by specific predicate
        :param func: predicate (specific filter function)
        '''
        if (len(self.key_existed) == 0) or func is None:
            return
        keyFunc = []
        for key in self.key_existed:
            value = self.access_member(key)
            if not func(value):
                keyFunc.append(key)
        for key in keyFunc:
            self.remove(key)

    def map(self, func: Optional[Callable[..., Any]] = None) -> None:
        '''
        Map structure by specific function
        :param func: specific map function
        '''
        if func is None:
            return
        for key in self.key_existed:
            value = self.access_member(key)
            self.add(key, func(value))

    def reduce(self, func: Callable[..., Any], initValue: defineType) -> Any:
        '''
        Reduce the HashMap to one value
        :param func: specific reduce method
        :param initValue: initial value for reduce
        :return: result of the reduce
        '''
        res = initValue
        for key in self.key_existed:
            value = self.access_member(key)
            res = func(res, value)
        return res

    def __iter__(self) -> Iter:
        '''
        Get an iterator
        :return: an object of class Iter
        '''
        return Iter(self)

    # 9. empty
    def empty(self) -> None:
        '''
        Operation in property monoid identify
        '''
        for key in self.key_existed:
            self.remove(key)

    # 10. concat
    def concat(self, hashMap: "HashMap") -> None:
        '''
        Operation in property monoid associativity
        :param hashMap: another HashMap concats to the current HashMap
        '''
        for key in hashMap.key_existed:
            self.add(key, hashMap.access_member(key))
