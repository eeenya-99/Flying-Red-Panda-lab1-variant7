import unittest
from hypothesis import given,  strategies

from hashmap import HashMap


class TestFoo(unittest.TestCase):

    def test_init(self):
        hm = HashMap(45)
        self.assertEqual(hm.bucket_size, 45)

        hm = HashMap(10, {2: 'abc', 'omiga': 43, 7: 'cba', 'ocean': 66})
        hKey = hm.hashFuction(2)
        self.assertEqual(hm.bucket[hKey].value, 'abc')
        # hm.hashFuction(7) == hm.hashFuction(2)
        self.assertEqual(hm.bucket[hKey].next.value, 'cba')

        hKey = hm.hashFuction('omiga')
        self.assertEqual(hm.bucket[hKey].value, 43)
        # hm.hashFuction('omiga') == hm.hashFuction('ocean')
        self.assertEqual(hm.bucket[hKey].next.value, 66)

    def test_hashFuction(self):
        hm = HashMap()
        self.assertEqual(hm.hashFuction(2), 9)
        self.assertEqual(hm.hashFuction(7), 9)
        self.assertEqual(hm.hashFuction('omiga'), 1)
        self.assertEqual(hm.hashFuction(2.14), 9)

    def test_add(self):
        hm = HashMap()
        hm.add(2, 'abc')
        self.assertEqual(hm.access_member(2), 'abc')
        hm.add(2, 100)
        self.assertEqual(hm.access_member(2), 100)

    def test_remove(self):
        hm = HashMap(
            10,
            {2: 'abc', 'omiga': 43, 7: 'cba', 'ocean': 66, 12: 'bca'})
        hm.remove(17)
        self.assertEqual(len(hm.key_existed), 5)

        hm.remove(12)
        self.assertEqual(len(hm.key_existed), 4)

        hm.remove('omiga')
        # hm.hashFuction('omiga') == hm.hashFuction('ocean')
        hKey = hm.hashFuction('omiga')
        self.assertEqual(hm.bucket[hKey].key, 'ocean')
        self.assertEqual(hm.bucket[hKey].value, 66)
        self.assertEqual(hm.bucket[hKey].next, None)

        # key 9 doesn't exist
        hm.remove(9)
        hKey = hm.hashFuction(9)
        self.assertEqual(hm.bucket[hKey], hm.empty)

    def test_access_size(self):
        hm = HashMap(10, {2: 'abc', 'omiga': 43, 7: 'cba', 'ocean': 66})
        self.assertEqual(hm.access_size(), 4)
        hm.remove('ocean')
        self.assertEqual(hm.access_size(), 3)

    def test_access_member(self):
        hm = HashMap(10, {2: 'abc', 'omiga': 43, 7: 'cba'})
        self.assertEqual(hm.access_member(7), 'cba')
        self.assertEqual(hm.access_member(100), None)

    def test_dict_to_hash(self):
        hm = HashMap()
        dict = {'omiga': 43, 7: 'cba', 'ocean': 66, 8: 'hello'}
        hm.dict_to_hash(dict)
        self.assertEqual(hm.access_member(7), 'cba')
        self.assertEqual(hm.access_size(), 4)

        hm.dict_to_hash({4: 'four'})
        self.assertEqual(hm.access_member(4), 'four')
        self.assertEqual(hm.access_size(), 5)

    def test_hash_to_dic(self):
        hm = HashMap()
        hm.add('omiga', 10)
        hm.add(2, 'abc')
        hm.add('omiga', 1000)
        hm.add('ocean', 2000)
        self.assertEqual(len(hm.key_existed), 3)
        self.assertEqual(
            hm.hash_to_dic(),
            {'omiga': 1000, 2: 'abc', 'ocean': 2000})

        hm = HashMap()
        self.assertEqual(
            hm.hash_to_dic(), {})

    def test_filter_even(self):
        hm = HashMap(10, {'a': 3.14, 'b': 43, 'c': 22, 'd': 66, 'e': 'hello'})
        hm.filter_even()
        self.assertEqual(hm.access_size(), 3)

        hm = HashMap()
        hm.filter_even()
        self.assertEqual(hm.hash_to_dic(), {})

    def test_map(self):
        hm = HashMap(10, {'a': 3.14, 'b': 43, 'c': 22, 'd': 66, 'e': 'hello'})
        hmMap = hm.map(str)
        self.assertEqual(
            hmMap,
            {'a': '3.14', 'b': '43', 'c': '22', 'd': '66', 'e': 'hello'})

        hm = HashMap(10, {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5})
        hmMap = hm.map(lambda x: x+2)
        self.assertEqual(hmMap, {'a': 3, 'b': 4, 'c': 5, 'd': 6, 'e': 7})

    def test_reduce(self):
        hm = HashMap(10, {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5})
        hmReduce = hm.reduce(lambda x, y: x+y, 0)
        self.assertEqual(hmReduce, 15)

        hm = HashMap(
            10,
            {1: 'Hello', 2: 'This', 3: 'Is', 4: 'A', 5: 'Dictionary'})
        hmReduce = hm.reduce(lambda x, y: x+y, '')
        self.assertEqual(hmReduce, 'HelloThisIsADictionary')

    def test_iter(self):
        hm = HashMap(10, {'a': 3.14, 'b': 43, 'c': 22, 'd': 66, 'e': 'hello'})
        dict = hm.hash_to_dic()
        res = {}
        for node in hm:
            res[node.key] = node.value
        self.assertEqual(dict, res)

    @given(
        dictA=strategies.dictionaries(
            strategies.integers(), strategies.integers()),
        dictB=strategies.dictionaries(
            strategies.integers(), strategies.integers()),
        dictC=strategies.dictionaries(
            strategies.integers(), strategies.integers()),
        )
    def test_monoid_associativity(self, dictA, dictB, dictC):
        hm = HashMap()
        hmA = HashMap(10, dictA)
        hmB = HashMap(10, dictB)
        hmC = HashMap(10, dictC)
        # (a•b)•c = a•(b•c)
        self.assertEqual(
            hm.concatHM(hm.concatHM(hmA, hmB), hmC),
            hm.concatHM(hmA, hm.concatHM(hmB, hmC)))

    @given(dict=strategies.dictionaries(
        strategies.integers(), strategies.integers()))
    def test_monoid_identify(self, dict):
        hmA = HashMap(10, dict)
        hm = HashMap()
        # a•e = a
        self.assertEqual(hmA.concatHM(hmA, hm.emptyHM()), hmA)
        # e•a = a
        self.assertEqual(hmA.concatHM(hm.emptyHM(), hmA), hmA)
